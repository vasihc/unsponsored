<img src="assets/icon-512.png" width="96" alt="">

# unsponsored

People increasingly ask AI assistants what to buy. The assistant searches the web, and the web's answer to "best stroller" is mostly pages that earn a commission on every product they list. This repository contains:

- **A Claude skill** (`plugins/unsponsored`) that makes Claude weigh sources by who pays them, look for recalls and failed tests, and say what it could not verify. It does not filter advertising out of the web; it tells you what each claim rests on.
- **A benchmark** (`bench/`) that measures whether the skill changes anything, by running the same questions through Claude Code with and without it.

Status: version 0.1. Two preliminary rounds have been run (28 prompts, one run per arm); see `bench/RESULTS.md`. They are too small to publish as findings.

## Install the skill

```bash
claude plugin marketplace add vasihc/unsponsored
claude plugin install unsponsored@unsponsored
```

Or try it for one session without installing:

```bash
claude --plugin-dir ./plugins/unsponsored
```

## Run the benchmark

Requires a recent Claude Code (the flags were checked against 2.1.322), signed in, and Python 3.9+. No Python packages are needed.

```bash
python3 bench/run.py --smoke            # 2 runs: checks that the setup is sound
python3 bench/run.py                    # 40 prompts x 2 arms x 3 runs = 240 runs
python3 bench/judge.py bench/runs/<dir> # scores the answers
python3 bench/analyze.py bench/runs/<dir>
```

The full run makes 240 agent sessions with web search plus 240 short judge calls, all on your Claude account. Start smaller, for example `--types verify_trap,verify_control --runs 2`.

What is measured, how, and what the numbers cannot tell you: [bench/METHODOLOGY.md](bench/METHODOLOGY.md).

## Layout

```
.claude-plugin/marketplace.json     marketplace listing
plugins/unsponsored/                 the plugin
  skills/product-research/SKILL.md  the skill itself
bench/
  prompts.jsonl                     40 benchmark questions
  domains.csv                       site classification by funding model
  run.py  judge.py  analyze.py      harness
  METHODOLOGY.md
  RESULTS.md                        pilot results
  runs/                             reports from each run
assets/                             icon
```

## License

MIT
