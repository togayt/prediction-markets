/**
 * SINGLE SOURCE OF TRUTH for all platform facts.
 *
 * RULE: Every factual claim uses the V() placeholder unless it is
 * self-reported by the platform's own public documentation and cited here.
 * Specific numbers (fees, minimums, commissions) always require V().
 *
 * V() format: [VERIFY: <what to check> | source: <url> | updated: <date>]
 */

export const V = (what: string, source: string, updated = "needs-check") =>
  `[VERIFY: ${what} | source: ${source} | updated: ${updated}]` as const;

// ─────────────────────────────────────────────────────────────────────────────

export interface MobileApp {
  ios: boolean | null;     // null = unconfirmed
  android: boolean | null;
  notes: string;
}

export interface Eligibility {
  regions: string;
  usStatus: string;        // use V() for contested / unverified status
  details: string;
  source: string;
  lastUpdated: string;
}

export interface PlatformData {
  id: string;
  name: string;
  slug: string;
  oneLiner: string;
  eligibility: Eligibility;
  regulation: string;
  fees: string;
  minDeposit: string;
  withdrawalMethods: string;
  fundingMethods: string;
  currency: string;
  mobileApp: MobileApp;
  affiliateUrl: string | null;
  affiliateNetwork: string | null;
  promoCode: string | null;    // null = never render a code; show controlled state
  promoNote: string | null;
  bestFor: string;
  skipIf: string;
  ease: "Easy" | "Medium" | "Advanced";
  notes: string;
  live: boolean;           // true = we have a published review page
  reviewPath: string | null;

  // ── Backward-compat aliases so existing pages don't break ─────────────────
  region: string;          // = eligibility.regions (short form)
  funding: string;         // = fundingMethods
  affiliate: boolean;      // = affiliateUrl !== null
}

// ─────────────────────────────────────────────────────────────────────────────
//  PLATFORM DATA
// ─────────────────────────────────────────────────────────────────────────────

export const platforms: PlatformData[] = [
  // ── KALSHI ────────────────────────────────────────────────────────────────
  {
    id: "kalshi",
    name: "Kalshi",
    slug: "kalshi",
    oneLiner: "The only CFTC-regulated prediction market exchange for US residents.",
    eligibility: {
      regions: "United States",
      usStatus: "Available — US residents only",
      details: "Must be a US resident, 18+. Not available outside the US.",
      source: "https://kalshi.com/legal/user-agreement",
      lastUpdated: "2025-01",
    },
    regulation: "CFTC-regulated (US) — designated contract market",
    fees: V(
      "taker fee per contract and any maker rebate — check current fee schedule",
      "https://kalshi.com/fees",
    ),
    minDeposit: V(
      "minimum deposit amount",
      "https://kalshi.com/help",
    ),
    withdrawalMethods: V(
      "available withdrawal methods (bank ACH, debit card, wire?)",
      "https://kalshi.com/help",
    ),
    fundingMethods: "USD: bank transfer / debit card",
    currency: "USD",
    mobileApp: {
      ios: true,
      android: true,
      notes: V(
        "confirm iOS App Store and Google Play availability and ratings",
        "https://apps.apple.com / https://play.google.com",
      ),
    },
    affiliateUrl: null,
    affiliateNetwork: V(
      "Kalshi affiliate / partner program — check for an affiliate portal",
      "https://kalshi.com/partners",
    ),
    promoCode: null,
    promoNote: V(
      "any active promo code or signup bonus",
      "https://kalshi.com",
    ),
    bestFor: "US residents who want a fully regulated, beginner-friendly experience with standard USD funding",
    skipIf: "You are outside the United States — Kalshi is US-only",
    ease: "Easy",
    notes: "The most beginner-friendly regulated option for US residents. Bank-account funding, no crypto required.",
    live: true,
    reviewPath: "/blog/kalshi-review",
    // compat
    region: "United States",
    funding: "USD: bank transfer / debit card",
    affiliate: false,
  },

  // ── POLYMARKET ────────────────────────────────────────────────────────────
  {
    id: "polymarket",
    name: "Polymarket",
    slug: "polymarket",
    oneLiner: "The largest prediction market by global trading volume, built on the Polygon blockchain.",
    eligibility: {
      regions: "Global",
      usStatus: V(
        "TOP PRIORITY — Polymarket was previously unavailable to US persons (offshore, no CFTC authorization). A claimed CFTC authorization as of Nov 2025 has been reported but not independently confirmed. Verify: (1) is there a CFTC no-action letter or DCM designation for Polymarket dated 2025? (2) has Polymarket updated its own terms-of-service to permit US users? Do NOT assert availability to US persons until both are confirmed with dated primary sources.",
        "https://polymarket.com/terms + https://www.cftc.gov (search 'Polymarket')",
        "UNVERIFIED — do not publish without checking",
      ),
      details: "Previously geo-blocked for US IPs. USDC / Polygon wallet required regardless of location.",
      source: "https://polymarket.com/terms",
      lastUpdated: "2025-01",
    },
    regulation: V(
      "regulatory status — offshore / unregulated historically; verify any 2025 CFTC authorization",
      "https://www.cftc.gov + https://polymarket.com/terms",
    ),
    fees: V(
      "trading fee percentage (historically low/zero; check current maker/taker schedule)",
      "https://docs.polymarket.com",
    ),
    minDeposit: V(
      "minimum USDC deposit amount",
      "https://polymarket.com",
    ),
    withdrawalMethods: V(
      "USDC withdrawal to Polygon wallet — confirm current options",
      "https://polymarket.com/help",
    ),
    fundingMethods: "USDC stablecoin (Polygon network)",
    currency: "USDC (Polygon)",
    mobileApp: {
      ios: null,
      android: null,
      notes: V(
        "native iOS / Android app availability (previously web-only / PWA)",
        "https://polymarket.com",
      ),
    },
    affiliateUrl: null,
    affiliateNetwork: V(
      "Polymarket referral or affiliate program",
      "https://polymarket.com",
    ),
    promoCode: null,
    promoNote: V(
      "any active promo code or signup bonus",
      "https://polymarket.com",
    ),
    bestFor: "Crypto-comfortable traders outside the US who want the widest market selection and highest liquidity",
    skipIf: "You are in the United States (verify current status before trading) or uncomfortable holding USDC on a blockchain wallet",
    ease: "Medium",
    notes: "Largest event selection and global brand recognition. Requires a crypto wallet and USDC on Polygon. US status must be verified before advising US readers.",
    live: true,
    reviewPath: "/blog/polymarket-review",
    // compat
    region: V("Global — US eligibility unconfirmed, see eligibility.usStatus", "https://polymarket.com/terms"),
    funding: "USDC stablecoin (Polygon network)",
    affiliate: false,
  },

  // ── CRYPTO.COM PREDICT ────────────────────────────────────────────────────
  {
    id: "crypto-com",
    name: "Crypto.com",
    slug: "crypto-com",
    oneLiner: "Prediction markets embedded in the Crypto.com exchange ecosystem.",
    eligibility: {
      regions: V(
        "list of supported countries for the Predict product specifically",
        "https://crypto.com/predict",
      ),
      usStatus: V(
        "whether the Predict product is available to US residents (Crypto.com has US regulatory presence but product availability varies)",
        "https://crypto.com/predict",
      ),
      details: "Availability varies significantly by country. Check the platform directly for your jurisdiction.",
      source: "https://crypto.com/predict",
      lastUpdated: "2025-01",
    },
    regulation: V(
      "specific regulatory licenses applicable to the Predict product",
      "https://crypto.com/en/legal",
    ),
    fees: V(
      "trading fee for Predict markets",
      "https://crypto.com/predict",
    ),
    minDeposit: V(
      "minimum deposit or trade size for Predict",
      "https://crypto.com/predict",
    ),
    withdrawalMethods: V(
      "withdrawal options from Crypto.com Predict",
      "https://crypto.com/help",
    ),
    fundingMethods: V(
      "funding methods for Predict (fiat, crypto, CRO?)",
      "https://crypto.com/predict",
    ),
    currency: V(
      "settlement currency for Predict markets",
      "https://crypto.com/predict",
    ),
    mobileApp: {
      ios: true,
      android: true,
      notes: "Predict is accessible within the main Crypto.com app",
    },
    affiliateUrl: null,
    affiliateNetwork: V(
      "Crypto.com affiliate program details and network",
      "https://crypto.com/en/affiliate",
    ),
    promoCode: null,
    promoNote: V(
      "any active Crypto.com Predict promo or bonus",
      "https://crypto.com/predict",
    ),
    bestFor: "Existing Crypto.com users who want prediction markets alongside their exchange account",
    skipIf: "You don't already use Crypto.com and don't want to onboard to a full crypto exchange just for prediction markets",
    ease: "Medium",
    notes: "Convenient if you already hold assets on Crypto.com. Verify availability in your country before signing up.",
    live: true,
    reviewPath: "/blog/crypto-com-predict-review",
    // compat
    region: V("varies by country — check crypto.com/predict for your jurisdiction", "https://crypto.com/predict"),
    funding: V("fiat and crypto options — check current deposit methods", "https://crypto.com/predict"),
    affiliate: false,
  },

  // ── ROBINHOOD ─────────────────────────────────────────────────────────────
  {
    id: "robinhood",
    name: "Robinhood",
    slug: "robinhood",
    oneLiner: "Mainstream US brokerage that added CFTC-regulated event contracts in 2024.",
    eligibility: {
      regions: "United States",
      usStatus: V(
        "confirm US-only availability and any state-level restrictions for event contracts specifically",
        "https://robinhood.com/legal",
        "2025",
      ),
      details: V(
        "age requirement and any state exclusions for event contract trading",
        "https://robinhood.com/legal",
      ),
      source: "https://robinhood.com/learn/articles/event-contracts",
      lastUpdated: "needs-check",
    },
    regulation: V(
      "CFTC registration status for Robinhood's event contracts product",
      "https://www.cftc.gov / https://robinhood.com/legal",
    ),
    fees: V(
      "fee structure for event contracts on Robinhood",
      "https://robinhood.com/legal/fee-schedule",
    ),
    minDeposit: V(
      "minimum deposit or trade size for event contracts",
      "https://robinhood.com",
    ),
    withdrawalMethods: V(
      "withdrawal methods from Robinhood",
      "https://robinhood.com/help",
    ),
    fundingMethods: V(
      "funding methods for Robinhood event contracts (ACH, wire, instant deposit?)",
      "https://robinhood.com/help",
    ),
    currency: "USD",
    mobileApp: {
      ios: true,
      android: true,
      notes: V(
        "confirm event contracts are accessible in the Robinhood mobile app (iOS + Android)",
        "https://apps.apple.com/app/robinhood",
      ),
    },
    affiliateUrl: null,
    affiliateNetwork: V(
      "Robinhood affiliate program — likely through Impact Radius",
      "https://impact.com (search Robinhood)",
    ),
    promoCode: null,
    promoNote: V(
      "any active Robinhood promo for new accounts or event contracts",
      "https://robinhood.com/us/en/support/articles/inviting-friends",
    ),
    bestFor: "US investors who already have a Robinhood account and want to try event contracts without a separate signup",
    skipIf: "You want the widest market selection or are not already a Robinhood user — dedicated platforms have more events",
    ease: "Easy",
    notes: "Lowest barrier to entry for existing Robinhood users. Event contract selection is narrower than dedicated platforms.",
    live: false,
    reviewPath: "/platforms/robinhood",
    // compat
    region: "United States",
    funding: V("ACH bank transfer, debit card — check current options", "https://robinhood.com/help"),
    affiliate: false,
  },

  // ── PREDICTIT ─────────────────────────────────────────────────────────────
  {
    id: "predictit",
    name: "PredictIt",
    slug: "predictit",
    oneLiner: "US political prediction markets originally authorized as an academic research project.",
    eligibility: {
      regions: "United States",
      usStatus: V(
        "CRITICAL — PredictIt's CFTC no-action letter was revoked Aug 2022; PredictIt obtained a court injunction allowing continued operation. Verify current legal/operational status before advising readers to sign up.",
        "https://www.cftc.gov / https://predictit.org",
        "UNVERIFIED — check before publishing",
      ),
      details: V(
        "current age requirement and any state restrictions",
        "https://predictit.org/legal",
      ),
      source: "https://predictit.org/legal",
      lastUpdated: "needs-check",
    },
    regulation: V(
      "current regulatory status — no-action letter revoked 2022; check whether a new authorization or court order is in place",
      "https://www.cftc.gov + https://predictit.org",
    ),
    fees: V(
      "PredictIt's 2% trading fee and 5% withdrawal fee — confirm these figures are current",
      "https://predictit.org/legal/feestructure",
    ),
    minDeposit: V(
      "minimum deposit amount",
      "https://predictit.org",
    ),
    withdrawalMethods: V(
      "withdrawal methods (historically ACH, check) — confirm current options",
      "https://predictit.org/help",
    ),
    fundingMethods: V(
      "funding methods — ACH, debit card?",
      "https://predictit.org/help",
    ),
    currency: "USD",
    mobileApp: {
      ios: null,
      android: null,
      notes: V(
        "native iOS / Android app availability",
        "https://predictit.org",
      ),
    },
    affiliateUrl: null,
    affiliateNetwork: V(
      "PredictIt affiliate or referral program",
      "https://predictit.org",
    ),
    promoCode: null,
    promoNote: V(
      "any active PredictIt promo code or signup bonus",
      "https://predictit.org",
    ),
    bestFor: "US users focused on political markets who want to trade small positions ($1 increments)",
    skipIf: "You want macro-economic or sports markets — PredictIt is primarily political. Also verify current legal status before trading.",
    ease: "Easy",
    notes: "Historically focused on US political events. Small contract limits apply. VERIFY operational status before recommending.",
    live: false,
    reviewPath: "/platforms/predictit",
    // compat
    region: "United States",
    funding: V("ACH bank transfer — confirm current deposit options", "https://predictit.org"),
    affiliate: false,
  },

  // ── COINBASE ──────────────────────────────────────────────────────────────
  {
    id: "coinbase",
    name: "Coinbase",
    slug: "coinbase",
    oneLiner: "Major US crypto exchange that has introduced regulated event contracts.",
    eligibility: {
      regions: V(
        "countries where Coinbase event contracts / prediction markets are available",
        "https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trading",
      ),
      usStatus: V(
        "confirm US availability for event contracts product specifically",
        "https://help.coinbase.com",
        "needs-check",
      ),
      details: V(
        "age requirement and any state exclusions",
        "https://coinbase.com/legal",
      ),
      source: "https://coinbase.com/legal",
      lastUpdated: "needs-check",
    },
    regulation: V(
      "CFTC or state-level registration for any event contracts / prediction market product",
      "https://www.cftc.gov / https://coinbase.com/legal",
    ),
    fees: V(
      "fee structure for any prediction market or event contract product on Coinbase",
      "https://coinbase.com/advanced-trade/fees",
    ),
    minDeposit: V(
      "minimum deposit or trade size for prediction market products",
      "https://coinbase.com",
    ),
    withdrawalMethods: V(
      "withdrawal methods from Coinbase",
      "https://help.coinbase.com",
    ),
    fundingMethods: V(
      "fiat and crypto funding methods",
      "https://help.coinbase.com",
    ),
    currency: V(
      "settlement currency for prediction markets product",
      "https://coinbase.com",
    ),
    mobileApp: {
      ios: true,
      android: true,
      notes: V(
        "confirm prediction market features are in the Coinbase mobile app",
        "https://apps.apple.com/app/coinbase-buy-bitcoin-ether",
      ),
    },
    affiliateUrl: null,
    affiliateNetwork: V(
      "Coinbase affiliate program — likely through Impact Radius or CoinbaseOne partner",
      "https://www.coinbase.com/affiliate-program",
    ),
    promoCode: null,
    promoNote: V(
      "any active Coinbase promo code for new accounts",
      "https://coinbase.com/earn",
    ),
    bestFor: "Crypto-native users who already have a Coinbase account and want to try event contracts without a new wallet",
    skipIf: V(
      "Confirm what specific prediction market / event contract product Coinbase offers before writing this section",
      "https://coinbase.com",
    ),
    ease: "Medium",
    notes: "VERIFY whether Coinbase has a current prediction markets product. The exchange has discussed event contracts; confirm current offering.",
    live: false,
    reviewPath: "/platforms/coinbase",
    // compat
    region: V("US + international — check coinbase.com/legal for country list", "https://coinbase.com/legal"),
    funding: V("fiat (ACH, wire, debit) and crypto — check current methods", "https://help.coinbase.com"),
    affiliate: false,
  },

  // ── DRAFTKINGS ────────────────────────────────────────────────────────────
  {
    id: "draftkings",
    name: "DraftKings",
    slug: "draftkings",
    oneLiner: "US sports-betting leader that offers prediction-market-style event contracts alongside sportsbook.",
    eligibility: {
      regions: "United States (state-by-state)",
      usStatus: V(
        "list of US states where DraftKings Sportsbook / event contracts are legal — availability changes as states legalize",
        "https://draftkings.com/help/us-state-by-state-regulations",
        "needs-check",
      ),
      details: "Must be 21+ in most states. Not available in all US states. Check your state before signing up.",
      source: "https://draftkings.com/help",
      lastUpdated: "needs-check",
    },
    regulation: V(
      "CFTC registration for any event contract product (distinct from their sportsbook licenses)",
      "https://www.cftc.gov / https://draftkings.com/legal",
    ),
    fees: V(
      "juice/vig or fee structure for DraftKings event contracts or prediction-market products",
      "https://draftkings.com/help",
    ),
    minDeposit: V(
      "minimum deposit amount",
      "https://draftkings.com/help",
    ),
    withdrawalMethods: V(
      "withdrawal methods (PayPal, ACH, check, online banking?)",
      "https://draftkings.com/help/account/payouts",
    ),
    fundingMethods: V(
      "deposit methods (debit card, ACH, PayPal, etc.)",
      "https://draftkings.com/help",
    ),
    currency: "USD",
    mobileApp: {
      ios: true,
      android: true,
      notes: V(
        "confirm app availability and whether event contracts feature is in mobile app",
        "https://apps.apple.com (search DraftKings Sportsbook)",
      ),
    },
    affiliateUrl: null,
    affiliateNetwork: V(
      "DraftKings affiliate program — check their affiliate portal or CJ/Impact networks",
      "https://draftkings.com/affiliates",
    ),
    promoCode: null,
    promoNote: V(
      "any active DraftKings new-user promo (these change frequently — never hardcode)",
      "https://draftkings.com/promo",
    ),
    bestFor: "US sports fans in legal-betting states who want to combine sports predictions with a full sportsbook account",
    skipIf: "You are outside the US, in a state where DraftKings is not licensed, under 21, or primarily interested in macro/political markets",
    ease: "Easy",
    notes: "Primarily a sportsbook. VERIFY what specific prediction-market or event-contract product DraftKings offers, distinct from their standard sports betting.",
    live: false,
    reviewPath: "/platforms/draftkings",
    // compat
    region: "United States (varies by state)",
    funding: V("debit card, ACH, PayPal — confirm current options", "https://draftkings.com/help"),
    affiliate: false,
  },

  // ── MANIFOLD MARKETS ──────────────────────────────────────────────────────
  {
    id: "manifold",
    name: "Manifold",
    slug: "manifold",
    oneLiner: "Free play-money prediction markets — the best risk-free way to learn prediction market mechanics.",
    eligibility: {
      regions: "Global (play-money only, no real-money trading)",
      usStatus: "Available — no real money involved, no geographic restrictions reported",
      details: "Manifold uses 'mana' (M$), a play-money currency with no cash value. No deposit, no withdrawal of real funds.",
      source: "https://manifold.markets/about",
      lastUpdated: "2025-01",
    },
    regulation: "Not applicable — no real money trading",
    fees: "Free",
    minDeposit: "None — free to sign up and play",
    withdrawalMethods: "Not applicable — play money only",
    fundingMethods: "None — free starting balance of mana",
    currency: "Mana (M$) — play money, no real-money value",
    mobileApp: {
      ios: null,
      android: null,
      notes: V(
        "native iOS / Android app or PWA availability",
        "https://manifold.markets",
      ),
    },
    affiliateUrl: null,
    affiliateNetwork: "None — no-revenue platform",
    promoCode: null,
    promoNote: "No promo codes — Manifold is completely free",
    bestFor: "Anyone who wants to learn prediction market mechanics without risking real money, or researchers who want to create experimental markets",
    skipIf: "You want to trade with real money — Manifold is play-money only and wins have no cash value",
    ease: "Easy",
    notes: "Excellent learning tool. Zero financial risk. Community-created markets on almost any topic.",
    live: false,
    reviewPath: "/platforms/manifold",
    // compat
    region: "Global (play-money, no restrictions reported)",
    funding: "None (free play money)",
    affiliate: false,
  },
];

// ─────────────────────────────────────────────────────────────────────────────
//  Convenience lookups
// ─────────────────────────────────────────────────────────────────────────────

export const platformById = Object.fromEntries(
  platforms.map((p) => [p.id, p])
) as Record<string, PlatformData>;

/** Platforms with a published live review page */
export const livePlatforms = platforms.filter((p) => p.live);

/** Platforms that are stubs only (review page not yet fully written) */
export const stubPlatforms = platforms.filter((p) => !p.live);
