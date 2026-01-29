Author: Yvanna Nseke

# Constrained Markowitz Portfolio Optimization (Minimum Variance) — Rolling Out-of-Sample Backtest

This project implements a **constrained minimum-variance (Markowitz) portfolio** and compares it to an **equal-weight benchmark** using a **rolling out-of-sample backtest** (to mitigate look-ahead bias).

## Objective
Build a long-only portfolio that minimizes variance under realistic constraints:
- Fully invested: sum(w) = 1
- Long-only: w >= 0
- Concentration cap: w_i <= 20%

We evaluate whether the optimized portfolio delivers risk reduction (volatility / drawdowns) compared to a simple benchmark across multiple market regimes.

## Universe
A small, sector-diversified equity universe:
- AAPL, MSFT, JPM, XOM, PFE, KO

## Methodology
1. Download daily **adjusted close** prices (dividends/splits accounted for)
2. Compute daily returns
3. Estimate covariance on a rolling window
4. Solve the constrained minimum-variance problem with **CVXPY**
5. Backtest out-of-sample between rebalancing dates
6. Report performance and risk metrics:
   - annualized return / volatility
   - Sharpe ratio (rf = 0 assumption unless specified)
   - maximum drawdown
   - cumulative performance

## Results (high level)
- The minimum-variance portfolio tends to exhibit **lower volatility and smaller drawdowns**
- It may lag in strong bull markets (defensive profile)
- Rolling weights highlight estimation instability and motivate transaction cost modeling

> See the notebook for full figures and metrics.

## Repository structure
- `OptiMarkowitz.ipynb` : main notebook (report + backtest)
- `requirements.txt` : Python dependencies

## Installation
```bash
pip install -r requirements.txt
```

## How to run
jupyter notebook OptiMarkowitz.ipynb
