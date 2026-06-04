/**
 * Internal link graph — maps page slugs/paths to contextually related pages.
 * Used by RelatedGuides.astro to render the "Related guides" block.
 *
 * Rules (from spec):
 *  - fees article   -> each platform review
 *  - each review    -> comparison page + beginner guide
 *  - comparison     -> reviews + roundup
 *  - event pages    -> relevant reviews
 */

export interface RelatedLink {
  href: string;
  title: string;
  description: string;
}

export type RelatedLinksMap = Record<string, RelatedLink[]>;

export const relatedLinks: RelatedLinksMap = {
  // ── Blog posts ─────────────────────────────────────────────────────────────

  "prediction-market-fees-explained": [
    { href: "/blog/kalshi-review", title: "Kalshi Review", description: "Full review of fees, markets, and ease of use" },
    { href: "/blog/polymarket-review", title: "Polymarket Review", description: "How Polymarket's fee structure compares" },
    { href: "/blog/crypto-com-predict-review", title: "Crypto.com Predict Review", description: "Fees and funding on Crypto.com" },
    { href: "/compare", title: "Compare all platforms", description: "Side-by-side fee and feature table" },
  ],

  "kalshi-review": [
    { href: "/compare", title: "Compare all platforms", description: "See how Kalshi stacks up against alternatives" },
    { href: "/guides/how-to-use-kalshi", title: "How to use Kalshi", description: "Step-by-step guide to placing your first trade" },
    { href: "/what-is-a-prediction-market", title: "What is a prediction market?", description: "New to prediction markets? Start here" },
    { href: "/best-prediction-markets-2026", title: "Best prediction markets 2026", description: "Where Kalshi ranks in our roundup" },
  ],

  "polymarket-review": [
    { href: "/compare", title: "Compare all platforms", description: "Side-by-side with Kalshi and others" },
    { href: "/blog/polymarket-beginners-guide", title: "Polymarket beginner's guide", description: "How to get started with USDC and Polygon" },
    { href: "/what-is-a-prediction-market", title: "What is a prediction market?", description: "New to prediction markets? Start here" },
    { href: "/best-prediction-markets-2026", title: "Best prediction markets 2026", description: "Where Polymarket ranks in our roundup" },
  ],

  "crypto-com-predict-review": [
    { href: "/compare", title: "Compare all platforms", description: "See how Crypto.com compares to Kalshi and Polymarket" },
    { href: "/what-is-a-prediction-market", title: "What is a prediction market?", description: "New to prediction markets? Start here" },
    { href: "/best-prediction-markets-2026", title: "Best prediction markets 2026", description: "Where Crypto.com ranks in our roundup" },
  ],

  "kalshi-vs-polymarket": [
    { href: "/blog/kalshi-review", title: "Full Kalshi review", description: "Deep dive into Kalshi's markets and features" },
    { href: "/blog/polymarket-review", title: "Full Polymarket review", description: "Deep dive into Polymarket's markets and features" },
    { href: "/compare", title: "3-platform comparison", description: "Add Crypto.com to the comparison" },
    { href: "/guides/how-to-use-kalshi", title: "How to use Kalshi", description: "Chose Kalshi? Here's how to start" },
  ],

  "what-is-a-prediction-market-beginners-guide": [
    { href: "/what-is-a-prediction-market", title: "Platform overview", description: "Which platform is right for you?" },
    { href: "/compare", title: "Compare platforms", description: "Side-by-side comparison" },
    { href: "/blog/how-to-read-prediction-market-prices", title: "How to read prices", description: "What 65¢ actually means" },
    { href: "/risks-and-responsible-trading", title: "Risks and responsible trading", description: "What to know before you trade" },
  ],

  "how-to-read-prediction-market-prices": [
    { href: "/what-is-a-prediction-market", title: "What is a prediction market?", description: "Start here if you're new" },
    { href: "/blog/prediction-market-strategies-beginners", title: "Beginner strategies", description: "Apply price-reading to your trading" },
    { href: "/compare", title: "Compare platforms", description: "Where to apply what you've learned" },
  ],

  "prediction-market-strategies-beginners": [
    { href: "/blog/how-to-read-prediction-market-prices", title: "How to read prices", description: "The foundation of every strategy" },
    { href: "/blog/how-prediction-markets-make-money", title: "Can you make money?", description: "An honest look at the odds" },
    { href: "/risks-and-responsible-trading", title: "Risks and responsible trading", description: "Know the risks before you go deeper" },
  ],

  "how-prediction-markets-make-money": [
    { href: "/blog/prediction-market-strategies-beginners", title: "Beginner strategies", description: "How to find your edge" },
    { href: "/blog/prediction-market-fees-explained", title: "Fees explained", description: "How fees affect your returns" },
    { href: "/risks-and-responsible-trading", title: "Risks and responsible trading", description: "Important reading before you go deeper" },
  ],

  "election-prediction-markets-guide": [
    { href: "/blog/kalshi-review", title: "Kalshi review", description: "The main regulated US platform for political markets" },
    { href: "/blog/polymarket-review", title: "Polymarket review", description: "Global political markets on crypto" },
    { href: "/compare", title: "Compare platforms", description: "Find the right platform for political trading" },
  ],

  "sports-prediction-markets": [
    { href: "/blog/kalshi-review", title: "Kalshi review", description: "Sports markets on a regulated US platform" },
    { href: "/compare", title: "Compare platforms", description: "Which platform has the sports markets you want?" },
    { href: "/risks-and-responsible-trading", title: "Risks and responsible trading", description: "Important before wagering on sports" },
  ],

  "crypto-prediction-markets-guide": [
    { href: "/blog/polymarket-review", title: "Polymarket review", description: "The leading crypto-native prediction market" },
    { href: "/blog/crypto-com-predict-review", title: "Crypto.com Predict review", description: "Predictions within a crypto exchange" },
    { href: "/compare", title: "Compare platforms", description: "Full side-by-side comparison" },
  ],

  "polymarket-beginners-guide": [
    { href: "/blog/polymarket-review", title: "Polymarket review", description: "Is Polymarket right for you?" },
    { href: "/compare", title: "Compare platforms", description: "See if Polymarket is the right choice" },
    { href: "/risks-and-responsible-trading", title: "Risks and responsible trading", description: "Read before you deposit" },
  ],

  // ── Static pages ───────────────────────────────────────────────────────────

  "compare": [
    { href: "/blog/kalshi-review", title: "Kalshi review", description: "Full Kalshi deep dive" },
    { href: "/blog/polymarket-review", title: "Polymarket review", description: "Full Polymarket deep dive" },
    { href: "/blog/crypto-com-predict-review", title: "Crypto.com review", description: "Full Crypto.com deep dive" },
    { href: "/best-prediction-markets-2026", title: "Best prediction markets 2026", description: "Our ranked roundup" },
  ],

  "best-prediction-markets-2026": [
    { href: "/blog/kalshi-review", title: "Kalshi review", description: "Full review" },
    { href: "/blog/polymarket-review", title: "Polymarket review", description: "Full review" },
    { href: "/blog/crypto-com-predict-review", title: "Crypto.com review", description: "Full review" },
    { href: "/compare", title: "Side-by-side comparison", description: "Feature-by-feature table" },
  ],

  "risks-and-responsible-trading": [
    { href: "/what-is-a-prediction-market", title: "What is a prediction market?", description: "The basics before you start" },
    { href: "/blog/how-prediction-markets-make-money", title: "Can you make money?", description: "An honest assessment" },
    { href: "/blog/prediction-market-fees-explained", title: "Fees explained", description: "What trading actually costs" },
  ],
};
