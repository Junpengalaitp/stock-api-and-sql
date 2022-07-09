# Design Documentation

## Requirements
* input: list of company names, exp:  Apple, Amazon, Netflix, Facebook, Google
* output: the most volatile stock in csv format

## Technical implementation
* use command line args to pass the input, and output path(optional, save to current dir if not provide)
* use symbol lookup api to find the mapping between name(https://finnhub.io/docs/api/symbol-search)
* use candle api(https://finnhub.io/docs/api/stock-candles) to find the latest 1min candle and the 1min candle 24 hours ago
* last_close_price: close price of the candle 24 hours ago
* current_price: close price of the current candle
* percentage_change: (current_price - last_close_price) / last_close_price
* use Python file system operations to save the output, (just 2 lines, if this is a bigger csv, could use Pandas)

## Exceptions
* If there are any names in the input that is unable to find the symbol, print the error name to the console

## Unit Tests
* Test the symbol can be mapped from the company name
* Test the volatility is calculated correctly(truncate to 2 decimal points)

## Quick Start
```
Simplest:
python3 find_most_volatile_stock.py "Apple, Amazon, Netflix, Facebook, Google" 

With output path:
python3 find_most_volatile_stock.py "Apple, Amazon, Netflix, Facebook, Google" "./stock-api-and-sql"

Error input:
python3 find_most_volatile_stock.py "Aoogle" 
will print error to console: "Cannot find stock symbol for name: Aoogle"

```