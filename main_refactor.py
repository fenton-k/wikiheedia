import pickle
import pandas as pd

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 10)
pd.set_option("display.width", 1000)

with open("df.pkl", "rb") as f:
    df = pickle.load(f)

# semi-random number. We look ~basically quarterly
lookback = 56

stocks = {"V": "Visa_Inc.", "MA": "Mastercard"}

# calcluate z scores
for ticker, name in stocks.items():
    df[f"{ticker}_z"] = (df[name] - df[name].rolling(lookback).mean()) / df[
        name
    ].rolling(lookback).std()

    df[f"{ticker}_7d_profit"] = df["V"].diff(periods=-5)

# print(df)

# calculate buys
for ticker, name in stocks.items():
    buys_df = df[df[f"{ticker}_z"] > 2]

    for other_ticker in stocks:
        # print(other_ticker)
        if ticker == other_ticker:
            continue
        else:
            # continue
            buys_df = buys_df[buys_df[f"{other_ticker}_z"] < 2]

    print(buys_df)

# print(visa_buys)

# MA_buys = df[df["MA_z"] > 2]
# MA_buys = MA_buys[MA_buys["V_z"] < 2]
# print(MA_buys)


# df.to_csv("zscores.csv", index=False)
