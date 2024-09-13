import numpy as np
import pandas as pd
import yfinance as yf

# Monte Carlo Simulation for Stock Price Paths
def simulate_price_paths(initial_price, volatility, time_horizon, num_simulations, num_steps=252):
    dt = time_horizon / num_steps
    price_paths = np.zeros((num_steps + 1, num_simulations))
    price_paths[0] = initial_price

    for i in range(1, num_steps + 1):
        z = np.random.normal(0, 1, num_simulations)
        price_paths[i] = price_paths[i - 1] * np.exp((0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * z)
    
    return price_paths

# Binomial Tree Pricing Model for American Options
def price_american_option(initial_price, strike_price, time_horizon, risk_free_rate, volatility, option_type, num_steps=1000):
    dt = time_horizon / num_steps
    u = np.exp(volatility * np.sqrt(dt))  # Up factor
    d = 1 / u  # Down factor
    q = (np.exp(risk_free_rate * dt) - d) / (u - d)  # Risk-neutral probability

    # Initialize price tree
    price_tree = np.zeros((num_steps + 1, num_steps + 1))
    price_tree[0, 0] = initial_price

    for i in range(1, num_steps + 1):
        for j in range(i + 1):
            price_tree[j, i] = initial_price * (u ** (i - j)) * (d ** j)

    # Initialize option value tree
    option_tree = np.zeros_like(price_tree)

    # Payoff at maturity
    for j in range(num_steps + 1):
        if option_type == 'call':
            option_tree[j, num_steps] = max(0, price_tree[j, num_steps] - strike_price)
        elif option_type == 'put':
            option_tree[j, num_steps] = max(0, strike_price - price_tree[j, num_steps])

    # Backward induction
    for i in range(num_steps - 1, -1, -1):
        for j in range(i + 1):
            hold_value = np.exp(-risk_free_rate * dt) * (q * option_tree[j, i + 1] + (1 - q) * option_tree[j + 1, i + 1])
            exercise_value = max(0, price_tree[j, i] - strike_price) if option_type == 'call' else max(0, strike_price - price_tree[j, i])
            option_tree[j, i] = max(hold_value, exercise_value)

    return option_tree[0, 0]

# Backtesting a Moving Average Crossover Strategy
def backtest_strategy(ticker, start_date, end_date):
    data = fetch_historical_data(ticker, start_date, end_date)

    # Calculate moving averages
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()

    # Create buy/sell signals
    data['Signal'] = 0
    data['Signal'][50:] = np.where(data['50_MA'][50:] > data['200_MA'][50:], 1, 0)
    data['Position'] = data['Signal'].diff()

    # Backtest returns
    initial_cash = 100000
    shares = 0
    cash = initial_cash

    for i in range(1, len(data)):
        if data['Position'].iloc[i] == 1:  # Buy signal
            shares = cash // data['Close'].iloc[i]
            cash -= shares * data['Close'].iloc[i]
        elif data['Position'].iloc[i] == -1:  # Sell signal
            cash += shares * data['Close'].iloc[i]
            shares = 0

    portfolio_value = cash + shares * data['Close'].iloc[-1]

    # Ensure 'dates' and 'prices' are returned correctly
    result = {
        'dates': data.index.strftime('%Y-%m-%d').tolist(),  # Convert index to list of strings
        'prices': data['Close'].tolist()  # Convert 'Close' prices to list
    }
    return result, portfolio_value

# Fetch Historical Data using yfinance
def fetch_historical_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data[['Close']]
