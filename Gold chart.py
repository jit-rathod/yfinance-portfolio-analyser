import yfinance as yf
import matplotlib.pyplot as plt

# Download gold price data (Gold Futures)
gold = yf.download("GC=F", start="2025-01-01", end="2026-01-01")

# Display first few rows
print(gold.head())

# Plot closing price
plt.figure(figsize=(10,5))
plt.plot(gold['Close'])

plt.title("Gold Price Chart")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.grid(True)

plt.show()
