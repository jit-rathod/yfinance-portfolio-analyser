# Stock Market Portfolio Analyser

A comprehensive Stock Market Portfolio Analysis project built using Python and the `yfinance` package.

This project fetches historical market data, calculates financial metrics, evaluates portfolio performance, analyzes stock correlations, and visualizes gold price trends.

---

# Project Features

## Portfolio Analysis
- Download 1 year historical stock data
- Analyze multiple stocks simultaneously
- Compare portfolio performance against S&P 500 benchmark

## Financial Metrics
The project calculates:

- Total Return
- Annual Return
- Volatility
- Sharpe Ratio
- Maximum Drawdown

## Correlation Analysis
- Compare stock relationships
- Understand diversification
- Generate correlation matrix

## Portfolio Performance
- Equal-weight portfolio analysis
- Benchmark comparison with S&P 500
- Best and worst performer detection

## Company Information
Fetches:
- Sector
- Market Capitalization
- P/E Ratio
- Employee Count

## Gold Price Analysis
- Downloads gold futures data
- Plots gold price chart
- Visualizes market trends using matplotlib

---

# Technologies Used

- Python
- yfinance
- pandas
- numpy
- matplotlib

---

# Python Libraries

Install dependencies using:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install yfinance pandas numpy matplotlib
```

---

# How to Run

## Run Portfolio Analysis

```bash
python portfolio_analyser.py
```

## Run Gold Price Chart

```bash
python gold_chart.py
```

---

# Portfolio Analysis Workflow

1. Download historical stock data
2. Calculate daily returns
3. Compute financial metrics
4. Analyze correlations
5. Evaluate portfolio performance
6. Compare with benchmark
7. Generate report

---

# Stocks Used in Analysis

- Apple (AAPL)
- Microsoft (MSFT)
- Google (GOOGL)
- Amazon (AMZN)
- Tesla (TSLA)

Benchmark:
- S&P 500 (^GSPC)

---

# Sample Features Implemented

## Risk Metrics
- Volatility Calculation
- Sharpe Ratio
- Maximum Drawdown

## Financial Analysis
- Historical Price Analysis
- Return Calculations
- Portfolio Comparison

## Visualization
- Gold Price Chart
- Financial Trend Analysis

---

# Example Output

```text
STOCK MARKET PORTFOLIO ANALYSIS REPORT

Company Snapshots
Performance Metrics
Correlation Matrix
Portfolio vs Benchmark
Best Performer
Worst Performer
```

---

# Learning Outcomes

This project demonstrates:

- Financial data analysis
- Python package usage
- API-based stock market data extraction
- Portfolio performance evaluation
- Risk analysis
- Data visualization
- Real-world financial analytics

---

# Future Improvements

Possible enhancements:

- GUI Dashboard
- Real-time stock tracker
- Interactive graphs
- Machine learning predictions
- Portfolio optimization
- Export reports to PDF/Excel

---

# About yfinance

`yfinance` is a Python library used to fetch financial market data from Yahoo Finance.

It provides:
- Historical market data
- Company information
- Financial statements
- Recommendations
- Stock trends

---

# License

This project is licensed under the MIT License.
