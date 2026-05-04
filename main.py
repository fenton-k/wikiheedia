import yfinance as yf
from mwviews.api import PageviewsClient
import pandas as pd
import pickle

pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 1000)

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
            start="20250502",
            end="20260502",
        )

        wiki_df = pd.DataFrame.from_dict(result, orient="index")

raw_stock_df = yf.download(
    groups[0][0], interval="1d", start="2025-05-02", end="2026-05-02"
)

stock_df = raw_stock_df[["Close"]].copy()
stock_df = stock_df["Close"]

combined_df = stock_df.join(wiki_df)


with open("df.pkl", "wb") as f:
    pickle.dump(combined_df, f)


# combined_df["Visa_z"] = (
#     combined_df["Visa_Inc."] - combined_df["Visa_Inc."].mean()
# ) / combined_df["Visa_Inc."].std()

# combined_df["Mastercard_z"] = (
#     combined_df["Mastercard"] - combined_df["Mastercard"].mean()
# ) / combined_df["Mastercard"].std()

# combined_df["supposition"] = (
#     (combined_df["MA"] > combined_df["V"])
#     & (combined_df["Mastercard"] > combined_df["Visa_Inc."])
# ) | (
#     (combined_df["MA"] < combined_df["V"])
#     & (combined_df["Mastercard"] < combined_df["Visa_Inc."])
# )

# combined_df["supposition_2"] = (
#     (combined_df["MA"] > combined_df["V"])
#     & (combined_df["Mastercard_z"] > combined_df["Visa_z"])
# ) | (
#     (combined_df["MA"] < combined_df["V"])
#     & (combined_df["Mastercard_z"] < combined_df["Visa_z"])
# )
# print(combined_df)
