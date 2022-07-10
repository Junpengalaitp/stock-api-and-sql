from collections import defaultdict
from datetime import datetime

import holidays
from typing import List

import requests
from loguru import logger

token = "cb4nii2ad3i5f7mlav70"
base_url = "https://finnhub.io/api/v1"

NAME_TO_SYMBOL_MAPPING = {"apple": "AAPL", "amazon": "AMZN", "facebook": "META", "google": "GOOGL", "netflix": "NFLX"}
us_holidays = holidays.US()


def most_volatile_stock_to_csv(names: str, path: str = None):
    symbol_list = map_names_to_symbols(names)
    if not symbol_list:
        return
    logger.info(f"mapped names:{names} to symbols:{symbol_list}")
    stock_prices = retrieve_candles(symbol_list)
    most_volatile_stock_info = {}
    for stock_price in stock_prices:
        info = calculate_volatility(stock_price)
        if len(most_volatile_stock_info) == 0 or abs(info["percentage_change"]) > abs(
                most_volatile_stock_info["percentage_change"]):
            most_volatile_stock_info = info
    export_csv(most_volatile_stock_info, path)


def export_csv(most_volatile_stock_info: dict, path: str = None):
    header = "stock_symbol,percentage_change,current_price,last_close_price"
    csv_str = header + "\n" + most_volatile_stock_info["symbol"] + "," + str(
        round(most_volatile_stock_info["percentage_change"], 2)) \
              + "," + str(most_volatile_stock_info["current_price"]) + "," + str(
        most_volatile_stock_info["last_close_price"])
    logger.info(csv_str)
    file_name = "most_volatile_stock.csv"
    if path:
        path = path.lstrip()
        if not path.endswith("/"):
            file_name = path + "/" + file_name
        else:
            file_name = path + file_name
    f = open(file_name, "w")
    f.write(csv_str)
    f.close()
    logger.info(f"wrote to path: {file_name}")


def calculate_volatility(stock_price) -> dict:
    res = {}
    res["symbol"] = stock_price["symbol"]
    res["current_price"] = stock_price["latest"]["c"][0]
    res["last_close_price"] = stock_price["previous"]["c"][0]
    res["percentage_change"] = (res["current_price"] - res["last_close_price"]) / res["current_price"] * 100
    return res


def retrieve_candles(symbol_list: List[str]) -> List[dict]:
    res = []
    if not symbol_list:
        return res
    end_time = symbol_latest_quote_minute_timestamp(symbol_list[0])
    logger.info(f"last timestamp is {end_time}")
    for symbol in symbol_list:
        latest_candle = retrieve_one_candle(symbol, end_time)
        prev_candle = retrieve_one_candle(symbol, timestamp_1_trading_day_ago(end_time))
        dc = {}
        dc["symbol"] = symbol
        dc["latest"] = latest_candle
        dc["previous"] = prev_candle
        res.append(dc)
    return res


def timestamp_1_trading_day_ago(timestamp: int) -> int:
    """
    :return: the timestamp 1 trading day ago, if it is in weekend or a US public holiday, recursive call
    this function until it's not
    """
    timestamp -= 86400
    if not is_weekend_or_US_holiday(timestamp):
        return timestamp
    return timestamp_1_trading_day_ago(timestamp)


def is_weekend_or_US_holiday(timestamp: int) -> bool:
    dt_obj = datetime.fromtimestamp(timestamp)
    return dt_obj.weekday() in (5, 6) or dt_obj in us_holidays


def retrieve_one_candle(symbol: str, end_time: int):
    url = f'{base_url}/stock/candle?symbol={symbol}&resolution=1&from={end_time}&to={end_time}&&token={token}'
    logger.info(f"get candle of {symbol} by calling url: {url}")
    r = requests.get(url)
    return r.json()


def symbol_latest_quote_minute_timestamp(symbol: str) -> int:
    """
    :returns: whole minute timestamp
    """
    url = f'{base_url}/quote?symbol={symbol}&token={token}'
    r = requests.get(url)
    timestamp = r.json()["t"]
    return timestamp - (timestamp % 1440)


def map_names_to_symbols(names: str) -> List[str]:
    """
    :param names:
    :return: successfully mapped names, if there is any invalid name, return empty list
    """
    name_list = names.split(",")
    res = []
    for name in name_list:
        symbol = map_name_to_symbol(name.strip())
        if not symbol:
            return []
        res.append(symbol)
    return res


def map_name_to_symbol(name: str) -> str:
    if NAME_TO_SYMBOL_MAPPING.get(name.lower()):
        return NAME_TO_SYMBOL_MAPPING[name.lower()]
    try:
        r = requests.get(f'{base_url}/search?q={name}&token={token}')
        res = r.json()["result"][0]["symbol"]
    except:
        logger.error(f"cannot find symbol for name: {name}, please check the input")
        return ""
    return res


if __name__ == '__main__':
    import sys
    args = sys.argv
    if len(args) <= 1:
        logger.error("please provide a comma separated company names")
    else:
        path = args[2] if len(args) == 3 else None
        most_volatile_stock_to_csv(args[1], path)
