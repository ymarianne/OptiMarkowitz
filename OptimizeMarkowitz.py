import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import cvxpy as cp
import plotly.io as pio
import webbrowser

pio.renderers.default = "browser"

class MarkowitzModel:
    def __init__(self, tickers, start, end, max_weight = 0.20):
        self.tickers = tickers
        self.start = start
        self.end = end
        self.max_weight = max_weight

        self.returns = None
        self.log_returns = None
        self.prices = None

        self.mu = None
        self.sigma = None
        self.weights = None

    def download_data(self):
        """Télécharge les données Yahoo Finance."""
        data_raw = yf.download(self.tickers, self.start, self.end)

        if data_raw.empty:
            raise ConnectionError("Échec du téléchargement Yahoo Finance. Data vide.")

        self.prices = data_raw["Close"]
        return self.prices
    
    def plot_prices(self):
        """Tracer l'évolution des prix de chaque action."""
        if self.prices is None:
            raise ValueError("Il faut d'abord appeler download_data().")
        fig = px.line(self.prices, title="Évolution des prix de clôture")
        fig.show()
        return fig

    def compute_returns(self):
        if self.prices is None:
            raise ValueError("Il faut appeler download_data() avant compute_returns()")

        self.returns = self.prices.pct_change().dropna()
        self.log_returns = np.log(self.prices / self.prices.shift(1)).dropna()

        self.mu = self.log_returns.mean()
        self.sigma = self.log_returns.cov()

        return self.returns, self.log_returns


    def optimize(self):
        if self.sigma is None:
            raise ValueError("Il faut appeler compute_returns() avant optimize()")

        n = len(self.log_returns.columns)
        w = cp.Variable(n)

        objective = cp.Minimize(cp.quad_form(w, self.sigma.values))
        constraints = [w >= 0, w <= self.max_weight, cp.sum(w) == 1]

        prob = cp.Problem(objective, constraints)
        prob.solve()

        if w.value is None:
            raise RuntimeError("Optimisation échouée. CVXPY n'a pas trouvé de solution.")

        self.weights = pd.Series(w.value, index=self.log_returns.columns)
        return self.weights

    def plot_performance(self):
        if self.weights is None:
            raise ValueError("Il faut appeler optimize() avant plot_performance()")

        #Portefeuille optimise
        port_opt = self.returns.dot(self.weights)
        perf_opt = (1 + port_opt).cumprod()

        #Portefeuille equipondere
        n = len(self.tickers)
        w_eq = np.ones(n) / n
        port_eq = self.returns.dot(w_eq)
        perf_eq = (1 + port_eq).cumprod()

        df = pd.DataFrame({
            "Portefeuille optimisé": perf_opt,
            "Portefeuille équipondéré": perf_eq
        })

        fig = px.line(df, title="Performance du portefeuille optimisé")
        fig.show()

        return perf_opt
    
    def backtest_rolling(self, window=252):
        if self.returns is None or self.log_returns is None:
            raise ValueError("Il faut appeler compute_returns() avant backtest().")

        dates = self.returns.index
        portfolio_returns = []
        weights_history = []
        weights_dates = []

        n = len(self.tickers)

        for t in range(window, len(dates)):
            past_log_returns = self.log_returns.iloc[t-window:t]
            sigma_t = past_log_returns.cov()

            w = cp.Variable(n)

            objective = cp.Minimize(cp.quad_form(w, sigma_t.values))
            constraints = [
                w >= 0,
                w <= self.max_weight,
                cp.sum(w) == 1
            ]

            problem = cp.Problem(objective, constraints)
            problem.solve()

            if w.value is None:
                continue

            weights_t = w.value

            # rendement réalisé au jour t avec les poids calculés sur le passé
            ret_t = self.returns.iloc[t].values @ weights_t

            portfolio_returns.append(ret_t)
            weights_history.append(weights_t)
            weights_dates.append(dates[t])

        bt_returns = pd.Series(portfolio_returns, index=weights_dates, name="Markowitz rolling")

        weights_history = pd.DataFrame(
            weights_history,
            index=weights_dates,
            columns=self.tickers
        )

        return bt_returns, weights_history
    
    def plot_weights(self, weights_history):
        if weights_history is None or weights_history.empty:
            raise ValueError("weights_history est vide.")

        fig = px.area(
            weights_history,
            title="Evolution of Portfolio Weights (Rolling Backtest)",
            labels={
                "index": "Rebalancing Date",
                "value": "Weight",
                "variable": "Ticker"
            }
        )

        fig.show()
        return fig


if __name__ == "__main__":
    model = MarkowitzModel(
        ["AAPL", "MSFT", "JPM", "XOM", "PFE", "KO"],
        "2020-01-01",
        "2026-01-01"
    )

    model.download_data()
    model.compute_returns()

    # In-sample
    weights = model.optimize()
    print("\nPoids optimaux in-sample :")
    print(weights)

    model.plot_performance()

    # Rolling backtest Markowitz
    bt, weights_history = model.backtest_rolling(window=252)
    perf_bt = (1 + bt).cumprod()

    # Benchmark équipondéré sur la même période que le backtest
    n = len(model.tickers)
    w_eq = np.ones(n) / n
    bt_eq = model.returns.loc[bt.index].dot(w_eq)
    perf_eq = (1 + bt_eq).cumprod()

    # Comparaison backtest Markowitz vs équipondéré
    df_backtest = pd.DataFrame({
        "Markowitz rolling": perf_bt,
        "Equal-weight": perf_eq
    })

    fig = px.line(
        df_backtest,
        title="Backtest rolling : Markowitz vs Equal-weight",
        labels={
            "index": "Date",
            "value": "Performance cumulée",
            "variable": "Portefeuille"
        }
    )
    fig.show()

    # Evolution des poids
    model.plot_weights(weights_history)