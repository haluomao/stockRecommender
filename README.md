# A simple stock recommender referring to several indexes such as MACD, RSI and so on.

Usage:

    python macd.py TYPE DAYS
    
--TYPE: buy/sell
$python macd.py buy 3
    # Recommend out the stock codes to buy in latest 3 days.
$python macd.py sell 5
    # stock to sell in latest 5 days.

    python macd.py update UPDATE_TYPE
    
--UPDATE_TYPE: all/add
$python macd.py update add
    # Update recent days incrementally, will not download all stock data.

