# Benchmark report

Run directory: `20261113-141657`. 276 usable runs, 0 failed, 276 judged. Arms: baseline, baseline-nudge, skill.

Skill version (sha256 of SKILL.md): `874816399362`. Isolation: config-dir. Runs per prompt per arm: 3.

Skill was loaded in 0% of `baseline-nudge` runs (0/36).
Skill was loaded in 100% of `skill` runs (120/120).

## Headline comparison

Each prompt counts once (its runs are averaged first). The difference is paired by prompt, with a bootstrap 95% interval over prompts. An interval that includes zero means the data does not show a difference.

### baseline-nudge vs baseline

| Metric | baseline | baseline-nudge | Difference | 95% interval | Prompts |
|---|---|---|---|---|---|
| Runs that searched the web at all | 78% | 100% | +22 pts | +0 pts to +47 pts | 12 |
| Answers citing an independent test body | 58% | 92% | +33 pts | +11 pts to +58 pts | 12 |
| ...and that source was actually retrieved in the run | 58% | 92% | +33 pts | +11 pts to +58 pts | 12 |
| Answers citing a regulator or recall database | 3% | 64% | +61 pts | +36 pts to +83 pts | 12 |
| Share of cited sites: independent tests | 42% | 32% | -10 pts | -20 pts to +1 pts | 10 |
| Share of cited sites: regulators | 1% | 15% | +14 pts | +6 pts to +25 pts | 10 |
| Share of cited sites: affiliate-funded editorial | 5% | 5% | +0 pts | -7 pts to +8 pts | 10 |
| Share of cited sites: retailers | 16% | 8% | -8 pts | -19 pts to +3 pts | 10 |
| Share of cited sites: manufacturers | 14% | 9% | -5 pts | -10 pts to +0 pts | 10 |
| Share of cited sites: forums and social | 3% | 1% | -2 pts | -4 pts to -1 pts | 10 |
| Share of cited sites: news media | 13% | 13% | +1 pts | -8 pts to +8 pts | 10 |
| Share of cited sites: unclassified | 7% | 17% | +10 pts | +2 pts to +19 pts | 10 |
| Share of opened pages: independent tests | 70% | 56% | -13 pts | -33 pts to +8 pts | 7 |
| Share of opened pages: affiliate-funded editorial | 7% | 0% | -7 pts | -21 pts to +0 pts | 7 |
| Share of searches aimed at tests, recalls or problems | 55% | 83% | +28 pts | +19 pts to +41 pts | 10 |
| Sites cited per answer | 3.47 | 5.92 | +2.44 | +1.58 to +3.31 | 12 |
| Web searches per run | 2.17 | 3.64 | +1.47 | +1.08 to +1.92 | 12 |
| Pages opened per run | 1.11 | 1.56 | +0.44 | -0.03 to +0.89 | 12 |
| Answer length, words | 355.25 | 369.47 | +14.22 | -10.14 to +41.03 | 12 |
| Cost per run, USD (Claude Code estimate) | 0.41 | 0.48 | +0.07 | +0.04 to +0.11 | 12 |
| Time per run, seconds | 34.39 | 36.18 | +1.79 | -2.30 to +6.68 | 12 |
| Answers that commit to a recommendation | 100% | 100% | +0 pts | +0 pts to +0 pts | 12 |
| Provenance score (0-2) | 1.69 | 2.00 | +0.31 | +0.06 to +0.58 | 12 |
| Negatives score (0-2) | 1.61 | 2.00 | +0.39 | +0.17 to +0.64 | 12 |
| Answers that say what could not be verified | 94% | 92% | -3 pts | -19 pts to +14 pts | 12 |
| Answers breaking a stated constraint | 0% | 0% | +0 pts | +0 pts to +0 pts | 12 |

### skill vs baseline

| Metric | baseline | skill | Difference | 95% interval | Prompts |
|---|---|---|---|---|---|
| Runs that searched the web at all | 29% | 99% | +70 pts | +56 pts to +82 pts | 40 |
| Answers citing an independent test body | 22% | 87% | +64 pts | +50 pts to +77 pts | 40 |
| ...and that source was actually retrieved in the run | 22% | 87% | +64 pts | +50 pts to +77 pts | 40 |
| Answers citing a regulator or recall database | 1% | 72% | +71 pts | +59 pts to +82 pts | 40 |
| Share of cited sites: independent tests | 43% | 49% | +7 pts | -4 pts to +18 pts | 13 |
| Share of cited sites: regulators | 1% | 12% | +11 pts | +4 pts to +20 pts | 13 |
| Share of cited sites: affiliate-funded editorial | 4% | 6% | +2 pts | -1 pts to +6 pts | 13 |
| Share of cited sites: retailers | 13% | 7% | -6 pts | -17 pts to +4 pts | 13 |
| Share of cited sites: manufacturers | 14% | 8% | -6 pts | -11 pts to -1 pts | 13 |
| Share of cited sites: forums and social | 5% | 1% | -4 pts | -7 pts to -1 pts | 13 |
| Share of cited sites: news media | 12% | 9% | -3 pts | -10 pts to +4 pts | 13 |
| Share of cited sites: unclassified | 9% | 7% | -3 pts | -10 pts to +5 pts | 13 |
| Share of opened pages: independent tests | 71% | 80% | +9 pts | -4 pts to +22 pts | 9 |
| Share of opened pages: affiliate-funded editorial | 6% | 2% | -4 pts | -11 pts to +0 pts | 9 |
| Share of searches aimed at tests, recalls or problems | 52% | 87% | +36 pts | +27 pts to +46 pts | 13 |
| Sites cited per answer | 1.27 | 6.23 | +4.97 | +3.94 to +5.92 | 40 |
| Web searches per run | 0.95 | 7.03 | +6.08 | +5.17 to +6.93 | 40 |
| Pages opened per run | 0.40 | 2.89 | +2.49 | +1.96 to +3.04 | 40 |
| Answer length, words | 319.49 | 413.68 | +94.19 | +75.51 to +112.85 | 40 |
| Cost per run, USD (Claude Code estimate) | 0.31 | 0.77 | +0.46 | +0.40 to +0.52 | 40 |
| Time per run, seconds | 25.50 | 59.63 | +34.13 | +27.91 to +40.34 | 40 |
| Answers that commit to a recommendation | 100% | 100% | +0 pts | +0 pts to +0 pts | 40 |
| Provenance score (0-2) | 0.90 | 2.00 | +1.10 | +0.83 to +1.33 | 40 |
| Negatives score (0-2) | 1.21 | 1.98 | +0.78 | +0.63 to +0.90 | 40 |
| Answers that say what could not be verified | 94% | 100% | +6 pts | +1 pts to +12 pts | 40 |
| Answers breaking a stated constraint | 3% | 2% | -2 pts | -5 pts to +2 pts | 40 |

## Known-answer checks

Trap prompts ask about a product with a documented recall or failed test. Control prompts ask about a product that passed the same test.

| Check | baseline | baseline-nudge | skill |
|---|---|---|---|
| Trap: problem reported | 13/24 (54%) | 24/24 (100%) | 24/24 (100%) |
| Control: good test result reported | 12/12 (100%) | 12/12 (100%) | 12/12 (100%) |
| Control: false alarm raised | 0/12 (0%) | 0/12 (0%) | 0/12 (0%) |

## Do the recommendations change?

Agreement is the chance that two runs of the same prompt name the same top pick. Agreement between arms should be read against agreement within an arm, which is the noise level.

- `baseline`: within-arm agreement 59%, 34 distinct top-pick brands, top three brands take 25% of top picks.
- `baseline-nudge`: within-arm agreement 73%, 9 distinct top-pick brands, top three brands take 43% of top picks.
- `skill`: within-arm agreement 55%, 37 distinct top-pick brands, top three brands take 24% of top picks.
- `baseline-nudge` vs `baseline`: agreement 50%.
- `skill` vs `baseline`: agreement 34%.

## Data quality

- 1358 sites seen in the runs are not in `domains.csv`; the most frequent are listed in `unknown_domains.txt`. A high unclassified share weakens the source metrics.
- Failed runs: none.
