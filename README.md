Author: Yvanna Nseke

# Constrained Markowitz Portfolio Optimization — In-Sample and Rolling Out-of-Sample Backtest

This project implements a **constrained minimum-variance (Markowitz) portfolio** and compares it to an **equal-weight benchmark** using both **in-sample analysis** and a **rolling out-of-sample backtest** (to mitigate look-ahead bias).

---

## Objective

Build a long-only portfolio that minimizes variance under realistic constraints:

- Fully invested: sum(w) = 1  
- Long-only: w >= 0  
- Concentration cap: w_i <= 20%  

We evaluate whether the optimized portfolio delivers **risk reduction (volatility / drawdowns)** compared to a simple benchmark across multiple market regimes.

---

## Universe

A small, sector-diversified equity universe:

- AAPL (Technology)  
- MSFT (Technology)  
- JPM (Financials)  
- XOM (Energy)  
- PFE (Healthcare)  
- KO (Consumer Staples)  

---

## Methodology

### 1. Data Acquisition
Daily adjusted close prices are downloaded for all assets to ensure consistency and correct treatment of dividends and splits. Dates are aligned and missing observations removed.

### 2. Return Computation
Daily returns are computed from price series and used for both statistical estimation and portfolio performance evaluation.

### 3. Exploratory Analysis
We visualize price trajectories and return dynamics to inspect volatility regimes, outliers, and potential structural patterns before modeling.

### 4. Estimation of μ and Σ
Expected returns and the covariance matrix are estimated from historical returns and annualized using standard market conventions.

### 5. Correlation Structure
The correlation matrix is analyzed to understand dependence across assets and assess diversification potential.

### 6. Constrained Markowitz Optimization
We solve a quadratic minimum-variance optimization problem under realistic constraints:
- fully invested portfolio  
- long-only weights  
- maximum 20% allocation per asset  
The problem is solved using **CVXPY**.

### 7. Optimized Weights Analysis
We analyze the resulting allocation to interpret diversification, concentration, and the relationship between weights and asset risk characteristics.

### 8. Portfolio Performance Computation
Portfolio returns are computed as the weighted sum of asset returns and used to construct cumulative performance curves.

### 9. Equal-Weight Benchmark
We compare results with an equally weighted portfolio to provide a robust baseline independent of estimation.

### 10. Result Summary
We evaluate portfolios through cumulative performance and visual comparison, highlighting differences in volatility, drawdowns, and overall growth dynamics.

### 11. Limitations and Out-of-Sample Validation
In-sample optimization may lead to overfitting. To address this, we implement a rolling out-of-sample backtest where parameters are estimated only using past data and applied to future periods.

---

## Results (High Level)

- The minimum-variance portfolio exhibits **lower volatility and smaller drawdowns**  
- It may **underperform in strong bull markets** (defensive profile)  
- Rolling weights highlight **estimation instability**  
- Out-of-sample results provide a more **realistic assessment of performance**  

---

## Implementation

The project is implemented in two complementary formats:

- **Jupyter Notebook (`OptiMarkowitz.ipynb`)**  
  - Exploratory analysis  
  - Visualizations  
  - Detailed reporting  

- **Python Script (`OptimizeMarkowitz.py`)**  
  - Modular class-based implementation  
  - Markowitz optimization  
  - Rolling backtest  
  - Benchmark comparison  
  - Visualization of performance and weights  

This separation reflects standard quantitative research workflows.

---

## Repository Structure

- `OptiMarkowitz.ipynb` : main notebook (analysis + report)  
- `OptimizeMarkowitz.py` : modular Python implementation  
- `requirements.txt` : dependencies  

---

## Installation

```bash
pip install -r requirements.txt
