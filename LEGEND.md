## Method and Assumptions

We analyze repositories of the **open-source** cryptocurrencies hosted on github to compare the activity levels. Due to the approach there are several limitations. Since in many cases the cryptocurrency organizations will have multiple repositories we consider repositories related to protocol development only, e.g. there are tens of different bitcoin wallets and they are not counting towards activity on BTC protocol itself, or as another example only the protocol-related work on [Cardano](https://github.com/input-output-hk) is considered. For forked currencies there is no separation of pre-fork activity vs post-fork activity, i.e. BCH will have all history related to BTC pre-fork. Similarly if BCH is pulling some changes from BTC these are shown as original BCH commits. Finally we do not account for the size of the commit - one line change or 100+ lines submitted in one commit have the same weight.

TL/DR: List of limitations and assumptions:
- Open-source and github only
- Forks get credit for all commits history prior to the fork - no separation of pre-fork activity
- Repositories related to wallets, websites, tutorials are ignored - protocol-related code only
- Mergers are considered as original commits
- The size of the commit is ignored


## Calculation method

We analyze all commits and extract the number of unique contributors per week of activity. We then apply a moving average (16 weeks or 4mo) period to emphasize the trend. We also calculate the percentage of developers who made more than 5 commits. Then the similar calculation is done for commits - we calculate the number of commits per week and use 16-weeks moving average to show the trend.

## Table Legend

* Market cap in $MM
* Price in $
* Age of repository since first commit in days
* Total number of commits
* Avg number of commits/week
* The number above divided by the market cap
* 16 wks moving average of commits/week
* Number of unique developers
* Percent of developers with more than 5 contributions
* Avg number of unique developers per week
* The number above divided by the market cap
* 16 wks moving average of dev/week
* List of considered repos

## Plot Legend

First row shows the time series for commits/week and developers per week. Once again this is the 16-weeks moving average, otherwise the data is too noisy and trend is not clear.

Second row is for average number of commits/week and devs/week vs market cap. The top 10% and bottom 10% are highlighted by blue and red.
