import yfinance as yf
from mwviews.api import PageviewsClient
import pandas as pd

pd.set_option("display.max_columns", 20)

tickers = []

with open("tickers.txt", "r") as file:
    for line in file.readlines():
        tickers.append(line.strip())


# Sends a descriptive User-Agent header with every request
p = PageviewsClient(user_agent="<fenton@fentonk.com> wiki analysis")


groups = [
    [["V", "MA"], ["Visa_Inc.", "Mastercard"]],
    # [["HD", "LOW"], ["The_Home_Depot", "Lowe's"]],
    # [["KO", "PEP"], ["The_Coca-Cola_Company", "PepsiCo"]],
]

wiki_df = None

for g in groups:
    for i in range(len(g[0])):
        result = p.article_views(
            "en.wikipedia",
            g[1],
            granularity="daily",
            start="20260223",
            end="20260502",
        )

        weekly_views = {}
        raw_wiki_df = pd.DataFrame.from_dict(result, orient="index")
        # print(raw_wiki_df)
        wiki_df = raw_wiki_df.resample("W-MON").sum()

        # for (
        #     key,
        #     value,
        # ) in result.items():
        #     week = key.isocalendar()[1]

        #     if week in weekly_views:
        #         for ticker, views in value.items():
        #             if ticker in weekly_views[week]:
        #                 weekly_views[week][ticker] += views
        #             else:
        #                 weekly_views[week][ticker] = views
        #     else:
        #         weekly_views[week] = value


# print(weekly_views)

# print(wiki_df)

raw_stock_df = yf.download(
    groups[0][0], interval="1wk", start="2026-02-16", end="2026-05-02"
)

stock_df = raw_stock_df[["Close"]].copy()
stock_df = stock_df["Close"].diff()
# print(stock_df)
# weekly_stock_df = stock_df.resample("W").sum()
# print(weekly_stock_df)

# print(raw_stock_df.columns.tolist())
# df.to_csv("stocks.csv", index=False)

combined_df = stock_df.join(wiki_df)
print(combined_df)
