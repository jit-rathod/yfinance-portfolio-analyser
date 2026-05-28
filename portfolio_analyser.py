"""
╔══════════════════════════════════════════════════════════╗
║   Stock Market Portfolio Analyser using yfinance         ║
║   Author  : You                                          ║
║   Library : yfinance, pandas, numpy                      ║
║   Install : pip install yfinance pandas numpy            ║
╚══════════════════════════════════════════════════════════╝
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURATION — Change these to your preferred stocks
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PORTFOLIO = {
    'Apple'    : 'AAPL',
    'Microsoft': 'MSFT',
    'Google'   : 'GOOGL',
    'Amazon'   : 'AMZN',
    'Tesla'    : 'TSLA',
}

BENCHMARK   = '^GSPC'    # S&P 500
PERIOD      = "1y"       # 1 year of data
RISK_FREE   = 0.05       # 5% annual risk-free rate (approx US T-bill)
TRADING_DAYS= 252        # trading days in a year

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 1: Download Historical Price Data
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fetch_data(tickers_dict, benchmark, period="1y"):
    """
    Downloads adjusted closing prices for all portfolio stocks
    and the benchmark index.
    Returns a single DataFrame where each column is one asset.
    """
    print("\n📥 Downloading market data...")
    
    all_tickers = list(tickers_dict.values()) + [benchmark]
    
    # Download all at once (multi-threaded internally)
    raw = yf.download(all_tickers, period=period,
                      interval="1d", auto_adjust=True)
    
    # Keep only the "Close" price column
    prices = raw["Close"]
    
    # Rename columns from ticker to company name
    rename_map = {v: k for k, v in tickers_dict.items()}
    rename_map[benchmark] = "S&P 500"
    prices = prices.rename(columns=rename_map)
    
    # Drop any rows with all NaN (market holidays)
    prices = prices.dropna(how="all")
    
    print(f"   ✅ Downloaded {len(prices)} trading days of data")
    print(f"   📅 Date range: {prices.index[0].date()} to {prices.index[-1].date()}")
    
    return prices


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 2: Calculate Daily Returns
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def calculate_returns(prices):
    """
    Daily return = (Today Price - Yesterday Price) / Yesterday Price
    This tells us what % the stock moved each day.
    pandas .pct_change() does this automatically.
    """
    daily_returns = prices.pct_change().dropna()
    return daily_returns


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 3: Compute Performance Metrics
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def compute_metrics(prices, daily_returns, risk_free=0.05, trading_days=252):
    """
    Calculates key metrics for each stock:
    - Total Return   : overall gain/loss over the period
    - Annual Return  : annualised return (geometric)
    - Volatility     : annualised standard deviation of daily returns
    - Sharpe Ratio   : risk-adjusted return
                       (return above risk-free) / volatility
    - Max Drawdown   : largest peak-to-trough decline
    """
    metrics = {}
    
    for col in prices.columns:
        p = prices[col].dropna()
        r = daily_returns[col].dropna()
        
        # Total return: (end price / start price) - 1
        total_return = (p.iloc[-1] / p.iloc[0]) - 1
        
        # Annualised return using compound formula
        n_days = len(p)
        annual_return = (1 + total_return) ** (trading_days / n_days) - 1
        
        # Volatility: std dev of daily returns × sqrt(252)
        volatility = r.std() * np.sqrt(trading_days)
        
        # Sharpe Ratio: (annual return - risk-free rate) / volatility
        sharpe = (annual_return - risk_free) / volatility
        
        # Max Drawdown
        rolling_max  = p.cummax()  # running maximum
        drawdown     = (p - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        metrics[col] = {
            'Start Price'   : round(p.iloc[0], 2),
            'End Price'     : round(p.iloc[-1], 2),
            'Total Return'  : round(total_return * 100, 2),
            'Annual Return' : round(annual_return * 100, 2),
            'Volatility'    : round(volatility * 100, 2),
            'Sharpe Ratio'  : round(sharpe, 3),
            'Max Drawdown'  : round(max_drawdown * 100, 2),
        }
    
    return pd.DataFrame(metrics).T


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 4: Portfolio Performance
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def portfolio_performance(daily_returns, portfolio_cols):
    """
    Equal-weight portfolio: each stock gets 1/N of the capital.
    Portfolio daily return = average of individual daily returns.
    """
    port_daily = daily_returns[portfolio_cols].mean(axis=1)
    # Cumulative return: how $1 invested grows over time
    cumulative  = (1 + port_daily).cumprod()
    total_return = (cumulative.iloc[-1] - 1) * 100
    return port_daily, cumulative, total_return


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 5: Correlation Matrix
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def correlation_matrix(daily_returns, portfolio_cols):
    """
    Correlation tells you how much two stocks move together:
    +1.0 = always move together (perfectly correlated)
     0.0 = no relationship
    -1.0 = always move in opposite directions
    A well-diversified portfolio has LOW correlation between stocks.
    """
    return daily_returns[portfolio_cols].corr()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 6: Company Info Snapshot
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_company_snapshots(tickers_dict):
    """
    For each stock, get key company info from Yahoo Finance:
    market cap, P/E ratio, sector, number of employees.
    """
    print("\n🏢 Fetching company information...")
    snapshots = {}
    for name, ticker in tickers_dict.items():
        try:
            t = yf.Ticker(ticker)
            i = t.info
            snapshots[name] = {
                'Ticker'    : ticker,
                'Sector'    : i.get('sector', 'N/A'),
                'Market Cap': f"${i.get('marketCap', 0)/1e9:.1f}B",
                'P/E Ratio' : round(i.get('trailingPE', 0), 2),
                'Employees' : f"{i.get('fullTimeEmployees', 0):,}",
            }
        except Exception as e:
            snapshots[name] = {"Error": str(e)}
    return pd.DataFrame(snapshots).T


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STEP 7: Print the Report
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def print_report(prices, metrics, corr, port_return, bench_return, snapshots):
    sep = "═" * 65
    print(f"\n{sep}")
    print("  📊  STOCK MARKET PORTFOLIO ANALYSIS REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(sep)
    
    print("\n📌 COMPANY SNAPSHOTS")
    print(snapshots.to_string())
    
    print(f"\n{sep}")
    print("📈 PERFORMANCE METRICS")
    print(sep)
    print(metrics.to_string())
    
    print(f"\n{sep}")
    print("🔗 CORRELATION MATRIX (daily returns)")
    print("   [Values near +1.0 = highly correlated, near 0 = independent]")
    print(sep)
    print(corr.to_string())
    
    print(f"\n{sep}")
    print("⚖️  PORTFOLIO vs BENCHMARK")
    print(sep)
    
    portfolio_stocks = [c for c in metrics.index if c != "S&P 500"]
    best  = metrics.loc[portfolio_stocks, "Total Return"].idxmax()
    worst = metrics.loc[portfolio_stocks, "Total Return"].idxmin()
    
    print(f"  Equal-Weight Portfolio Return  : {port_return:+.2f}%")
    print(f"  S&P 500 Benchmark Return       : {bench_return:+.2f}%")
    print(f"  Alpha (Portfolio - Benchmark)  : {port_return - bench_return:+.2f}%")
    print(f"  Best Performer                 : {best}")
    print(f"  Worst Performer                : {worst}")
    print(sep)
    print("\n✅ Analysis Complete!")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN — Run Everything
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    # 1. Fetch data
    prices = fetch_data(PORTFOLIO, BENCHMARK, PERIOD)
    
    # 2. Calculate daily returns
    daily_returns = calculate_returns(prices)
    
    # 3. Compute metrics for all assets
    metrics = compute_metrics(prices, daily_returns, RISK_FREE, TRADING_DAYS)
    
    # 4. Portfolio vs benchmark
    portfolio_cols = list(PORTFOLIO.keys())
    port_daily, port_cumulative, port_return = portfolio_performance(
        daily_returns, portfolio_cols
    )
    bench_return = float(metrics.loc["S&P 500", "Total Return"])
    
    # 5. Correlation
    corr = correlation_matrix(daily_returns, portfolio_cols)
    
    # 6. Company info
    snapshots = get_company_snapshots(PORTFOLIO)
    
    # 7. Print report
    print_report(prices, metrics, corr, port_return, bench_return, snapshots)
