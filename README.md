# Delta Hedging Simulation — Vanilla Call Option

Dynamic delta hedging simulation of a vanilla call option using Black-Scholes in Python.

## Product Description
Simulation of a delta-neutral hedging strategy on a vanilla call option,
rebalanced weekly over 1 year to replicate the option payoff.

- **Underlying spot** : 100
- **Strike** : 100 (ATM)
- **Maturity** : 1 year
- **Volatility** : 20%
- **Risk-free rate** : 2%
- **Rebalancing** : weekly (52 steps/year)

## Methodology
- Underlying modelled via **Geometric Brownian Motion (GBM)**
- Delta computed analytically via **Black-Scholes formula**
- At each step : rebalance the share position, update cash account with interest
- PnL tracked as : hedge portfolio value − option mark-to-market

## Key Results
- Residual hedging error : **~8% of initial premium**
- PnL leakage explained by **gamma exposure** between rebalancing dates
- The more frequent the rebalancing, the smaller the residual error

## Key Takeaway
Perfect replication is only achievable with continuous rebalancing.
In practice, discrete hedging introduces a residual PnL driven by gamma —
the core risk of any delta-hedging strategy.

## Tech Stack
- Python 3
- NumPy (math, erf)

## Author
Mathis Sebilleau — [LinkedIn](https://www.linkedin.com/in/mathis-sebilleau)
