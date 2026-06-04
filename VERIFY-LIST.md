# VERIFY-LIST.md
## Facts that must be checked before publishing or updating

Every item marked [VERIFY] in `src/data/platforms.ts` is aggregated here.
Items are prioritized: TOP PRIORITY must be resolved before those pages go live.

---

## ⚠️ TOP PRIORITY

### POLYMARKET — US eligibility status (UNVERIFIED)
- **Field:** `platforms.polymarket.eligibility.usStatus`
- **Issue:** The site previously stated "not available to US persons." A review claims this changed with a CFTC authorization in November 2025. This has NOT been independently confirmed.
- **Risk:** If we assert US availability without confirmation, we could mislead US readers into using a platform they are not legally permitted to trade on. If we assert unavailability after a confirmed change, we lose US traffic and give wrong guidance.
- **What to check:**
  1. Search CFTC website (cftc.gov) for any no-action letter, DCM designation, or enforcement action referencing "Polymarket" dated 2025.
  2. Check Polymarket's own Terms of Service (polymarket.com/terms) for any updated language on US user eligibility.
  3. Check reliable financial news sources (Bloomberg, Reuters, WSJ) for a dated article confirming the regulatory change.
  4. If you find a primary source (CFTC document or Polymarket TOS update), note the exact URL and date.
- **Current state in code:** Set to a VERIFY placeholder — page renders the placeholder text. Do NOT remove the placeholder until this is confirmed.
- **Source to check:** https://www.cftc.gov (search "Polymarket") + https://polymarket.com/terms
- **Urgency:** Before publishing any content that addresses Polymarket's US availability.

---

## HIGH PRIORITY — Specific numbers (fees, minimums)

### KALSHI
| Field | What to check | Check URL |
|-------|---------------|-----------|
| `fees` | Taker fee % per contract; any maker rebate | https://kalshi.com/fees |
| `minDeposit` | Minimum USD deposit amount | https://kalshi.com/help |
| `withdrawalMethods` | Current withdrawal options (ACH, wire, debit?) | https://kalshi.com/help |
| `mobileApp.notes` | iOS App Store link + Android Play Store link + ratings | App Store / Play Store |
| `affiliateNetwork` | Affiliate/partner program URL and terms | https://kalshi.com/partners |
| `promoNote` | Any active signup promo or bonus | https://kalshi.com |

### POLYMARKET
| Field | What to check | Check URL |
|-------|---------------|-----------|
| `fees` | Current maker/taker fee schedule | https://docs.polymarket.com |
| `minDeposit` | Minimum USDC deposit | https://polymarket.com |
| `withdrawalMethods` | Polygon USDC withdrawal options | https://polymarket.com/help |
| `mobileApp.notes` | iOS and Android app (was web-only / PWA) | https://polymarket.com |
| `affiliateNetwork` | Any referral or affiliate program | https://polymarket.com |

### CRYPTO.COM
| Field | What to check | Check URL |
|-------|---------------|-----------|
| `eligibility.regions` | Country list for Predict product specifically | https://crypto.com/predict |
| `eligibility.usStatus` | US availability for the Predict product | https://crypto.com/predict |
| `fees` | Trading fee for Predict markets | https://crypto.com/predict |
| `fundingMethods` | Deposit methods for Predict | https://crypto.com/predict |
| `currency` | Settlement currency | https://crypto.com/predict |
| `affiliateNetwork` | Affiliate program terms and commission | https://crypto.com/en/affiliate |

---

## MEDIUM PRIORITY — New platform stubs

### ROBINHOOD
| Field | What to check | Check URL |
|-------|---------------|-----------|
| `eligibility.usStatus` | State-level restrictions for event contracts | https://robinhood.com/legal |
| `regulation` | CFTC registration status for event contracts | https://www.cftc.gov + https://robinhood.com/legal |
| `fees` | Fee structure for event contracts | https://robinhood.com/legal/fee-schedule |
| `minDeposit` | Minimum trade size for event contracts | https://robinhood.com |
| `fundingMethods` | Current deposit methods | https://robinhood.com/help |
| `mobileApp.notes` | Event contracts in iOS + Android app | App Store |
| `affiliateNetwork` | Affiliate program — likely Impact Radius | https://impact.com (search Robinhood) |
| `promoNote` | Any active signup promo | https://robinhood.com |

### PREDICTIT — CRITICAL OPERATIONAL STATUS
| Field | What to check | Check URL |
|-------|---------------|-----------|
| `eligibility.usStatus` | Current legal/operational status post-2022 CFTC dispute | https://predictit.org + cftc.gov |
| `regulation` | Current authorization basis (court order? new no-action letter?) | https://www.cftc.gov |
| `fees` | Current trading fee (was 2%) + withdrawal fee (was 5%) | https://predictit.org/legal/feestructure |
| `minDeposit` | Current minimum deposit | https://predictit.org |
| `mobileApp.notes` | App availability | https://predictit.org |

### COINBASE
| Field | What to check | Check URL |
|-------|---------------|-----------|
| `skipIf` field | FIRST: confirm what prediction market / event contract product Coinbase actually offers | https://coinbase.com |
| `eligibility.usStatus` | US availability for the specific product | https://help.coinbase.com |
| `regulation` | CFTC status for prediction/event contract product | https://www.cftc.gov |
| `fees` | Fee schedule for the specific product | https://coinbase.com/advanced-trade/fees |
| `affiliateNetwork` | Affiliate program — check Impact Radius | https://www.coinbase.com/affiliate-program |

### DRAFTKINGS
| Field | What to check | Check URL |
|-------|---------------|-----------|
| `eligibility.usStatus` | Current list of legal states | https://draftkings.com/help/us-state-by-state-regulations |
| `regulation` | CFTC registration for event contracts (separate from sportsbook) | https://www.cftc.gov |
| `fees` | Vig / fee structure for event contracts | https://draftkings.com/help |
| `minDeposit` | Minimum deposit amount | https://draftkings.com/help |
| `affiliateNetwork` | DraftKings affiliate program terms | https://draftkings.com/affiliates |
| `promoNote` | Current new-user promo (changes frequently — do not hardcode) | https://draftkings.com/promo |

### MANIFOLD
| Field | What to check | Check URL |
|-------|---------------|-----------|
| `mobileApp.notes` | iOS / Android app or PWA availability | https://manifold.markets |

---

## LOWER PRIORITY — When you apply for affiliate programs

| Platform | What to confirm | Where |
|----------|-----------------|-------|
| Kalshi | Affiliate commission rate (CPA / RevShare / Hybrid) | After applying to program |
| Polymarket | Whether affiliate program exists + terms | After applying |
| Crypto.com | Commission rate and cookie window | https://crypto.com/en/affiliate |
| Robinhood | Impact Radius program terms | https://impact.com |
| DraftKings | Commission rate and conditions | https://draftkings.com/affiliates |
| Coinbase | Impact Radius program terms | https://www.coinbase.com/affiliate-program |

Once affiliate links are approved:
1. Update `affiliateUrl` in `src/data/platforms.ts` for that platform
2. The `Cta.astro` and `AffiliateCTA.astro` components will automatically display "we may earn a commission" instead of "affiliate link coming soon"

---

## CONTENT VERIFY NOTES

### "best-prediction-markets-2026" roundup page
- The Polymarket eligibility VERIFY block will render verbatim as a callout — once you resolve the US status, update `platforms.ts` and the callout will update automatically.
- DraftKings promo section: never hardcode a promo code. The `showPromo={true}` prop renders "check official site" when `promoCode` is null (which it is).

### "risks-and-responsible-trading" page
- Problem gambling helpline numbers are current as of writing. Verify periodically.
- CFTC link on Kalshi fund protection: add a direct CFTC source link once you identify the relevant rule section.

---

## HOW TO UPDATE A VERIFIED FACT

1. Open `src/data/platforms.ts`
2. Find the platform and field
3. Replace the `V(...)` string with the real value and a source comment
4. If the fact is eligibility-related, also update `eligibility.lastUpdated` to today's date
5. Run `npm run build` to verify no errors
6. Add a note in this file: "Verified on [date] — source: [url]"
7. Commit and push
