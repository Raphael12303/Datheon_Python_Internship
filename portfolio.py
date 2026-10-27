import csv
import os

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

def get_current_price(ticker):
    if HAS_YFINANCE:
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")['Close'].iloc[-1]
            return float(price)
        except Exception:
            pass
    return None

def main():
    portfolio = {}
    print("=== Investment Portfolio Tracker ===")
    print("Enter your holdings (type 'done' when finished).\n")

    # 2. Store portfolio positions in a dictionary structure
    while True:
        ticker = input("Enter stock ticker (e.g., AAPL, TSLA) or 'done': ").strip().upper()
        if ticker == 'DONE':
            break
        if not ticker:
            continue

        try:
            shares = float(input(f"Enter quantity of shares for {ticker}: "))
            buy_price = float(input(f"Enter buy price per share for {ticker} ($): "))
        except ValueError:
            print("Invalid input. Please enter numbers for shares and price.")
            continue

        portfolio[ticker] = {
            'shares': shares,
            'buy_price': buy_price
        }

    if not portfolio:
        print("No portfolio data entered. Exiting.")
        return

    summary_data = []
    total_invested = 0.0
    total_current_value = 0.0

    print("\nFetching current prices and calculating metrics...\n")

    for ticker, data in portfolio.items():
        shares = data['shares']
        buy_price = data['buy_price']
        
        # 4. Calculate total invested capital
        invested = shares * buy_price
        total_invested += invested

        # 3. Look up current ticker prices
        current_price = get_current_price(ticker)
        if current_price is None:
            try:
                current_price = float(input(f"Could not fetch live price for {ticker}. Enter current price manually ($): "))
            except ValueError:
                current_price = buy_price

        current_value = shares * current_price
        total_current_value += current_value

        # Calculate percentage gain/loss per holding
        gain_loss_dollar = current_value - invested
        gain_loss_pct = (gain_loss_dollar / invested) * 100 if invested > 0 else 0.0

        summary_data.append({
            'Ticker': ticker,
            'Shares': shares,
            'Buy Price': buy_price,
            'Current Price': round(current_price, 2),
            'Invested Capital': round(invested, 2),
            'Current Value': round(current_value, 2),
            'Gain/Loss ($)': round(gain_loss_dollar, 2),
            'Gain/Loss (%)': round(gain_loss_pct, 2)
        })

    # 5. Write results into 'portfolio_summary.csv' using Python's built-in csv module
    csv_filename = "portfolio_summary.csv"
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), csv_filename)
    fieldnames = ['Ticker', 'Shares', 'Buy Price', 'Current Price', 'Invested Capital', 'Current Value', 'Gain/Loss ($)', 'Gain/Loss (%)']

    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_data:
            writer.writerow(row)

    # Print Execution Summary
    print("=" * 45)
    print("          PORTFOLIO SUMMARY")
    print("=" * 45)
    print(f"Total Invested Capital: ${total_invested:,.2f}")
    print(f"Total Current Value:    ${total_current_value:,.2f}")
    total_diff = total_current_value - total_invested
    total_pct = (total_diff / total_invested) * 100 if total_invested > 0 else 0.0
    print(f"Total Gain/Loss:        ${total_diff:,.2f} ({total_pct:.2f}%)")
    print("-" * 45)
    print(f"Summary successfully saved to: {csv_path}")
    print("=" * 45)

if __name__ == "__main__":
    main()