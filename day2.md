# 📅 Day 2 – Market Data Ingestion & OHLCV Understanding

## 🎯 Goal of Day 2

The objective of Day 2 was to **understand and implement market data ingestion**, specifically:

* What **OHLCV data** is
* How raw market data becomes **structured time-series data**
* How to fetch, store, and reason about this data programmatically
* How this fits into a **quantitative trading system**

This is the **foundation layer** of any quant / trading platform.

---

## 🧠 Big Picture (Plain English)

Before trading, predicting, or backtesting:

> **We must first answer:**
> “What actually happened in the market, at each point in time?”

Day 2 is about **capturing reality** in a format machines can analyze.

---

## 📊 What is OHLCV?

**OHLCV** represents market price movement for a given time interval.

| Term       | Meaning                    | Example                    |
| ---------- | -------------------------- | -------------------------- |
| **Open**   | Price at start of interval | 9:15 AM price              |
| **High**   | Highest price in interval  | Day’s peak                 |
| **Low**    | Lowest price in interval   | Day’s bottom               |
| **Close**  | Price at end of interval   | 9:30 AM price              |
| **Volume** | Quantity traded            | Number of shares/contracts |

### Example (1-minute candle)

```text
09:15 – 09:16
Open: 100
High: 102
Low: 99
Close: 101
Volume: 12,000
```

This single row summarizes **hundreds or thousands of trades**.

---

## ⏱ What Does “Interval” Mean?

The **interval** defines *how we compress time*.

| Interval | Meaning                  |
| -------- | ------------------------ |
| `1m`     | One candle per minute    |
| `5m`     | One candle per 5 minutes |
| `1h`     | One candle per hour      |
| `1d`     | One candle per day       |

📌 **Why interval matters:**
Strategies behave *very differently* on 1-minute vs daily data.

---

## 🔄 What Are We Doing in Code?

### Step 1: Fetch Raw Market Data

We call a function like:

```python
fetch_ohlcv(symbol, interval)
```

Conceptually:

> “Give me historical price movement for **this asset**, grouped by **this time window**.”

---

### Step 2: Convert to Structured Table

The raw API data is converted into a **tabular time-series**:

```text
timestamp | open | high | low | close | volume
```

Why this matters:

* Machines think in **tables**
* Quants think in **time-indexed matrices**
* kdb+/qdb+ is *built exactly for this structure*

---

### Step 3: Store as `ohlcv.parquet`

#### What is `ohlcv.parquet`?

`parquet` is a **columnar storage format**, optimized for analytics.

Think of it as:

* CSV ❌ slow, large
* JSON ❌ messy
* Parquet ✅ fast, compressed, analytics-friendly

📌 **Why Parquet is important for quants:**

* Faster reads
* Less memory
* Perfect for time-series analytics
* Common in institutional pipelines

---

## 🧩 Why This Matters for kdb+ / qdb+

kdb+ is designed for **exactly this type of data**:

```text
time | symbol | open | high | low | close | volume
```

Day 2 prepares us to later:

* Load OHLCV into kdb+
* Run ultra-fast time-series queries
* Compare Python vs q performance
* Simulate real trading desks

---

## ⚠️ Error Encountered & Learning

### Error:

```text
TypeError: fetch_ohlcv() missing 1 required positional argument: 'interval'
```

### What it taught:

* Functions require **all mandatory parameters**
* Market data **cannot exist without time granularity**
* “Price” alone is meaningless without **when**

This reinforced the mental model:

> **Time is the backbone of quantitative systems**

---

## 🧠 Mental Model (Important)

By end of Day 2, the system looks like this:

```
Market Exchange
     ↓
Raw Trades
     ↓
OHLCV Aggregation (by interval)
     ↓
Structured Table
     ↓
Parquet Storage
     ↓
Future Analytics / kdb+ / Strategies
```

Everything later (signals, ML, alpha, execution) **depends on this layer**.

---

## ✅ What We Achieved Today

✔ Understood OHLCV deeply
✔ Learned why interval is mandatory
✔ Built first market data ingestion pipeline
✔ Stored time-series data properly
✔ Built quant-grade mental models
✔ Prepared ground for kdb+ integration

---
