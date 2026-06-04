---
title: 'Prediction Market Fees Explained: What You Actually Pay to Trade'
description: 'A clear breakdown of every fee you might pay on Kalshi, Polymarket, and Crypto.com: trading fees, spreads, deposit costs, and withdrawal charges.'
pubDate: 'Jan 15 2026'
heroImage: '../../assets/fees-calculator.svg'
---

Fees are one of the least-discussed but most important factors in prediction market trading. A trade that looks profitable on paper can turn into a loss once you account for the full cost of entering and exiting. Here is a clear breakdown.

*Educational content only, not financial advice. Fee structures change: always verify current rates on each platform before trading.*

## The three costs you actually pay

### 1. Trading fees (explicit)

Some platforms charge an explicit fee on every trade, shown as a percentage of your potential payout or notional value. Kalshi is the primary example among the major platforms.

How it works: if you buy 100 Yes contracts at 60¢ ($60 total) and the fee is 7% of potential payout, you pay roughly $4.20 in fees on a $100 potential payout. That shifts your break-even from 60% to about 65%.

Explicit fees are predictable and easy to model. The downside is they compound quickly on multiple trades, especially on contracts with short time horizons where you are trading in and out frequently.

### 2. Spread (implicit)

The spread is the gap between the best bid (what buyers will pay) and the best ask (what sellers will accept). Even on platforms with zero explicit fees, the spread is a real cost.

Example: You want to buy Yes at the current price. The bid is 58¢ and the ask is 62¢. If you buy at the ask (62¢), you have already "paid" 4¢ more than the midpoint (60¢). If you later sell at the bid (58¢), you have paid 4¢ on exit too. Round trip cost: 8¢ per contract, or 8% of a $1 contract.

On liquid markets (major elections, Fed decisions), spreads on Polymarket and Kalshi are often 1-3¢. On thin markets, spreads can be 10-20¢ or more. Always check the order book before trading.

### 3. Blockchain gas fees (Polymarket)

Polymarket runs on Polygon, which has very low gas fees: typically a fraction of a cent per transaction. This is not a material cost for most traders but worth knowing about.

Withdrawing USDC from Polymarket to a bank account requires going through a crypto exchange, which has its own fees (usually 0.5-1.5% of the amount). Factor this in if you are calculating total round-trip costs.

## Platform-by-platform breakdown

### Kalshi

- **Trading fee:** Per-contract fee on each trade, expressed as a percentage of potential payout. Rates vary by market (typically 5-10%). Check Kalshi's fee schedule for current rates.
- **Deposit fee:** None for ACH bank transfer. Card deposits may incur a small processing fee.
- **Withdrawal fee:** None for standard ACH.
- **Spread:** Typically narrow on popular markets, wider on niche ones.

**Total round-trip cost estimate (liquid market):** 10-15% of contract value including trading fees and spread.

### Polymarket

- **Trading fee:** Historically very low or zero on most markets. Check current terms: fee structures have evolved.
- **Deposit fee:** None (you bring USDC from your wallet).
- **Withdrawal:** No fee to withdraw to your wallet; exchange fees apply if converting back to fiat.
- **Spread:** Varies. Top markets are very tight (1-3¢). Smaller markets can be wide.
- **Gas fees:** Negligible on Polygon.

**Total round-trip cost estimate (liquid market):** 2-6% depending on spread and withdrawal method.

### Crypto.com Predict

- **Trading fee:** Varies by product and CRO holder status. Review current pricing on the platform.
- **Deposit:** Via Crypto.com wallet, no additional deposit fee.
- **Withdrawal:** Standard Crypto.com withdrawal rules apply.
- **Spread:** Information less publicly available; check the platform directly.

## How fees affect your profitability

Say you think an outcome has a 65% true probability but the market prices it at 60¢. You have a theoretical 5-percentage-point edge.

On Polymarket with a 2¢ spread: your effective entry is 62¢. Break-even probability becomes 62%. Your edge is now 3 percentage points, not 5.

On Kalshi with a 7% fee and 2¢ spread: your costs are higher. The fee on a 60¢ entry (7% of $1 potential payout) is 7¢, plus 2¢ spread = 9¢ per contract total cost. Break-even probability becomes roughly 69%. Your supposed 5-point edge is now negative.

This is why fees matter so much. Small perceived edges disappear entirely once costs are included.

## The rule of thumb

Before any trade, calculate your break-even probability including all costs:

> **Break-even = (entry price + total fees per contract) / $1**

If that number is below your estimated true probability, the trade has positive expected value. If not, skip it.

*Fee schedules are subject to change. Always check each platform's current terms before trading.*
