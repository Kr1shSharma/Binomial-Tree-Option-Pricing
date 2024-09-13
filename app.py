from flask import Flask, render_template, request
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from monte_carlo import simulate_price_paths, price_american_option, backtest_strategy

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        initial_price = float(request.form['initial_price'])
        volatility = float(request.form['volatility'])
        time_horizon = float(request.form['time_horizon'])
        num_simulations = int(request.form['num_simulations'])

        price_paths = simulate_price_paths(initial_price, volatility, time_horizon, num_simulations)

        fig = go.Figure()
        for i in range(min(num_simulations, 10)):
            fig.add_trace(go.Scatter(x=list(range(price_paths.shape[0])), y=price_paths[:, i], mode='lines', name=f'Simulation {i+1}'))

        fig.update_layout(title='Monte Carlo Simulation: Stock Price Paths', xaxis_title='Time Step', yaxis_title='Stock Price')
        graph_html = fig.to_html(full_html=False)

        return render_template('simulation.html', graph_html=graph_html)
    except Exception as e:
        return f"<h2>Error: {str(e)}</h2>"

@app.route('/price-option', methods=['POST'])
def price_option():
    try:
        initial_price = float(request.form['initial_price'])
        strike_price = float(request.form['strike_price'])
        time_horizon = float(request.form['time_horizon'])
        risk_free_rate = float(request.form['risk_free_rate'])
        volatility = float(request.form['volatility'])
        option_type = request.form['option_type']

        if option_type in ['call', 'put']:
            option_price = price_american_option(initial_price, strike_price, time_horizon, risk_free_rate, volatility, option_type)
            return f"<h2>The estimated price of the American {option_type} option is: ${option_price:.2f}</h2>"
        else:
            return "<h2>Invalid option type</h2>"
    except Exception as e:
        return f"<h2>Error: {str(e)}</h2>"

@app.route('/backtest', methods=['POST'])
def backtest():
    try:
        ticker = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        # Fetch historical data and backtest data
        historical_data_dict, portfolio_value = backtest_strategy(ticker, start_date, end_date)

        # Convert dictionary to DataFrame for plotting
        historical_data = pd.DataFrame({
            'dates': pd.to_datetime(historical_data_dict['dates']),
            'prices': historical_data_dict['prices']
        })

        # Plot historical data
        fig_historical = px.line(historical_data, x='dates', y='prices', title=f'Historical Data for {ticker}')
        historical_graph_html = fig_historical.to_html(full_html=False)

        # Plot backtest data
        fig_backtest = go.Figure()
        fig_backtest.add_trace(go.Scatter(x=historical_data['dates'], y=historical_data['prices'], mode='lines', name='Price'))

        fig_backtest.update_layout(title=f'Backtesting {ticker}', xaxis_title='Date', yaxis_title='Price')
        backtest_graph_html = fig_backtest.to_html(full_html=False)

        return render_template('backtest.html', historical_graph_html=historical_graph_html, backtest_graph_html=backtest_graph_html)
    except Exception as e:
        return f"<h2>Error: {str(e)}</h2>"

if __name__ == '__main__':
    app.run(debug=True)
