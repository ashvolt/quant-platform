import requests
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

BINANCE_URL = "https://api.binance.com/api/v3/klines"


def fetch_ohlcv(symbol: str, interval: str = '1m', limit: int = 1000) -> pd.DataFrame:
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(BINANCE_URL, params=params, timeout=10)
    response.raise_for_status()

    cols = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ]

    df = pd.DataFrame(response.json(), columns=cols)

    df["timestamp"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]

    df[["open", "high", "low", "close", "volume"]] = \
        df[["open", "high", "low", "close", "volume"]].astype(float)

    df["symbol"] = symbol

    return df.sort_values("timestamp").reset_index(drop=True)

def validate_ohlcv(df: pd.DataFrame):
    if not df["timestamp"].is_monotonic_increasing:
        raise ValueError("Timestamps not sorted")

    if not df["timestamp"].is_unique:
        raise ValueError("Duplicate timestamps found")

    deltas = df["timestamp"].diff().dropna()
    expected = pd.Timedelta(minutes=1)

    if not (deltas == expected).all():
        raise ValueError("Missing or irregular candles")

def store_parquet(df: pd.DataFrame):
    symbol = df["symbol"].iloc[0]
    date = df["timestamp"].dt.date.iloc[-1]

    base = Path("data/raw/market")
    path = base / f"symbol={symbol}" / f"date={date}"
    path.mkdir(parents=True, exist_ok=True)

    df.drop(columns=["symbol"]).to_parquet(
        path / "ohlcv.parquet",
        engine="pyarrow",
        index=False
    )
if __name__ == "__main__":
    for sym in ["BTCUSDT", "ETHUSDT"]:
        df = fetch_ohlcv(sym)
        validate_ohlcv(df)
        store_parquet(df)
        print(f"{sym}: {len(df)} rows ingested")
