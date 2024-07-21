---
layout: post
title:  "TSA trading bot: Part 4 - Trading rules"
date:   2024-07-25 00:00:00 -0500
categories: in-progress
toc: true
---

![trading_bot](/assets/tsa_trading_bot/baseline_model_title_image.png)

<h2> Overview </h2>
* Table of contents
{:toc}

# Introduction
[Last time](https://ferraijv.github.io/posts/data/2024/07/05/tsa-exploratory-analysis.html), we built a simple model to 
predict next week's TSA traffic using only previous TSA traffic numbers. We relied on a straightforward heuristic: using 
last year's numbers adjusted for YoY trend. This simple baseline model allows us to quickly get a model in production, 
from where we can track performance and gradually refine it to improve profitability.

Today, we take the next step: using the output from this model to make actual trades on Kalshi, a prediction market 
platform where users can trade on the outcome of events. This will involve:

1. Integrating with Kalshi's API
2. Pulling current market prices
3. Comparing current market prices with our model's predictions
4. Identifying any mispricings in the market
5. Placing orders through the Kalshi API if a mispricing exists

By the end of this post, you’ll have a practical understanding of how to leverage your predictive model to potentially 
generate profits on [Kalshi](kalshi.com/sign-up/?referral=c9d2b0f1-b339-4878-b61c-65c4e7002b51).

Note: I link to Kalshi with my referral link. We each get $25 if you sign up and make a certain number of trades with
this link.

# Integrating with Kalshi's API



