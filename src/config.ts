// ──────────────────────────────────────────────────────────────────────────
//  Site identity — the only things you need to change here.
//  All platform data now lives in src/data/platforms.ts (single source of truth).
// ──────────────────────────────────────────────────────────────────────────

// 1) YOUR BRAND NAME
export const SITE_NAME = "Predikt";

// 2) YOUR DOMAIN — update after you buy a custom domain
export const SITE_URL = "https://venerable-lollipop-5e026d.netlify.app";

// 3) A one-line tagline for the header and search results
export const SITE_TAGLINE =
  "Plain-English guides to prediction markets: and where to trade them.";

// ── Platform data re-exported for backward compatibility ──────────────────
// All pages that previously imported Platform / platforms from here continue
// to work. New code should import directly from src/data/platforms.ts.
export type { PlatformData as Platform } from "./data/platforms";
export { platforms, platformById } from "./data/platforms";
