import unittest

from find_most_volatile_stock import map_name_to_symbol, map_names_to_symbols, timestamp_1_trading_day_ago


class MyTestCase(unittest.TestCase):
    def test_map_name_to_symbol(self):
        res = map_name_to_symbol("apple")
        print(res)
        self.assertEqual("AAPL", res)  # add assertion here

    def test_map_names_to_symbols(self):
        names = " Apple, Amazon, Netflix, Facebook, Google"
        res = map_names_to_symbols(names)
        print(res)
        self.assertEqual(['AAPL', 'AMZN', 'NFLX', 'META', 'GOOGL'], res)

    def test_timestamp_1_day_ago(self):
        timestamp = timestamp_1_trading_day_ago(1657310400)
        print(timestamp)
        self.assertEqual(1657224000, timestamp)

    def test_timestamp_1_day_ago_holiday(self):
        independent_day = 1657008900 # 2022-07-04
        timestamp = timestamp_1_trading_day_ago(independent_day)
        print(timestamp)
        self.assertEqual(1656663300, timestamp)


if __name__ == '__main__':
    unittest.main()
