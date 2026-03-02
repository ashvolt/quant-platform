import os
import pandas as pd
import pandas_ta as ta


def load_raw_data(symbol: str):
    path = f"data/raw/market/{symbol}/ohlcv.parquet"
    return pd.read_parquet(path)


def save_features(symbol: str, df: pd.DataFrame):
    path = f"data/processed/features/{symbol}"
    os.makedirs(path, exist_ok=True)
    df.to_parquet(f"{path}/features.parquet")


def engineer_features(df: pd.DataFrame):
    df = df.sort_values("timestamp")

    # Moving averages
    df["sma_20"] = ta.sma(df["close"], length=20)
    df["ema_20"] = ta.ema(df["close"], length=20)

    # RSI
    df["rsi_14"] = ta.rsi(df["close"], length=14)

    # MACD
    macd = ta.macd(df["close"])
    df["macd"] = macd.iloc[:, 0]
    df["macd_signal"] = macd.iloc[:, 1]

    # Bollinger Bands (safe version)
    bb = ta.bbands(df["close"], length=20)
    print(bb.columns)
    print(bb.head())
    bb.columns = ["BBL_20_2.0_2.0", "BBM_20_2.0_2.0", "BBU_20_2.0_2.0","BBB_20_2.0_2.0","BBP_20_2.0_2.0"]
    df = pd.concat([df, bb], axis=1)

    df = df.dropna()

    return df


if __name__ == "__main__":
    symbol = "BTCUSDT"

    df = load_raw_data(symbol)
    df = engineer_features(df)
    save_features(symbol, df)

    print("Features generated successfully.")