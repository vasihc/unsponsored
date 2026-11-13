# Benchmark report

Run directory: `iter2`. 56 usable runs, 0 failed, 56 judged. Arms: baseline, skill.

Skill version (sha256 of SKILL.md): `874816399362`. Isolation: config-dir. Runs per prompt per arm: 1.

Skill was loaded in 100% of `skill` runs (28/28).

## Headline comparison

Each prompt counts once (its runs are averaged first). The difference is paired by prompt, with a bootstrap 95% interval over prompts. An interval that includes zero means the data does not show a difference.

### skill vs baseline

| Metric | baseline | skill | Difference | 95% interval | Prompts |
|---|---|---|---|---|---|
| Answers citing an independent test body | 39% | 86% | +46 pts | +29 pts to +64 pts | 28 |
| ...and that source was actually retrieved in the run | 39% | 86% | +46 pts | +29 pts to +64 pts | 28 |
| Answers citing a regulator or recall database | 18% | 71% | +54 pts | +36 pts to +71 pts | 28 |
| Share of cited sites: independent tests | 21% | 29% | +8 pts | +2 pts to +15 pts | 19 |
| Share of cited sites: regulators | 6% | 15% | +8 pts | +1 pts to +14 pts | 19 |
| Share of cited sites: affiliate-funded editorial | 7% | 9% | +3 pts | -6 pts to +11 pts | 19 |
| Share of cited sites: retailers | 14% | 8% | -6 pts | -14 pts to +2 pts | 19 |
| Share of cited sites: manufacturers | 10% | 6% | -4 pts | -10 pts to +1 pts | 19 |
| Share of cited sites: forums and social | 2% | 1% | -1 pts | -3 pts to +0 pts | 19 |
| Share of cited sites: news media | 7% | 12% | +5 pts | -2 pts to +12 pts | 19 |
| Share of cited sites: unclassified | 33% | 21% | -12 pts | -28 pts to +3 pts | 19 |
| Share of opened pages: independent tests | 48% | 51% | +3 pts | -10 pts to +21 pts | 9 |
| Share of opened pages: affiliate-funded editorial | 22% | 9% | -13 pts | -31 pts to +0 pts | 9 |
| Share of searches aimed at tests, recalls or problems | 48% | 82% | +34 pts | +24 pts to +45 pts | 19 |
| Sites cited per answer | 4.14 | 7.75 | +3.61 | +2.25 to +5.14 | 28 |
| Web searches per run | 2.32 | 6.43 | +4.11 | +3.04 to +5.29 | 28 |
| Pages opened per run | 0.82 | 2.36 | +1.54 | +0.96 to +2.07 | 28 |
| Answer length, words | 332.14 | 408.21 | +76.07 | +53.57 to +100.54 | 28 |
| Cost per run, USD (Claude Code estimate) | 0.26 | 0.58 | +0.31 | +0.25 to +0.37 | 28 |
| Time per run, seconds | 30.09 | 50.61 | +20.52 | +14.62 to +27.13 | 28 |
| Answers that commit to a recommendation | 100% | 100% | +0 pts | +0 pts to +0 pts | 28 |
| Provenance score (0-2) | 1.46 | 2.00 | +0.54 | +0.25 to +0.82 | 28 |
| Negatives score (0-2) | 1.36 | 2.00 | +0.64 | +0.43 to +0.86 | 28 |
| Answers that say what could not be verified | 96% | 100% | +4 pts | +0 pts to +11 pts | 28 |
| Answers breaking a stated constraint | 0% | 4% | +4 pts | +0 pts to +11 pts | 28 |

## Known-answer checks

Trap prompts ask about a product with a documented recall or failed test. Control prompts ask about a product that passed the same test.

| Check | baseline | skill |
|---|---|---|
| Trap: problem reported | 5/8 (62%) | 8/8 (100%) |
| Control: good test result reported | 4/4 (100%) | 4/4 (100%) |
| Control: false alarm raised | 0/4 (0%) | 0/4 (0%) |

## Do the recommendations change?

Agreement is the chance that two runs of the same prompt name the same top pick. Agreement between arms should be read against agreement within an arm, which is the noise level.

- `baseline`: within-arm agreement n/a, 19 distinct top-pick brands, top three brands take 27% of top picks.
- `skill`: within-arm agreement n/a, 18 distinct top-pick brands, top three brands take 27% of top picks.
- `skill` vs `baseline`: agreement 47%.

## Data quality

- 686 sites seen in the runs are not in `domains.csv`; the most frequent are listed in `unknown_domains.txt`. A high unclassified share weakens the source metrics.
- Failed runs: none.
