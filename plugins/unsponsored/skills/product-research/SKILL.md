---
name: product-research
description: Research a purchase and recommend products from evidence whose commercial incentives are known, instead of repeating affiliate "best of" lists and brand marketing. Use this whenever the user asks what to buy, which product, brand or model is best, whether a specific product is good, safe or worth the money, to compare products, or for a shortlist or gift idea (strollers, car seats, appliances, electronics, anything), even if they only say "recommend me a..." or "is X any good?". Also use it when the user quotes a review site, a ranking, star ratings or an influencer and asks whether to trust it.
---

# Product research

## Why this exists

When someone asks an assistant what to buy, the easy answer is whatever the web says most loudly. That is a poor proxy for quality. Most "best X of the year" pages earn a commission on every product they list, brands write content meant to be picked up by AI answers, and well-marketed products are over-represented in what a model remembers from training. An answer assembled from those sources looks balanced and is mostly advertising.

The fix is not to distrust everything. It is to know, for each claim, who is making it and what they gain, and to weight it accordingly. A lab that buys products anonymously and publishes failures is evidence. A ranking with a "buy" button next to every entry is a lead to check, not evidence.

## How to work

### 1. Pin down what the person needs

Recommendations depend on budget, country, and how the thing will be used. Country matters more than it seems: models, prices, safety standards and recalls differ between markets, and some products legal in one are not legal in another (child car seats are the classic case).

If something that would change the answer is missing, do not stall. State the assumption you are making ("assuming you are in the EU and want to stay under about EUR 400") and continue, so the person gets a usable answer in one turn and can correct you. Ask first only when no sensible assumption exists.

### 2. Look for tests, not for "best"

Searching "best stroller 2026" returns the pages built to win that search. Search instead for evidence by name: the product category plus the independent test bodies that cover it, in the language of the user's market ("Kinderwagen Test Stiftung Warentest", "infant car seat crash test ADAC", "stroller ratings Consumer Reports"). Then search each candidate model by its exact name.

Weigh what you find by the source's incentive:

| Tier | Who | What it is good for | Caveat |
|---|---|---|---|
| 1 | Independent test organisations that buy products themselves and take no money from manufacturers | Rankings, measured performance, failures | Often paywalled; test results are per model and per year |
| 2 | Regulators and recall databases | Recalls, safety warnings, legal requirements | Tells you what is dangerous, not what is good |
| 3 | Editorial reviewers who test hands-on but earn affiliate commission | Practical detail: fold, weight, fit, day-to-day annoyances | The ranking order and the choice of what to include are commercially shaped. Use the observations, not the verdict |
| 4 | Owners: forums, long-term reports, complaint databases | Failure patterns that only show after months | Individual posts prove little; look for the same fault reported independently. Reviews on retail listings are easy to fake |
| 5 | Manufacturers and retailers | Specifications, dimensions, price, availability | Nothing they say about quality counts as evidence |

Signs a page belongs in tier 3 or lower whatever it calls itself: an affiliate disclosure, purchase buttons beside each product, links carrying tracking tags, every product being "best for" something, no losers, no description of how anything was tested.

Popularity is not evidence either. A product you have "heard of" a lot is one that was written about a lot.

### 3. Look for what is wrong with it

Marketing never volunteers the bad news, so go and get it. For each product you are about to recommend, and for any product the user says they are considering, search its exact model name together with "recall", "safety warning", and the local equivalents, and check the relevant recall database. For anything a child's safety depends on, or anything that can burn, tip, or fail in a crash, treat this step as required rather than optional.

Report what you find precisely. A recall usually covers certain production dates or a specific combination of parts; say which, say what the remedy is, and do not turn "units made in 2025 were recalled" into "this product is unsafe". Equally, do not leave it out because the product is otherwise well reviewed.

Model names and line-ups change every year. Check that what you recommend is the current model and is actually sold in the user's country, rather than trusting memory.

### Know when to stop searching

The person is waiting, and every extra search costs them time. You have enough when each product you will name has (a) the best independent evidence available for it, or a clear finding that none exists, and (b) a recall check on its exact name. That usually takes four to six searches and a couple of opened pages. Do not keep re-wording a search to get behind a paywall or to confirm a detail that would not change the recommendation; note it under what you could not verify and move on.

### 4. Check the answer against the constraints

Before writing, confirm each recommended product fits the stated budget, is available and legal where the user lives, and suits the stated use (age, weight, vehicle, space). Recommendations that quietly ignore a constraint are the most common way these answers go wrong. The top pick has to fit the budget as stated; something better that costs more can be mentioned as an alternative, labelled as over budget.

### 5. Write the answer

Lead with the recommendation. People asked what to buy; caution is not a substitute for an answer. Then show the basis.

Keep it to roughly 250 to 350 words, short enough to read on a phone. The research can be thorough; the answer reports only what bears on the decision. One line per piece of evidence, at most two alternatives, and only the two or three gaps that matter. A simple yes-or-no question about one product deserves a shorter answer still.

Use this shape, adapting the labels to the user's language:

```
**Recommendation**: top pick and why, in one or two sentences. One or two alternatives and who each suits better.

**What this is based on**: the evidence behind each pick, each item naming its source and what kind of source it is (independent test, regulator, affiliate-funded review, owner reports, manufacturer).

**Known problems**: recalls, failed tests, recurring complaints for the products named. Say "none found" only if you actually looked, and say where.

**What I could not verify**: gaps, paywalled results you saw only second-hand, anything resting on weak sources.
```

A few rules of honesty that matter more than the format:

- Never state a test result you did not find. If you saw it reported second-hand, say "reported by <site> as...".
- If no independent test exists for a category, say so plainly. Then give the best answer the weaker evidence supports and label it as that.
- If the user's leading candidate has a problem, say it first, before alternatives.
- If the user is leaning on a ranking, star rating or influencer, say what that source is paid for and what it would take to trust it. Do not just agree or disagree with its conclusion.

### If you cannot search the web

Say that the answer comes from training data, which is dated and tilts toward heavily marketed products, and that recalls or new test results may be missing. Give your best shortlist anyway, and tell the person exactly which two or three checks to run themselves (the test body for their country, the recall database, the exact model name).

## Sources for baby and child gear

This is the first category with a curated list. For other categories apply the same tiers and find the equivalents.

**Independent testers (tier 1)**

- Germany, Austria, Switzerland: Stiftung Warentest (test.de); ADAC child seat tests, run jointly with ÖAMTC and TCS, published twice a year
- UK: Which?
- USA: Consumer Reports; IIHS booster seat ratings; NHTSA ease-of-use ratings for car seats
- Netherlands: Consumentenbond. Belgium: Test-Achats / Test-Aankoop. France: UFC-Que Choisir. Spain: OCU. Italy: Altroconsumo. Portugal: DECO Proteste. Denmark: Forbrugerrådet Tænk. Sweden: Råd & Rön
- Australia: Choice
- Rear-facing car seats: the Swedish Plus Test

European child seats are approved under UN R129 (i-Size) or the older R44; US seats under FMVSS 213. Seats are not interchangeable between the two markets, so a US test result says nothing about a seat sold in Europe under the same brand, and the reverse.

**Recalls and safety warnings (tier 2)**

- USA: cpsc.gov and saferproducts.gov for products; nhtsa.gov/recalls for car seats
- EU: Safety Gate (ec.europa.eu/safety-gate-alerts)
- UK: Product Safety Alerts, Reports and Recalls on gov.uk
- Canada: recalls-rappels.canada.ca. Australia: productsafety.gov.au
- Safe sleep guidance: the American Academy of Pediatrics (healthychildren.org), NHS, The Lullaby Trust. Anything marketed for infant sleep that is inclined, padded or not a flat firm surface deserves a check against this guidance regardless of its reviews.
