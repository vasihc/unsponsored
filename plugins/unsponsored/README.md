# unsponsored

A Claude skill for purchase research. When you ask what to buy, whether a product is any good, or which of two models to pick, Claude weighs each source by who pays for it: independent test organisations and recall databases first, affiliate-funded rankings and brand marketing last. It also looks for recalls and failed tests on the exact model before recommending it, and tells you what it could not verify.

## Install

```
/plugin install unsponsored --marketplace vasihc/unsponsored
```

## Use

No setup. Ask a shopping question the way you normally would:

- "Which infant car seat should I buy? We're in Germany, budget 400 euros."
- "Is the <brand> <model> a good choice?"
- "A top-10 list says X is the best stroller. Should I trust it?"

To call it explicitly: `/unsponsored:product-research <your question>`.

The skill needs web search to be useful. Without it, Claude says so and tells you which checks to run yourself.

## Scope

The method applies to any product. Version 0.1 ships a curated source list for baby and child gear only.

## Does it work?

The repository includes a benchmark that runs the same questions with and without the skill and compares the sources used and the answers given. See `bench/METHODOLOGY.md` in the repository root.
