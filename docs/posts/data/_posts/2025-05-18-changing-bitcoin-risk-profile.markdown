---
layout: post
title:  "How to Use Kalshi to Change Risk Profile of Bitcoin"
date:   2024-05-17 00:00:00 -0500
categories: [prediction markets, cryptocurrency]
image: /assets/placeholder.webp
---

# Overview

In this post, I'll show howto use [Kalshi's](kalshi.com/sign-up/?referral=22442314-8e90-4c94-aed9-a3f1f78e990d) Bitcoin markets to change the risk profile of Bitcoin. This allows for speculators to profit off bitcoin under a wider umbrella of outcomes. 

For example, if I hypothesize that bitcoin will either skyrocket to $200k+ or stay around the same price, I might hesitate to purchase bitcoin. This is because I am concerned about the opportunity cost of holding bitcoin when there is a high likelihood the price does not fluctuate significantly.

Using Kalshi's bitcoin market, we can devise holdings that will profit in either of these cases. 

This post will dive into how we can structure a portfolio catered to various hypotheses about Bitcoin's price movements. 

## Kalshi Bitcoin Market

Kalshi has several different cryptocurrency markets. For this post, we will focus on the [How high will Bitcoin get this year?](https://kalshi.com/markets/kxbtcmaxy/how-high-will-bitcoin-get-this-year) market. This market has contracts at various strike prices. For each contract there is a "yes" and "no" side. Let's look at the "$125k or above" "no" contract:

- If the price of btc reaches or exceeds $125k, this contract will pay $0
- If the price of btc **does not** reach or exceed $125k, this contract will pay $1

Currently:
- **"Yes"** contracts are priced at **$0.57**
- **"No"** contracts are priced at **$0.43**

This implies the market assigns a **57% probability** that BTC will reach $125k by year-end.

For more on how to interpret these probabilities, see [this primer](https://docs.polymarket.com/polymarket-learn/get-started/what-is-polymarket).


## Recent Bitcoin Price Action

![btc](/assets/change_risk_profile_of_bitcoin/btc_price.webp){: width="500" height="250" }

Bitcoin is currently priced at $103,046.60 after a recent increase from ~$80k. Reasons for this rally include:
1. [Recent trade deals](https://www.reuters.com/markets/currencies/bitcoin-tops-100000-trade-deal-optimism-2025-05-08/)
2. [Crypto friendly regulation](https://www.congress.gov/bill/119th-congress/senate-bill/394/text)
3. [Recent short liquidations](https://www.coindesk.com/markets/2025/04/23/bitcoin-ether-dogecoin-surge-spurs-usd500m-in-short-liquidations)

---

## Hypothetical Price Scenarios

Let’s simplify and assume BTC trades at **$100,000**. Suppose we believe there's a chance it will:

- Spike to **$200k**
- Drop modestly to **$80k**
- Crash to **$20k**

Let’s analyze this without Kalshi first.

### Case A: Holding Only Bitcoin

We buy **$100 worth** of BTC. Then:

- If BTC hits $200k → Gain $100  
- If BTC drops to $80k → Lose $20  
- If BTC drops to $20k → Lose $80  

Expected return (based on your probabilities):
- 10% chance of +$100 = +$10  
- 80% chance of -$20 = -$16  
- 10% chance of -$80 = -$8  
- **Net Expected Return:** **-$14**

So even though the upside is large, the probabilities suggest a net loss.

---

## Adjusting the Risk Profile with Kalshi

Now, suppose we **buy $100 of BTC** *and* spend **$43 on 100 "No" contracts** at $0.43 each.

### Payouts Under Different Scenarios

#### BTC @ $200k
- BTC doubles → +$100  
- Kalshi “No” contracts expire worthless → -$43  
- **Total profit: +$57**

#### BTC @ $80k
- BTC drops → -$20  
- Kalshi “No” contracts pay $1 each → +$57  
- **Total profit: +$37**

#### BTC @ $20k
- BTC drops → -$80  
- Kalshi contracts pay → +$57  
- **Total loss: -$23**

### Adjusted Expected Return

- 10% chance of +$57 = +$5.70  
- 80% chance of +$37 = +$29.60  
- 10% chance of -$23 = -$2.30  
- **Net Expected Return: +$33**

This setup turns a losing bet into a positive-expected-value trade, **based entirely on your assumptions**.

---

### Assumptions

- **Current BTC Price:** $100,000  
- **Kalshi $125k BTC No Price:** $0.43  
- **Bitcoin Purchase:** $100.00  
- **Kalshi 'No' Contracts Purchased:** 100  
- **Kalshi Strike Price:** $125,000.00  


| BTC Price | BTC % Change | BTC Return | Kalshi $125k Price | Kalshi $125k Payout | Kalshi $125k Return | Total Return | Total Spend |
|-----------|---------------|------------|---------------------|----------------------|----------------------|---------------|--------------|
| $20,000   | -80%          | -$80.00    | $43.00              | 100                  | $57                  | -$23.00       | $143.00      |
| $30,000   | -70%          | -$70.00    | $43.00              | 100                  | $57                  | -$13.00       | $143.00      |
| $40,000   | -60%          | -$60.00    | $43.00              | 100                  | $57                  | -$3.00        | $143.00      |
| $50,000   | -50%          | -$50.00    | $43.00              | 100                  | $57                  | $7.00         | $143.00      |
| $60,000   | -40%          | -$40.00    | $43.00              | 100                  | $57                  | $17.00        | $143.00      |
| $70,000   | -30%          | -$30.00    | $43.00              | 100                  | $57                  | $27.00        | $143.00      |
| $80,000   | -20%          | -$20.00    | $43.00              | 100                  | $57                  | $37.00        | $143.00      |
| $90,000   | -10%          | -$10.00    | $43.00              | 100                  | $57                  | $47.00        | $143.00      |
| $100,000  | 0%            | $0.00      | $43.00              | 100                  | $57                  | $57.00        | $143.00      |
| $110,000  | 10%           | $10.00     | $43.00              | 100                  | $57                  | $67.00        | $143.00      |
| $120,000  | 20%           | $20.00     | $43.00              | 100                  | $57                  | $77.00        | $143.00      |
| $130,000  | 30%           | $30.00     | $43.00              | 0                    | -$43                 | -$13.00       | $143.00      |
| $140,000  | 40%           | $40.00     | $43.00              | 0                    | -$43                 | -$3.00        | $143.00      |
| $150,000  | 50%           | $50.00     | $43.00              | 0                    | -$43                 | $7.00         | $143.00      |
| $160,000  | 60%           | $60.00     | $43.00              | 0                    | -$43                 | $17.00        | $143.00      |
| $170,000  | 70%           | $70.00     | $43.00              | 0                    | -$43                 | $27.00        | $143.00      |
| $180,000  | 80%           | $80.00     | $43.00              | 0                    | -$43                 | $37.00        | $143.00      |
| $190,000  | 90%           | $90.00     | $43.00              | 0                    | -$43                 | $47.00        | $143.00      |
| $200,000  | 100%          | $100.00    | $43.00              | 0                    | -$43                 | $57.00        | $143.00      |


## Disclaimer

This is not investment advice, and the outcome of this analysis depends on speculative assumptions about the relative probabilities of Bitcoin prices by the end of the year. I have no idea what the price of Bitcoin will be at any point in the future.

# Conclusion

This post shows how we can use prediction market contracts to hedge cryptocurrency holdings to adjust expected returns based on our assumptions about future prices.

