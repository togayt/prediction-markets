# Event Page Checklist — Shipping a Timely Page Before It Peaks

Prediction market event pages have a short traffic window. The goal is to be
indexed and ranking **2-4 weeks before** the event peaks in search volume.
Use this checklist every time.

---

## Step 1: Identify the event early (T-4 weeks minimum)

- [ ] Check Google Trends for the event query — is there a rising slope?
- [ ] Check Kalshi / Polymarket for existing markets on this event
- [ ] Confirm the event has a clear, binary-resolvable outcome (yes/no)
- [ ] Identify the target keyword (usually: "[event name] prediction market" or "[event name] odds")
- [ ] Check keyword difficulty — if it's dominated by ESPN/Bleacher Report, consider a longer-tail angle

**Decision gate:** If volume is too low or keyword difficulty too high, skip.

---

## Step 2: Create the page (T-3 to T-2 weeks)

- [ ] Copy `src/pages/events/_template.astro` to `src/pages/events/[event-slug].astro`
- [ ] Fill in all TODO fields in the CONFIGURATION block
- [ ] Write the lede — must directly answer "where can I trade on [event]?"
- [ ] Name at least 2-3 specific markets on Kalshi/Polymarket (with current prices)
- [ ] Write the resolution section — this is the highest-value part for readers
- [ ] Add 4-6 FAQs using the FAQSchema component
- [ ] Add affiliate CTAs via the `<Cta>` component for each available platform
- [ ] Run `npm run build` — verify no errors

---

## Step 3: Publish and accelerate indexing (T-2 weeks)

- [ ] Merge to main and push — Netlify deploys automatically
- [ ] Add the page URL to `src/pages/sitemap.xml.ts` routes array
- [ ] Submit URL directly in Google Search Console: URL Inspection > Request Indexing
- [ ] Add one internal link from the most relevant existing page (e.g. compare.astro or a blog post)
- [ ] Post about it once on X/Twitter with the event angle (not a pure promo — give value)
- [ ] If the event is US-relevant: post in r/predictionmarkets or r/Kalshi (only if genuinely useful)

---

## Step 4: Update during the event (T-0 to resolution)

- [ ] Update live prices/probabilities in the page body (at least 2-3 times as event approaches)
- [ ] Change `updatedDate` in the page config each time you update
- [ ] If odds move significantly, post a quick update on X/Twitter
- [ ] Monitor Search Console for impressions — if you rank position 8-20, try to improve the content

---

## Step 5: Post-event (T+1 to T+2 weeks)

- [ ] After the event resolves: add a "Result" section to the top of the page
- [ ] Note whether the prediction market was accurate vs. other forecasts
- [ ] Keep the page live — "2026 World Cup prediction market results" has search demand too
- [ ] Add a link to your next event page or the compare page to capture ongoing traffic

---

## Template quick-reference

```
File:     src/pages/events/[slug].astro   (copy from _template.astro)
URL:      /events/[slug]
Sitemap:  Add to src/pages/sitemap.xml.ts
Schema:   ArticleSchema + FAQSchema (both included in template)
CTAs:     <Cta> component wired to platforms array in config.ts
```

---

## Time-to-rank reality check

- Google typically crawls a new page within 24-72 hours after requesting indexing
- Ranking takes 1-3 weeks for low-competition queries, longer for competitive ones
- Event pages with specific market data (current prices, resolution criteria) outperform
  generic "can I bet on X" pages — that specificity is your edge over big media sites
