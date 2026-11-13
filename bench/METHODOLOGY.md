# Benchmark methodology

## Question

Does installing the skill change which sources Claude relies on and what it tells the user, compared with the same Claude without the skill?

The benchmark does not try to prove that one recommended product is better than another. Except for the known-answer checks below, there is no ground truth for "the best stroller".

## Design

- **Prompts**: 40 shopping questions about baby and child gear (`prompts.jsonl`), 18 set in Europe, 19 in the US, 3 with no country.
- **Arms**: `baseline` (plain Claude Code) and `skill` (same, with the plugin loaded; Claude decides by itself whether to use the skill). An optional third arm, `skill-forced`, invokes the skill explicitly, which separates "does the skill trigger" from "does the skill help once it runs".
- **Repetitions**: 3 runs per prompt per arm by default, because answers and search results vary between runs.
- **Order**: all runs are shuffled, so both arms are spread over the same period. Search results drift during a long run.
- **Unit of analysis**: the prompt. Runs of a prompt are averaged first, then arms are compared prompt by prompt, with a bootstrap 95% interval over prompts.

### Prompt types

| Type | Count | What it tests |
|---|---|---|
| `open` | 12 | "What should I buy" with budget, country and use stated |
| `compare` | 6 | Two named models |
| `verify_trap` | 8 | The user is about to buy a product with a documented recall or failed test |
| `verify_control` | 4 | Same wording, but the product passed the same test |
| `leading` | 4 | The user cites a ranking, star rating or influencer |
| `underspecified` | 3 | No budget, country or use given |
| `no_data` | 3 | Categories where independent tests probably do not exist |

### Isolation

Each run is a separate `claude -p` process in an empty temporary directory with:

- a clean Claude Code configuration directory (`bench/.claude-clean`, set through `CLAUDE_CONFIG_DIR`), so the operator's own CLAUDE.md, skills, installed plugins, hooks and MCP servers are absent and both arms start from the same state
- `--plugin-dir` for the skill arms only
- web search, page fetching and (skill arms) the Skill tool allowed; shell, file writing and subagents blocked in both arms
- no session persistence, no Chrome integration

The clean directory has no login. On your own machine sign in once before the first run: `CLAUDE_CONFIG_DIR=bench/.claude-clean claude`, then `/login`.

`--safe-mode` is not used: it keeps a `--plugin-dir` plugin loaded but hides its skills, so the skill arm would silently run without the skill (observed on Claude Code 2.1.322).

`run.py` reads the session's start-up record and reports a setup problem if the baseline can see the skill, the plugin or its skill failed to load, web tools are missing, or an MCP server is connected. Run `--smoke` first.

`--isolation none` runs with your normal configuration and is not suitable for published results. Skills built into Claude Code and organisation-managed settings are present in every mode, identically in both arms.

## Metrics

### From the transcript (no model involved)

Every site that appears in a run is classified by funding model using `domains.csv`: independent test body, regulator, affiliate-funded editorial, forum or social, retailer, manufacturer, news media, or unclassified. Each site counts once per run.

- Share of **cited** sites (links in the final answer) in each class
- Share of **opened** pages in each class
- Whether the answer cites an independent test body, and whether that site was actually retrieved in the run. The second number guards against test results quoted from memory.
- Share of searches aimed at tests, recalls or problems (keyword match on the query)
- Cost side: searches, pages opened, answer length, time, cost estimate

### From the judge (a second model, blind to the arm)

`judge.py` gives a model the user's request and the final answer and asks for a fixed set of fields: whether the answer commits to a recommendation, the top pick, whether sources are characterised (0-2), whether specific problems are reported (0-2), whether gaps are admitted, and whether a stated constraint is broken.

"Commits to a recommendation" is there on purpose. A skill that hedges everything would score well on caution and be useless.

### Known-answer checks

For trap prompts the judge is given the documented fact (for example: this seat failed the ADAC test published on 20 October 2026 and is under recall) and reports whether the answer mentions it. For control prompts it reports whether the answer mentions the good result, and whether it raises a false alarm.

These are the only metrics with a right answer, and the ones to lead with. All trap facts date from 2026 and most from its second half, so a model is unlikely to know them from training and has to find them by searching.

### Do recommendations change?

Agreement on the top pick between arms is compared with agreement within an arm. If two baseline runs agree with each other 40% of the time, 40% agreement between arms means no change.

## Limitations

- **One category, one language.** Baby gear, English prompts. Results say nothing about electronics or about questions asked in German.
- **Controls are narrow.** All four are car seats from one ADAC test.
- **Trap facts need re-checking before publication.** The two ADAC traps were read from adac.de and the Britax US recall from a news report citing NHTSA campaign 26C006. The other five were taken from a single Consumer Reports recall roundup on 12 November 2026 and should be confirmed on cpsc.gov or nhtsa.gov. Recalls have scope (production dates, part numbers); a correct answer may say the unit on sale today is unaffected.
- **`domains.csv` is a first draft.** Classifications come from general knowledge of each site's business model and were not verified site by site. `analyze.py` writes `unknown_domains.txt` after each run; a high unclassified share weakens the source metrics.
- **The judge is not fully blind.** The skill prescribes an answer layout, which a judge can recognise. Transcript metrics and known-answer checks do not have this problem.
- **The judge does not check facts.** An answer that invents a test result would score well on provenance. The "actually retrieved" metric catches part of this, not all.
- **Citing better sources is not the same as being right.** The source metrics show a change in what the answer rests on, not in the quality of the product recommended.
- **Search is not reproducible.** Re-running next month will give different numbers. Publish the transcripts, the date, the model and the Claude Code version (all recorded in `manifest.json` and the `.meta.json` files).
- **Small sample.** With 40 prompts, expect wide intervals on anything but large effects, and wider still within one prompt type.

## Before publishing results

1. Re-verify every trap and control fact against the primary source.
2. Review `domains.csv` and classify the frequent entries in `unknown_domains.txt`.
3. Read a sample of transcripts from both arms by hand, including failures.
4. Report the cost-side metrics next to the quality ones.
5. Freeze the skill (the report records its hash) and do not tune it on the same prompts you report. Keep a held-out set.
