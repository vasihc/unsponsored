# Benchmark report

Run directory: `20261113-141657`. 240 usable runs, 0 failed, 240 judged. Arms: baseline, skill.

Skill version (sha256 of SKILL.md): `874816399362`. Isolation: config-dir. Runs per prompt per arm: 3.

Skill was loaded in 100% of `skill` runs (120/120).

## Headline comparison

Each prompt counts once (its runs are averaged first). The difference is paired by prompt, with a bootstrap 95% interval over prompts. An interval that includes zero means the data does not show a difference.

### skill vs baseline

| Metric | baseline | skill | Difference | 95% interval | Prompts |
|---|---|---|---|---|---|
| Answers citing an independent test body | 22% | 87% | +64 pts | +50 pts to +77 pts | 40 |
| ...and that source was actually retrieved in the run | 22% | 87% | +64 pts | +50 pts to +77 pts | 40 |
| Answers citing a regulator or recall database | 1% | 71% | +70 pts | +57 pts to +82 pts | 40 |
| Share of cited sites: independent tests | 43% | 49% | +7 pts | -4 pts to +18 pts | 13 |
| Share of cited sites: regulators | 1% | 12% | +11 pts | +4 pts to +19 pts | 13 |
| Share of cited sites: affiliate-funded editorial | 4% | 6% | +2 pts | -1 pts to +6 pts | 13 |
| Share of cited sites: retailers | 11% | 7% | -3 pts | -12 pts to +6 pts | 13 |
| Share of cited sites: manufacturers | 14% | 8% | -6 pts | -11 pts to -1 pts | 13 |
| Share of cited sites: forums and social | 5% | 1% | -4 pts | -7 pts to -1 pts | 13 |
| Share of cited sites: news media | 10% | 8% | -2 pts | -9 pts to +4 pts | 13 |
| Share of cited sites: unclassified | 14% | 8% | -5 pts | -16 pts to +4 pts | 13 |
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

| Check | baseline | skill |
|---|---|---|
| Trap: problem reported | 13/24 (54%) | 24/24 (100%) |
| Control: good test result reported | 12/12 (100%) | 12/12 (100%) |
| Control: false alarm raised | 0/12 (0%) | 0/12 (0%) |

## Do the recommendations change?

Agreement is the chance that two runs of the same prompt name the same top pick. Agreement between arms should be read against agreement within an arm, which is the noise level.

- `baseline`: within-arm agreement 59%, 34 distinct top-pick brands, top three brands take 25% of top picks.
- `skill`: within-arm agreement 55%, 37 distinct top-pick brands, top three brands take 24% of top picks.
- `skill` vs `baseline`: agreement 34%.

## Data quality

- 1314 sites seen in the runs are not in `domains.csv`; the most frequent are listed in `unknown_domains.txt`. A high unclassified share weakens the source metrics.
- Failed runs: none.
