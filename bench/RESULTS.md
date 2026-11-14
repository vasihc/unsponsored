# Results

## Full run, 13–14 November 2026

All 40 prompts, **three runs per prompt per arm**, 240 runs, none failed, all judged. Model `claude-fable-5-2`. Claude Code 2.1.323 for 219 runs and 2.1.325 for the last 21 (retried after a rate limit). Run locally on macOS with an isolated config directory. The skill loaded in 120 of 120 skill runs.

Differences are paired by prompt, with a bootstrap 95% interval over prompts.

| | Baseline | Skill | Difference (95% interval) |
|---|---|---|---|
| Trap: recall or failed test reported | 13 of 24 | 24 of 24 | |
| Control: good test result reported | 12 of 12 | 12 of 12 | |
| Control: false alarm | 0 of 12 | 0 of 12 | |
| Answers citing an independent test body | 22% | 87% | +64 pts (+50 to +77) |
| Answers citing a regulator or recall database | 1% | 71% | +70 pts (+57 to +82) |
| Provenance score (0–2) | 0.90 | 2.00 | +1.10 (+0.83 to +1.33) |
| Negatives score (0–2) | 1.21 | 1.98 | +0.78 (+0.63 to +0.90) |
| Answers that say what could not be verified | 94% | 100% | +6 pts (+1 to +12) |
| Answers that commit to a recommendation | 100% | 100% | 0 |
| Web searches per run | 0.95 | 7.03 | +6.08 |
| Answer length, words | 319 | 414 | +94 |
| Time per run, seconds | 26 | 60 | +34 |
| Cost per run, USD (Claude Code estimate) | 0.31 | 0.77 | +0.46 |

What this shows:

- The baseline missed the recall in every run for three of the eight trap prompts: the Britax B-Safe car seat, the Baby Brezza steriliser and the Joolz stroller adapter. It caught the Babysense baby monitor recall in one run of three. The skill reported all eight in every run.
- In the pilot the baseline found the Britax recall; here it missed it three times out of three. One run per prompt was not enough to tell.
- No false alarms on the control prompts in either arm.
- The baseline rarely searches (under one search per run on average), so most of its answers rest on training data.
- The skill changes what gets recommended: two runs from different arms name the same top pick 34% of the time, against 55–59% for two runs from the same arm.
- The skill costs about 2.5 times the money and 2.3 times the time per answer.

Limits:

- Both arms loaded two organisation-synced plugins (`engineering`, `design`) into the isolated config directory. The arms are comparable with each other, but the baseline is not a stock Claude Code install.
- Source-share metrics remain weak: 1314 sites seen in the runs are not in `domains.csv`, and only 13 prompts have enough citations in both arms for that comparison. See `unknown_domains.txt` in the run folder, which is not committed.
- Answers were scored by a model judge. Only the trap answers described under "Review of the trap answers" were checked against the transcripts.

Full tables: `runs/20261113-141657/report.md`. Per-run data: `runs.csv`, `summary.json`. Raw transcripts and judgments are not in the repository.

### Review of the trap answers, 14 November 2026

The eleven baseline answers the judge marked as misses, and the first skill answer for four trap prompts, were read against the transcripts. The trap facts were checked against the primary sources (`FACTS.md`).

- **The judge's eleven "miss" verdicts are correct.** None of those answers mentions the recall.
- **In eight of the eleven the baseline did not search at all.** It answered from training data and said so. For the Britax seat all three answers say, in substance, "I'm not aware of a recall, but I haven't checked; look it up at nhtsa.gov". That is an honest answer that leaves the check to the user. It is not a made-up one.
- **In the other three (the Joolz adapter) it searched, but only for compatibility and dimensions**, never for recalls.
- **Across the whole run the baseline searched the web in 35 of 120 runs; the skill arm in 119 of 120.** By prompt type, the baseline searched in 16 of 24 trap runs, 12 of 12 control runs, 4 of 36 open "what should I buy" runs and none of the 30 leading, underspecified and no-data runs.
- **The four skill answers checked agree with the primary sources** on campaign numbers, unit counts and the nature of the defect. One detail was not confirmed: a serial-number prefix given for the Babysense monitor does not appear in the CPSC notice as read.
- **Four of the eight traps are weaker than the others**, because the recall may not cover the unit the user would buy today. See `FACTS.md`.

What follows for reading the headline: 24 of 24 against 13 of 24 measures mostly whether Claude Code searches and checks for recalls before answering. Whether one sentence of instruction would do the same is not yet measured; the `baseline-nudge` arm exists for that.

## Pilot, 12 November 2026

Two rounds, Claude Code 2.1.322, model `claude-fable-5-2`, cloud workspace. 28 of the 40 prompts, one run per prompt per arm. Round 2 re-ran only the skill arm with a revised skill (shorter answers, a stopping rule for searching) and reused the round 1 baseline transcripts.

| | Baseline | Skill, round 1 | Skill, round 2 |
|---|---|---|---|
| Trap: recall or failed test reported | 5 of 8 | 8 of 8 | 8 of 8 |
| Control: false alarm | 0 of 4 | 0 of 4 | 0 of 4 |
| Answers citing an independent test body | 39% | 93% | 86% |
| Answers citing a regulator or recall database | 18% | 71% | 71% |
| Web searches per run | 2.3 | 8.5 | 6.4 |
| Answer length, words | 332 | 515 | 408 |
| Time per run, seconds | 30 | 64 | 51 |
| Cost per run, USD (Claude Code estimate) | 0.26 | 0.70 | 0.58 |

Full tables: `runs/iter1/report.md`, `runs/iter2/report.md`.
