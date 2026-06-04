// ──────────────────────────────────────────────────────────────────────────
//  EDIT THIS FILE — it controls your whole site's brand + affiliate links.
//  You don't need to touch anything else to change the name or wire up money.
// ──────────────────────────────────────────────────────────────────────────

// 1) YOUR BRAND NAME — change this one line to whatever domain you buy.
export const SITE_NAME = "Predikt";

// 2) YOUR DOMAIN — set this after you buy it (used for SEO + sitemap).
export const SITE_URL = "https://venerable-lollipop-5e026d.netlify.app";

// 3) A one-line tagline shown in the header / search results.
export const SITE_TAGLINE =
  "Plain-English guides to prediction markets — and where to trade them.";

// 4) PLATFORMS — paste your real affiliate links into `affiliateUrl` once
//    your programs approve you. Until then they point to the public site so
//    nothing is broken. `affiliate: false` means "no link yet" (no money).
export type Platform = {
  id: string;
  name: string;
  affiliateUrl: string;
  affiliate: boolean; // true once your tracked link is in place
  region: string;
  regulation: string;
  fees: string;
  funding: string;
  bestFor: string;
  ease: string; // "Easy" | "Medium" | "Advanced"
  notes: string;
};

export const platforms: Platform[] = [
  {
    id: "kalshi",
    name: "Kalshi",
    affiliateUrl: "https://kalshi.com", // ← replace with your affiliate link
    affiliate: false,
    region: "United States",
    regulation: "CFTC-regulated (US)",
    fees: "Per-contract trading fee; no deposit fee",
    funding: "USD — bank transfer / debit",
    bestFor: "US users who want a regulated, mainstream experience",
    ease: "Easy",
    notes: "The most beginner-friendly regulated option for US residents.",
  },
  {
    id: "polymarket",
    name: "Polymarket",
    affiliateUrl: "https://polymarket.com", // ← replace with your affiliate link
    affiliate: false,
    region: "Global — NOT available to US persons",
    regulation: "Crypto-native, offshore",
    fees: "Low/zero trading fees historically",
    funding: "USDC (crypto stablecoin)",
    bestFor: "Crypto-comfortable users outside the US who want breadth + liquidity",
    ease: "Medium",
    notes: "Largest event selection and brand recognition. Requires a crypto wallet.",
  },
  {
    id: "crypto-com",
    name: "Crypto.com",
    affiliateUrl: "https://crypto.com", // ← replace with your affiliate link
    affiliate: false,
    region: "Varies by country — check local availability",
    regulation: "Licensed in multiple regions",
    fees: "Varies by product",
    funding: "Crypto + fiat (region dependent)",
    bestFor: "Existing Crypto.com users who want events alongside their exchange",
    ease: "Medium",
    notes: "Convenient if you already hold crypto on the platform.",
  },
];
