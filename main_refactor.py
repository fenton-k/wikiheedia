import pickle
import pandas as pd

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 10)
pd.set_option("display.width", 1000)

# with open("df.pkl", "rb") as f:
#     df1 = pickle.load(f)


def get_buys(df, stocks):
    # semi-random number. We look ~basically quarterly
    lookback = 56

    # calcluate z scores
    for ticker, name in stocks.items():
        df[f"{ticker}_z"] = (df[name] - df[name].rolling(lookback).mean()) / df[
            name
        ].rolling(lookback).std()

        df[f"{ticker}_7d_profit"] = df[ticker].diff(periods=-5)

    # print(df)

    buys = []

    # calculate buys
    for ticker, name in stocks.items():
        buys_df = df[df[f"{ticker}_z"] > 3]

        for other_ticker in stocks:
            # print(other_ticker)
            if ticker == other_ticker:
                continue
            else:
                # continue
                buys_df = buys_df[buys_df[f"{other_ticker}_z"] < 3]
                buys_df = buys_df.drop(f"{other_ticker}_7d_profit", axis=1)

        buys.append(buys_df)

    return buys
