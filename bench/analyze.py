#!/usr/bin/env python3
"""Turn saved transcripts (and judge scores, if present) into a comparison report.

    python3 bench/analyze.py bench/runs/<dir>

Writes report.md, summary.json, runs.csv and unknown_domains.txt into the run directory.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (CATEGORIES, DomainClassifier, extract_urls, load_prompts,  # noqa: E402
                    parse_stem, parse_transcript, skill_fired)

HERE = Path(__file__).resolve().parent
EVIDENCE_QUERY = re.compile(
    r"recall|rückruf|rueckruf|safety|warning|defect|complaint|problem|fail|crash test|"
    r"\btest\b|adac|warentest|consumer reports|which\?|cpsc|nhtsa|safety gate",
    re.IGNORECASE,
)

# (key, label, kind) - kind decides formatting; all are per-run numbers or None.
METRICS = [
    ("cites_independent", "Answers citing an independent test body", "pct"),
    ("cites_independent_grounded", "...and that source was actually retrieved in the run", "pct"),
    ("cites_regulator", "Answers citing a regulator or recall database", "pct"),
    ("cited_share_independent_test", "Share of cited sites: independent tests", "pct"),
    ("cited_share_regulator", "Share of cited sites: regulators", "pct"),
    ("cited_share_editorial_affiliate", "Share of cited sites: affiliate-funded editorial", "pct"),
    ("cited_share_retailer", "Share of cited sites: retailers", "pct"),
    ("cited_share_manufacturer", "Share of cited sites: manufacturers", "pct"),
    ("cited_share_ugc", "Share of cited sites: forums and social", "pct"),
    ("cited_share_news", "Share of cited sites: news media", "pct"),
    ("cited_share_unknown", "Share of cited sites: unclassified", "pct"),
    ("fetched_share_independent_test", "Share of opened pages: independent tests", "pct"),
    ("fetched_share_editorial_affiliate", "Share of opened pages: affiliate-funded editorial", "pct"),
    ("evidence_query_rate", "Share of searches aimed at tests, recalls or problems", "pct"),
    ("n_cited_sites", "Sites cited per answer", "num"),
    ("n_searches", "Web searches per run", "num"),
    ("n_fetches", "Pages opened per run", "num"),
    ("words", "Answer length, words", "num"),
    ("cost_usd", "Cost per run, USD (Claude Code estimate)", "usd"),
    ("duration_s", "Time per run, seconds", "num"),
    ("gives_recommendation", "Answers that commit to a recommendation", "pct"),
    ("provenance", "Provenance score (0-2)", "num"),
    ("negatives", "Negatives score (0-2)", "num"),
    ("flags_gaps", "Answers that say what could not be verified", "pct"),
    ("constraint_violation", "Answers breaking a stated constraint", "pct"),
]


def share(urls_by_cat: Counter, cat: str):
    total = sum(urls_by_cat.values())
    return urls_by_cat[cat] / total if total else None


def analyse_run(raw: Path, clf: DomainClassifier, skill_name: str) -> dict:
    prompt_id, arm, rep = parse_stem(raw.stem)
    t = parse_transcript(raw)
    result = t["result"] or {}
    queries, fetched, seen = [], [], []
    for call in t["tool_calls"]:
        if call["name"] == "WebSearch":
            queries.append(str(call["input"].get("query", "")))
            seen += extract_urls(t["tool_results"].get(call["id"], ""))
        elif call["name"] == "WebFetch":
            url = call["input"].get("url")
            if url:
                fetched.append(url)
    cited = extract_urls(t["final_text"])

    def sites(urls):  # one entry per site, so ten links to one site count once
        return {clf.host_of(u): clf.classify(u) for u in urls if clf.host_of(u)}

    cited_sites, fetched_sites, seen_sites = sites(cited), sites(fetched), sites(seen)
    cited_cats, fetched_cats = Counter(cited_sites.values()), Counter(fetched_sites.values())
    retrieved_hosts = set(fetched_sites) | set(seen_sites)
    indep_cited = [h for h, c in cited_sites.items() if c == "independent_test"]

    row = {
        "stem": raw.stem, "prompt_id": prompt_id, "arm": arm, "rep": rep,
        "ok": bool(t["result"]) and not result.get("is_error") and bool(t["final_text"].strip()),
        "skill_fired": skill_fired(t, skill_name),
        "n_searches": len(queries), "n_fetches": len(fetched),
        "n_cited_sites": len(cited_sites),
        "cites_independent": float(bool(indep_cited)),
        "cites_independent_grounded": float(any(h in retrieved_hosts for h in indep_cited)),
        "cites_regulator": float(cited_cats["regulator"] > 0),
        "evidence_query_rate": (sum(bool(EVIDENCE_QUERY.search(q)) for q in queries) / len(queries)
                                if queries else None),
        "words": len(t["final_text"].split()),
        "cost_usd": result.get("total_cost_usd"),
        "duration_s": (result.get("duration_ms") or 0) / 1000 or None,
        "_unknown": [h for h, c in {**seen_sites, **fetched_sites, **cited_sites}.items()
                     if c == "unknown"],
    }
    for cat in CATEGORIES:
        row[f"cited_share_{cat}"] = share(cited_cats, cat)
        row[f"fetched_share_{cat}"] = share(fetched_cats, cat)
    return row


def per_prompt_means(rows: list[dict], key: str) -> dict[str, dict[str, float]]:
    """arm -> prompt_id -> mean over that prompt's runs (runs without a value are skipped)."""
    acc = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r.get(key) is not None:
            acc[r["arm"]][r["prompt_id"]].append(float(r[key]))
    return {arm: {pid: mean(v) for pid, v in d.items()} for arm, d in acc.items()}


def paired(base: dict, other: dict, seed: int = 0):
    """Mean paired difference over prompts present in both arms, with a bootstrap 95% CI."""
    ids = sorted(set(base) & set(other))
    if not ids:
        return None
    diffs = [other[i] - base[i] for i in ids]
    rng = random.Random(seed)
    boots = sorted(mean(rng.choices(diffs, k=len(diffs))) for _ in range(2000))
    return {"n_prompts": len(ids), "base": mean(base[i] for i in ids),
            "other": mean(other[i] for i in ids), "diff": mean(diffs),
            "ci_low": boots[49], "ci_high": boots[1949]}


def fmt(value, kind: str, signed: bool = False) -> str:
    if value is None:
        return "n/a"
    sign = "+" if signed and value >= 0 else ""
    if kind == "pct":
        return f"{sign}{value * 100:.0f}" + (" pts" if signed else "%")
    if kind == "usd":
        return f"{sign}{value:.2f}"
    return f"{sign}{value:.2f}"


def norm(name) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (name or "").lower()).strip()


def agreement(picks_a: list[str], picks_b: list[str], same_list: bool) -> list[float]:
    pairs = itertools.combinations(picks_a, 2) if same_list else itertools.product(picks_a, picks_b)
    return [float(a == b) for a, b in pairs]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--prompts", type=Path, default=HERE / "prompts.jsonl")
    ap.add_argument("--domains", type=Path, default=HERE / "domains.csv")
    ap.add_argument("--skill-name", default="product-research")
    ap.add_argument("--baseline", default="baseline")
    args = ap.parse_args()

    prompts = {p["id"]: p for p in load_prompts(args.prompts)}
    clf = DomainClassifier(args.domains)
    raws = sorted((args.run_dir / "raw").glob("*.jsonl"))
    if not raws:
        raise SystemExit(f"no transcripts in {args.run_dir / 'raw'}")
    rows = [analyse_run(raw, clf, args.skill_name) for raw in raws]

    judged = 0
    jpath = args.run_dir / "judgments.jsonl"
    if jpath.exists():
        by_stem = {}
        for line in jpath.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            if rec.get("judgment"):
                by_stem[rec["stem"]] = rec["judgment"]
        for r in rows:
            j = by_stem.get(r["stem"])
            if j:
                judged += 1
                for key in ("gives_recommendation", "provenance", "negatives", "flags_gaps",
                            "constraint_violation", "fact_mentioned", "false_alarm"):
                    r[key] = None if j.get(key) is None else float(j[key])
                r["top_pick"], r["top_pick_brand"] = norm(j.get("top_pick")), norm(j.get("top_pick_brand"))

    failed = [r for r in rows if not r["ok"]]
    good = [r for r in rows if r["ok"]]
    arms = sorted({r["arm"] for r in good}, key=lambda a: (a != args.baseline, a))
    others = [a for a in arms if a != args.baseline]

    summary = {"arms": arms, "runs_total": len(rows), "runs_failed": len(failed),
               "runs_judged": judged, "metrics": {}, "by_type": {}}
    out = ["# Benchmark report", "",
           f"Run directory: `{args.run_dir.name}`. {len(good)} usable runs, {len(failed)} failed, "
           f"{judged} judged. Arms: {', '.join(arms)}.", ""]
    if (args.run_dir / "manifest.json").exists():
        m = json.loads((args.run_dir / "manifest.json").read_text())
        out += [f"Skill version (sha256 of SKILL.md): `{m.get('skill_sha256', '')[:12]}`. "
                f"Isolation: {m.get('isolation')}. Runs per prompt per arm: {m.get('runs_per_arm')}.", ""]

    for arm in others:
        fired = [r["skill_fired"] for r in good if r["arm"] == arm]
        if fired:
            rate = sum(fired) / len(fired)
            summary[f"skill_fired_rate_{arm}"] = rate
            out.append(f"Skill was loaded in {rate * 100:.0f}% of `{arm}` runs ({sum(fired)}/{len(fired)}).")
    out.append("")

    out += ["## Headline comparison", "",
            "Each prompt counts once (its runs are averaged first). The difference is paired by "
            "prompt, with a bootstrap 95% interval over prompts. An interval that includes zero "
            "means the data does not show a difference.", ""]
    for arm in others:
        out += [f"### {arm} vs {args.baseline}", "",
                f"| Metric | {args.baseline} | {arm} | Difference | 95% interval | Prompts |",
                "|---|---|---|---|---|---|"]
        for key, label, kind in METRICS:
            means = per_prompt_means(good, key)
            res = paired(means.get(args.baseline, {}), means.get(arm, {}))
            if res is None:
                continue
            summary["metrics"].setdefault(arm, {})[key] = res
            out.append(f"| {label} | {fmt(res['base'], kind)} | {fmt(res['other'], kind)} | "
                       f"{fmt(res['diff'], kind, True)} | {fmt(res['ci_low'], kind, True)} to "
                       f"{fmt(res['ci_high'], kind, True)} | {res['n_prompts']} |")
        out.append("")

    if judged:
        out += ["## Known-answer checks", "",
                "Trap prompts ask about a product with a documented recall or failed test. "
                "Control prompts ask about a product that passed the same test.", "",
                "| Check | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms)]
        checks = [("verify_trap", "fact_mentioned", "Trap: problem reported"),
                  ("verify_control", "fact_mentioned", "Control: good test result reported"),
                  ("verify_control", "false_alarm", "Control: false alarm raised")]
        for ptype, key, label in checks:
            cells = []
            for arm in arms:
                vals = [r[key] for r in good if r["arm"] == arm and r.get(key) is not None
                        and prompts.get(r["prompt_id"], {}).get("type") == ptype]
                summary["by_type"].setdefault(label, {})[arm] = (
                    {"rate": mean(vals), "n": len(vals)} if vals else None)
                cells.append(f"{sum(vals):.0f}/{len(vals)} ({mean(vals) * 100:.0f}%)" if vals else "n/a")
            out.append(f"| {label} | " + " | ".join(cells) + " |")
        out.append("")

        out += ["## Do the recommendations change?", "",
                "Agreement is the chance that two runs of the same prompt name the same top pick. "
                "Agreement between arms should be read against agreement within an arm, which is "
                "the noise level.", ""]
        picks = defaultdict(lambda: defaultdict(list))
        for r in good:
            if r.get("top_pick"):
                picks[r["prompt_id"]][r["arm"]].append(r["top_pick"])
        for arm in arms:
            within = [x for p in picks.values() for x in agreement(p.get(arm, []), [], True)]
            brands = Counter(r["top_pick_brand"] for r in good if r["arm"] == arm and r.get("top_pick_brand"))
            top3 = sum(c for _, c in brands.most_common(3)) / sum(brands.values()) if brands else None
            summary.setdefault("recommendations", {})[arm] = {
                "within_arm_agreement": mean(within) if within else None,
                "distinct_brands": len(brands), "top3_brand_share": top3}
            out.append(f"- `{arm}`: within-arm agreement {fmt(mean(within) if within else None, 'pct')}, "
                       f"{len(brands)} distinct top-pick brands, top three brands take "
                       f"{fmt(top3, 'pct')} of top picks.")
        for arm in others:
            between = [x for p in picks.values()
                       for x in agreement(p.get(args.baseline, []), p.get(arm, []), False)]
            summary["recommendations"][f"{arm}_vs_{args.baseline}_agreement"] = (
                mean(between) if between else None)
            out.append(f"- `{arm}` vs `{args.baseline}`: agreement "
                       f"{fmt(mean(between) if between else None, 'pct')}.")
        out.append("")
    else:
        out += ["_No judge scores found. Run `python3 bench/judge.py <run dir>` to add the "
                "known-answer checks and answer-quality scores._", ""]

    unknown = Counter(h for r in rows for h in r["_unknown"])
    (args.run_dir / "unknown_domains.txt").write_text(
        "\n".join(f"{n}\t{h}" for h, n in unknown.most_common()) + "\n", encoding="utf-8")
    out += ["## Data quality", "",
            f"- {len(unknown)} sites seen in the runs are not in `domains.csv`; the most frequent are "
            "listed in `unknown_domains.txt`. A high unclassified share weakens the source metrics.",
            f"- Failed runs: {', '.join(r['stem'] for r in failed) or 'none'}.", ""]

    fields = [k for k in rows[0] if not k.startswith("_")]
    extra = sorted({k for r in rows for k in r if not k.startswith("_")} - set(fields))
    with (args.run_dir / "runs.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields + extra, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    (args.run_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (args.run_dir / "report.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
