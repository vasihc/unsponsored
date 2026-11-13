# Preliminary results

Two rounds on 12 November 2026, Claude Code 2.1.322, model `claude-fable-5-2`, run in a cloud workspace (not a stock desktop install). 28 of the 40 prompts, **one run per prompt per arm**. Treat everything here as a pilot: it shows the harness works and where to look, not how large the effect is.

Round 2 re-ran only the skill arm with a revised skill (shorter answers, a stopping rule for searching) and reuses the round 1 baseline transcripts.

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

What this does and does not show:

- The baseline is not naive. It found both ADAC failures and all three US car seat recalls by itself. The three it missed were the baby monitor, the steriliser and the stroller adapter, none of them car seats.
- 8 of 8 against 5 of 8 is three prompts. It needs the full set with three runs before it is a number.
- The skill costs roughly twice the time and money per answer.
- The split of cited sites by funding model is not reliable yet: a third to a half of sites were unclassified in round 1 (see `unknown_domains.txt` in each run folder).
- No transcript has been read by hand except a few spot checks.

Full tables: `runs/iter1/report.md`, `runs/iter2/report.md`. Raw transcripts are not in the repository yet; they will be published with the full run, after review.
