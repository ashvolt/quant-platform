import os
import requests
import pandas as pd

BASE_URL = "https://api.binance.com/api/v3/klines"


def fetch_ohlcv(symbol: str, interval: str, limit: int = 1000):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "num_trades",
        "taker_base_vol", "taker_quote_vol", "ignore"
    ])

    df = df[["open_time", "open", "high", "low", "close", "volume"]]

    df["timestamp"] = pd.to_datetime(df["open_time"], unit="ms")

    numeric_cols = ["open", "high", "low", "close", "volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)

    df = df[["timestamp", "open", "high", "low", "close", "volume"]]

    return df


def save_ohlcv(symbol: str, df: pd.DataFrame):
    path = f"data/raw/market/{symbol}"
    os.makedirs(path, exist_ok=True)
    df.to_parquet(f"{path}/ohlcv.parquet")


if __name__ == "__main__":
    symbol = "BTCUSDT"
    interval = "1h"

    df = fetch_ohlcv(symbol, interval)
    save_ohlcv(symbol, df)

    print("Data saved successfully.")