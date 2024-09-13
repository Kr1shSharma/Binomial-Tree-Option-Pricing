# Option Pricing and Backtesting Web Application

This project is a web application that allows users to run Monte Carlo simulations, price American options, and backtest trading strategies. It uses Flask for the web framework and integrates with Plotly for visualizations.

## Features

- **Monte Carlo Simulation:** Simulate stock price paths and visualize the results.
- **American Option Pricing:** Calculate the price of American call and put options using the Binomial Tree model.
- **Backtesting Strategy:** Backtest a moving average crossover strategy and visualize historical data and backtest results.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Kr1shSharma/Option-Pricing.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd Option-Pricing
    ```

3. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. **Run the Flask application:**

    ```bash
    python app.py
    ```

5. **Open your web browser and go to:**

    ```
    http://127.0.0.1:5000
    ```

## Usage

1. **Monte Carlo Simulation:** Enter the initial stock price, volatility, time horizon, and number of simulations, then click "Run Simulation" to view the simulated price paths.

2. **American Option Pricing:** Enter the required parameters and click "Price Option" to get the option price.

3. **Backtest Strategy:** Enter the stock ticker symbol, start date, and end date, then click "Backtest Strategy" to view the historical data and backtest results.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Flask for the web framework.
- Plotly for the data visualization.
- yfinance for fetching historical stock data.
- NumPy and Pandas for numerical computations and data handling.

