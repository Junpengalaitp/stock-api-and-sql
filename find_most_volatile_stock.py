import requests

token = "cb4nii2ad3i5f7mlav70";

if __name__ == '__main__':

    # Register new webhook for earnings
    r = requests.get(f'https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=1&from=1631022248&to=1631627048&&token={token}')
    res = r.json()
    print(res)

