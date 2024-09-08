---
layout: post
title:  "What are prediction markets?"
date:   2024-07-24 00:00:00 -0500
categories: data
toc: true
---

![Prediction market cover art](/assets/what_are_prediction_markets/cover_art.webp){: width="500" height="500" }
<h1> Prediction Markets Explained </h1>
* Table of contents
{:toc}

### What is a Prediction Market?

A prediction market is an exchange to buy and sell contracts that pay out in certain 
events. Prediction markets offer contracts on a broad range of different categories like:

1. **Political Markets:** Predict outcomes of elections, policy decisions, or legislative actions. Examples include predicting the winner of a presidential election or the passage of a bill.

2. **Financial Markets:** Forecast economic indicators, stock prices, or corporate earnings. For instance, predicting the quarterly revenue of a tech giant.

3. **Sports Markets:** Estimate the outcomes of sports events, such as the winner of a championship or the performance of a specific player.

4. **Entertainment Markets:** Predict outcomes related to movies, TV shows, or awards. For example, forecasting the winner of the Oscars.


Participants trade these contracts based on their beliefs about the 
likelihood of a particular event occurring. The prices of these contracts fluctuate 
based on market participants' perceptions of the likelihood of these events occurring. The 
price at any given time can be interpreted as the probability of this event happening.

#### PredictIt Example

[PredictIt](https://www.predictit.org/) is a prediction market specialzing in political outcome markets. Their 
market for "Who will win the 2024 US Presidential Election"

![us presidential election market from PredictIt](/assets/what_are_prediction_markets/predictit_us_presidential_market.webp)

As of 7/24, "the market" is giving Donald Trump a roughly 57% change of winning the 
presidency and Harris a 45% chance. For a given candidate, market participants can purchase
either "yes" shares if they believe that candidate will win, or "no" contract if they do not think
that candidate will win. The price of the "no" shares are not explicitly listed above, but are 1-(yes_price).

### How Do Prediction Markets Work?

Prediction markets operate similarly to traditional financial markets but are focused on predicting the likelihood of specific events rather than trading stocks or commodities. Here's a step-by-step breakdown of how they work:

1. **Event Specification:** A specific event or outcome is defined. For example, "Will Candidate X win the upcoming presidential election?"

2. **Contract Creation:** Contracts are created that pay out a fixed amount if the event occurs and nothing if it doesn't. Generally, a contract might pay $1 if Candidate X wins and $0 if they lose.

3. **Trading:** Participants buy and sell these contracts based on their beliefs about the likelihood of the event occurring. If a participant believes Candidate X has a 70% chance of winning, they might be willing to pay up to $0.70 for the contract.

4. **Price Discovery:** As more participants trade, the contract price fluctuates, reflecting the collective belief about the probability of the event. If many participants believe Candidate X will win, the contract price will rise.

5. **Settlement:** After the event occurs, the contracts are settled. If Candidate X wins, holders of the contracts receive the payout; if not, the contracts expire worthless.

### Applications of Prediction Markets

Prediction markets have numerous applications across various fields, providing valuable insights and aiding decision-making:

#### Elections and Politics
Political analysts and campaigners use prediction markets to gauge public sentiment and adjust strategies accordingly. Governments and think tanks use these markets to forecast policy impacts.

#### Business and Economics
Companies utilize prediction markets to forecast sales, product success, and market trends. Economic 
researchers use them to predict macroeconomic indicators. Both companies and individuals can use 
prediction markets to hedge against adverse events. For example, Kalshi has offered a market for which
companies will have layoffs. If I work for Google, I can buy contracts that payout if Google has layoffs. 
That way, in the unfortunate case I am get laid off, I will get financially compensated from the contracts 
paying out. 

#### Academia and Research
Researchers use prediction markets to predict scientific breakthroughs and research outcomes. 
They also serve as experimental platforms for studying market behavior and decision-making. The most 
famous example of this is PredictIt which operates as a research project out of Victoria University 

#### Sports and Entertainment
Fans and analysts use prediction markets to speculate on game outcomes and entertainment awards. 
Studios and networks gauge potential success of movies and shows. 
[Kalshi](kalshi.com/sign-up/?referral=c9d2b0f1-b339-4878-b61c-65c4e7002b51) for example, has offers markets 
to predict the Rotten Tomatoes scores of upcoming movies.

![Kalshi movie markets](/assets/what_are_prediction_markets/movie_markets.webp)

#### Public Health
During pandemics, prediction markets have been used to forecast the spread of diseases and the effectiveness of interventions.

### Advantages of Prediction Markets

Prediction markets offer several benefits that make them valuable tools for forecasting:

#### Aggregated Wisdom
They aggregate diverse opinions and knowledge, often leading to more accurate predictions than individual experts. Most 
Americans get their news from [digital sources](https://www.pewresearch.org/journalism/fact-sheet/social-media-and-news-fact-sheet/)
where often the most incindiary pundits become viral with no regard for the historical accuracy of their predictions. Research
has drawn "political experts'" prediction. [capabilities into question](https://hbr.org/2015/02/what-research-tells-us-about-making-accurate-predictions) 

#### Incentive Alignment
Participants have a financial incentive to make accurate predictions, leading to more thoughtful and informed contributions. 

#### Real-Time Information
Markets provide up-to-date probabilities, allowing stakeholders to make informed decisions based on the latest data.

Recently, prediction markets have responded almost instataneously to new information. Below is an example
from PredictIt where you can clearly see the inflection point the night of June 26th when Joe Biden debated 
Donald Trump. Previously, markets had Joe Biden with about an 80% probability of winning the nomination. Traders
reacted strongly to Biden's debate performance sending Joe Biden's chances down to ~60% the night of the debate
and down to 40% just a few days later. 

[![Democratic nominee price history](/assets/what_are_prediction_markets/historical_democratic_nomination.webp)](https://www.predictit.org/markets/detail/7057/Who-will-win-the-2024-Democratic-presidential-nomination)

The above graphic shows the price of purchasing "yes" contracts for Biden and Harris overtime. You can see
a clear significant drop the night of the debate.

#### Transparency
Market prices reflect collective beliefs, providing a transparent and objective measure of event probabilities.

### Challenges and Limitations

Despite their advantages, prediction markets also face challenges and limitations:

#### Regulation 
Legal and regulatory issues can restrict the operation of prediction markets in some jurisdictions. This has been 
a significant issue for prediction market adoption especially in the United States. Currently, [PredictIt is at-risk
of being shut down](https://www.predictit.org/platform-announcements) and one of the largest market in the 
world, [Polymarket](https://polymarket.com/) isn't even available for US traders.

#### Market Manipulation
Like any market, prediction markets are susceptible to manipulation by participants with large financial stakes 
or ulterior motives. This is especially a concern for smaller markets where manipulation may be done with relatively small
amounts of capital.

#### Liquidity
Low participant numbers can lead to illiquid markets, reducing the accuracy and reliability of predictions.

#### Ethical Concerns 
Predicting sensitive or controversial events can raise ethical issues, such as markets on natural disasters or violent events. 
This can even create perverse incentives. As an example on the more comical side, there was allegedly a man who
placed on bet on the presence of a streaker during the Super Bowl. [This man guaranteed a payout to himself by becoming
that streaker](https://www.yahoo.com/news/super-bowl-streaker-says-bet-211422994.html)

This is a relatively harmless example, but you could see how other markets might present much more harmful incentives. For
example, imaging a market betting on a new CEO for a given company. If the market seems pretty sure that the current
CEO will last throughout the year, they may place the likelhiood of a CEO change at $0.10. In the case of a new CEO
these contracts would each payout $1. A 10x return might be enough to incentive a market participant to assassinating
the current CEO to get the 10x payout. 

