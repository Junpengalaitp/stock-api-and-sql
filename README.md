# Design Documentation

## Requirements
* input: list of company names, exp: Apple, Amazon, Netflix, Facebook, Google
* output: the most volatile stock in csv format

## Technical implementation
* use command line args to pass the input, and output path(optional, save to current dir if not provide)
* use config mapping to map company name to symbol(exp: Apple: AAPL), if the company name is not configured, use lookup api to find the mapping between name(https://finnhub.io/docs/api/symbol-search)
* use quote api(https://finnhub.io/docs/api/quote) to find the latest quote time, in case of market close time and holidays
* use candle api(https://finnhub.io/docs/api/stock-candles) to find the candles of current and the previous trading day(in case there are weekends and holidays)
* last_close_price: close price of the 1440th candle
* current_price: close price of the current candle
* percentage_change: (current_price - last_close_price) / last_close_price
* use Python file system operations to save the output, (just 2 lines, if this is a bigger csv, it better be done by Pandas)

## Exceptions
* If there are any names in the input that is unable to find the symbol, print the error name to the console

## Unit Tests
* Test the symbol can be mapped from the company name
* Test the volatility is calculated correctly
* Test the previous trading day can be found in case of US holidays of weekends

## Quick Start
```
install requirements:
pip3 install -r requirements.txt

Simplest:
python3 find_most_volatile_stock.py "Apple, Amazon, Netflix, Facebook, Google" 

With output path:
python3 find_most_volatile_stock.py "Apple, Amazon, Netflix, Facebook, Google" "<PATH>"

Error input:
python3 find_most_volatile_stock.py "Apple,abcdesfadhgaoifdgqowfr" 
will print error to console: "cannot find symbol for name: abcdesfadhgaoifdgqowfr, please check the input"

```