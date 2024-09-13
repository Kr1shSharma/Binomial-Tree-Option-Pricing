from monte_carlo import price_american_option

import pytest
from monte_carlo import price_american_option

def test_price_american_option():
    # Example parameters
    initial_price = 100
    strike_price = 100
    time_horizon = 1
    risk_free_rate = 0.05
    volatility = 0.2
    option_type = 'call'
    
    # Call the function
    price = price_american_option(initial_price, strike_price, time_horizon, risk_free_rate, volatility, option_type)
    
    # Example assertion (you need to adjust this based on expected output)
    assert price >= 0  # Ensure that the price is non-negative
