#!/usr/bin/env python3
"""Run the benchmark prompts through headless Claude Code, with and without the skill.

Each run is one `claude -p` process in an empty temporary directory. The full
stream-json transcript is saved so that sources can be analysed afterwards.

    python3 bench/run.py --smoke          # one prompt per arm, checks the setup
    python3 bench/run.py                  # full benchmark
    python3 bench/run.py --out bench/runs/<dir>   # resume an interrupted run
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_prompts, parse_transcript, run_stem, skill_fired  # noqa: E402

HERE = Path(__file__).resolve().parent
ARMS = ("baseline", "baseline-nudge", "skill", "skill-forced")
SKILL_ARMS = ("skill", "skill-forced")
# One sentence a user could add themselves. Tests how much of the skill's effect is
# simply "search first and check for recalls".
NUDGE = ("Before answering a question about buying a product, search the web, and check "
         "whether the product has been recalled or has failed an independent safety test.")
BLOCKED_TOOLS = "Bash,Write,Edit,NotebookEdit,Agent"
SYNC_VARS = ("CLAUDE_CODE_SYNC_SKILLS", "CLAUDE_CODE_SYNC_PLUGINS",
             "CLAUDE_CODE_CCR_EARLY_PLUGINS_SYNC", "CLAUDE_CODE_ENABLE_CFC")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_command(args, arm: str) -> list[str]:
    allowed = "WebSearch,WebFetch" + (",Skill" if arm in SKILL_ARMS else "")
    cmd = [
        args.claude_bin, "-p",
        "--output-format", "stream-json", "--verbose",
        "--no-session-persistence",
        "--permission-mode", "dontAsk",
        "--strict-mcp-config",
        "--allowedTools", allowed,
        "--disallowedTools", BLOCKED_TOOLS,
    ]
    if args.no_chrome:
        cmd.append("--no-chrome")
    if arm in SKILL_ARMS:
        cmd += ["--plugin-dir", str(args.plugin_dir)]
    if arm == "baseline-nudge":
        cmd += ["--append-system-prompt", NUDGE]
    if args.model:
        cmd += ["--model", args.model]
    return cmd


def check_setup(transcript: dict, arm: str, args) -> list[str]:
    """Return a list of problems with how the session was set up."""
    init = transcript["init"]
    if init is None:
        return ["no init event in the output (did claude start?)"]
    problems = []
    tools = init.get("tools") or []
    for tool in ("WebSearch", "WebFetch"):
        if tool not in tools:
            problems.append(f"{tool} is not available in this session")
    # Plugins built into Claude Code itself are the same in both arms; ignore them.
    plugins = [p.get("name") for p in init.get("plugins") or [] if p.get("path") != "builtin"]
    listed = (init.get("skills") or []) + (init.get("slash_commands") or [])
    has_skill = any(str(s).endswith(args.skill_name) for s in listed)
    if arm not in SKILL_ARMS:
        if args.plugin_name in plugins:
            problems.append("baseline loaded the plugin under test")
        elif plugins:
            # Organisation-managed plugins survive the clean config directory. They are the
            # same in every arm, so this is reported once in the manifest, not as a problem.
            pass
        if has_skill:
            problems.append("baseline can see the skill under test")
    else:
        if args.plugin_name not in plugins:
            problems.append(f"plugin '{args.plugin_name}' did not load (loaded: {plugins})")
        if not has_skill:
            problems.append(f"skill '{args.skill_name}' is not listed in the session")
        if "Skill" not in tools:
            problems.append("Skill tool is not available in this session")
    servers = [s.get("name") for s in init.get("mcp_servers") or []]
    if servers:
        problems.append(f"MCP servers connected: {servers}")
    return problems


def one_run(args, prompt: dict, arm: str, rep: int) -> dict:
    stem = run_stem(prompt["id"], arm, rep)
    raw_path = args.out / "raw" / f"{stem}.jsonl"
    meta_path = args.out / "raw" / f"{stem}.meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        if meta.get("ok"):
            meta["resumed"] = True
            return meta

    text = prompt["prompt"]
    if arm == "skill-forced":
        text = f"/{args.plugin_name}:{args.skill_name} {text}"

    env = os.environ.copy()
    if args.isolation == "config-dir":
        env["CLAUDE_CONFIG_DIR"] = str(args.config_dir)
        for var in SYNC_VARS:  # these would pull the operator's own skills and plugins back in
            env.pop(var, None)

    workdir = Path(tempfile.mkdtemp(prefix="unsponsored-run-"))
    started = time.time()
    error, stdout, stderr = None, "", ""
    try:
        proc = subprocess.run(
            build_command(args, arm), input=text, capture_output=True, text=True,
            cwd=workdir, env=env, timeout=args.timeout,
        )
        stdout, stderr = proc.stdout, proc.stderr
        if proc.returncode != 0:
            error = f"exit code {proc.returncode}"
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        error = f"timed out after {args.timeout}s"
    except FileNotFoundError:
        error = f"'{args.claude_bin}' not found; is Claude Code installed and on PATH?"
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    raw_path.write_text(stdout, encoding="utf-8")
    if stderr.strip():
        raw_path.with_suffix(".stderr.txt").write_text(stderr, encoding="utf-8")

    transcript = parse_transcript(raw_path)
    result = transcript["result"] or {}
    if error is None and not transcript["result"]:
        error = "no result event in the output"
    if error is None and result.get("is_error"):
        error = f"claude reported an error: {str(result.get('result'))[:200]}"

    meta = {
        "stem": stem,
        "prompt_id": prompt["id"],
        "arm": arm,
        "rep": rep,
        "ok": error is None,
        "error": error,
        "setup_problems": check_setup(transcript, arm, args),
        "skill_fired": skill_fired(transcript, args.skill_name),
        "tools_used": [c["name"] for c in transcript["tool_calls"]],
        "other_plugins": sorted(p.get("name") for p in (transcript["init"] or {}).get("plugins") or []
                                if p.get("path") != "builtin" and p.get("name") != args.plugin_name),
        "model": (transcript["init"] or {}).get("model"),
        "claude_code_version": (transcript["init"] or {}).get("claude_code_version"),
        "wall_seconds": round(time.time() - started, 1),
        "finished_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def smoke(args, prompts: list[dict]) -> int:
    prompt = next((p for p in prompts if p["type"] == "verify_trap"), prompts[0])
    print(f"Smoke test with prompt '{prompt['id']}', one run per arm.\n")
    failed = False
    for arm in args.arms:
        meta = one_run(args, prompt, arm, 0)
        transcript = parse_transcript(args.out / "raw" / f"{meta['stem']}.jsonl")
        print(f"[{arm}] model={meta['model']}  claude={meta['claude_code_version']}  "
              f"{meta['wall_seconds']}s")
        print(f"  tools used: {meta['tools_used'] or 'none'}")
        if arm in SKILL_ARMS:
            print(f"  skill fired: {meta['skill_fired']}")
        for problem in meta["setup_problems"]:
            print(f"  SETUP PROBLEM: {problem}")
        if meta["error"]:
            print(f"  ERROR: {meta['error']}")
        if not any(t in ("WebSearch", "WebFetch") for t in meta["tools_used"]):
            print("  WARNING: the run did not search the web")
        print("  answer starts: " + transcript["final_text"][:300].replace("\n", " ") + "\n")
        failed = failed or bool(meta["error"] or meta["setup_problems"])
    if failed:
        print("Smoke test FAILED. Fix the problems above before the full run.\n"
              "If the error is about signing in, see 'Isolation' in bench/METHODOLOGY.md.")
        return 1
    print("Smoke test passed.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompts", type=Path, default=HERE / "prompts.jsonl")
    ap.add_argument("--plugin-dir", type=Path, default=HERE.parent / "plugins" / "unsponsored")
    ap.add_argument("--plugin-name", default="unsponsored")
    ap.add_argument("--skill-name", default="product-research")
    ap.add_argument("--out", type=Path, help="output directory (default: bench/runs/<timestamp>)")
    ap.add_argument("--arms", default="baseline,skill",
                    help=f"comma-separated, from: {', '.join(ARMS)}")
    ap.add_argument("--runs", type=int, default=3, help="repetitions per prompt per arm")
    ap.add_argument("--model", help="model alias or id; default is your Claude Code default")
    ap.add_argument("--concurrency", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=900, help="seconds per run")
    ap.add_argument("--types", help="only these prompt types, comma-separated")
    ap.add_argument("--ids", help="only these prompt ids, comma-separated")
    ap.add_argument("--limit", type=int, help="only the first N prompts after filtering")
    ap.add_argument("--isolation", choices=("config-dir", "none"), default="config-dir")
    ap.add_argument("--config-dir", type=Path, default=HERE / ".claude-clean",
                    help="clean Claude Code config directory (default: bench/.claude-clean)")
    ap.add_argument("--keep-chrome", dest="no_chrome", action="store_false",
                    help="do not pass --no-chrome to claude")
    ap.add_argument("--claude-bin", default="claude")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--smoke", action="store_true", help="run one prompt per arm and check the setup")
    args = ap.parse_args()

    args.arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    for arm in args.arms:
        if arm not in ARMS:
            ap.error(f"unknown arm '{arm}'")
    if args.isolation == "config-dir":
        args.config_dir = args.config_dir.resolve()
        args.config_dir.mkdir(parents=True, exist_ok=True)
    args.plugin_dir = args.plugin_dir.resolve()
    skill_md = args.plugin_dir / "skills" / args.skill_name / "SKILL.md"
    if not skill_md.exists():
        ap.error(f"skill not found at {skill_md}")

    prompts = load_prompts(args.prompts)
    if args.types:
        wanted = set(args.types.split(","))
        prompts = [p for p in prompts if p["type"] in wanted]
    if args.ids:
        wanted = set(args.ids.split(","))
        prompts = [p for p in prompts if p["id"] in wanted]
    if args.limit:
        prompts = prompts[: args.limit]
    if not prompts:
        ap.error("no prompts selected")

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    if args.out is None:
        args.out = HERE / "runs" / (("smoke-" if args.smoke else "") + stamp)
    args.out = args.out.resolve()
    (args.out / "raw").mkdir(parents=True, exist_ok=True)

    if args.smoke:
        return smoke(args, prompts)

    manifest = {
        "started_at": stamp,
        "arms": args.arms,
        "runs_per_arm": args.runs,
        "model_requested": args.model,
        "isolation": args.isolation,
        "timeout_seconds": args.timeout,
        "prompts_file": str(args.prompts),
        "prompts_sha256": sha256(args.prompts),
        "skill_sha256": sha256(skill_md),
        "prompt_ids": [p["id"] for p in prompts],
        "blocked_tools": BLOCKED_TOOLS,
    }
    # A later run into the same folder (another arm, a retry) must not erase the record of
    # the first one: keep the original manifest and append this invocation to it.
    manifest_path = args.out / "manifest.json"
    if manifest_path.exists():
        first = json.loads(manifest_path.read_text(encoding="utf-8"))
        first.setdefault("later_invocations", []).append(manifest)
        manifest = first
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Shuffle so the arms are interleaved in time: search results drift during a long run.
    jobs = [(p, arm, rep) for p in prompts for arm in args.arms for rep in range(args.runs)]
    random.Random(args.seed).shuffle(jobs)
    print(f"{len(jobs)} runs -> {args.out}")

    done = failed = 0
    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
        futures = [pool.submit(one_run, args, p, arm, rep) for p, arm, rep in jobs]
        for fut in as_completed(futures):
            meta = fut.result()
            done += 1
            flag = "ok"
            if not meta["ok"]:
                failed += 1
                flag = f"FAILED: {meta['error']}"
            elif meta["setup_problems"]:
                flag = "ok, SETUP PROBLEMS: " + "; ".join(meta["setup_problems"])
            if meta.get("resumed"):
                flag += " (already done)"
            print(f"[{done}/{len(jobs)}] {meta['stem']}: {flag}", flush=True)

    print(f"\nFinished: {done - failed} ok, {failed} failed.")
    if failed:
        print(f"Re-run with --out {args.out} to retry the failed runs.")
    print(f"Next: python3 bench/judge.py {args.out}  &&  python3 bench/analyze.py {args.out}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
