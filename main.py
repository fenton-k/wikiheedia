import yfinance as yf
from mwviews.api import PageviewsClient
import pandas as pd
import pickle
from main_refactor import get_buys

pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 1000)

stock_start_day = "2025-05-02"
stock_end_day = "2026-05-02"
wiki_start_day = stock_start_day.replace("-", "")
wiki_end_day = stock_end_day.replace("-", "")

# tickers = []

# with open("tickers.txt", "r") as file:
#     for line in file.readlines():
#         tickers.append(line.strip())


def get_buys(df, stocks):
    # semi-random number. We look ~basically quarterly
    lookback = 56
    # print(df)

    # calcluate z scores
    for ticker, name in stocks.items():
        df[f"{ticker}_z"] = (df[name] - df[name].rolling(lookback).mean()) / df[
            name
        ].rolling(lookback).std()

        df[f"{ticker}_5d_fwd"] = df[ticker].shift(-5) / df[ticker] - 1
        df[f"{ticker}_5d_excess"] = df[f"{ticker}_5d_fwd"] - df["SPY_5d_fwd"]
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
                buys_df = buys_df.drop(f"{other_ticker}_5d_fwd", axis=1)

        buys.append(buys_df)

    return buys


# Sends a descriptive User-Agent header with every request
p = PageviewsClient(user_agent="<fenton@fentonk.com> wiki analysis")

groups = [
    {"V": "Visa_Inc.", "MA": "Mastercard"},
    {"HD": "The_Home_Depot", "LOW": "Lowe's"},
    {"KO": "The_Coca-Cola_Company", "PEP": "PepsiCo"},
    {"CVX": "Chevron_Corporation", "XOM": "ExxonMobil"},
    {"UPS": "United_Parcel_Service", "FDX": "FedEx"},
    {"WM": "Waste_Management_(corporation)", "RSG": "Republic_Services"},
    {"DAL": "Delta_Air_Lines", "AAL": "American_Airlines", "UAL": "United_Airlines"},
    {"MAR": "Marriott_International", "HLT": "Hilton_Worldwide"},
    {"CME": "CME_Group", "ICE": "Intercontinental_Exchange"},
    {"AMT": "American_Tower", "CCI": "Crown_Castle", "SBAC": "SBA_Communications"},
    {
        "AVB": "AvalonBay_Communities",
        "CPT": "Camden_Property_Trust",
        "EQR": "Equity_Residential",
    },
    # {"AON": "Aon_(company)", "AJG": "Arthur_J.Gallagher&Co.", "MSRH": "Marsh_McLennan"},
    {"CLX": "Clorox", "CHD": "Church&Dwight"},
    {"BAC": "Bank_of_America", "C": "Citigroup", "JPM": "JPMorgan_Chase"},
    {"T": "AT&T", "VZ": "Verizon"},
    # {"BKR": "Baker_Hughes", "HAL": "Halliburton", "SLB": "SLB"},
    {"AMD": "Advanced_Micro_Devices", "INTC": "Intel"},
    {"AZO": "AutoZone", "ORLY": "O'Reilly_Auto_Parts"},
    {"SPGI": "S&P_Global", "MCO": "Moody's_Corporation"},
    {"CSX": "CSX_Corporation", "NSC": "Norfolk_Southern_Railway"},
    {"CDNS": "Cadence_Design_Systems", "SNPS": "Synopsys"},
    {
        "CCL": "Carnival_Corporation&_plc",
        "RCL": "Royal_Caribbean_Group",
        "NCLH": "Norwegian_Cruise_Line_Holdings",
    },
    {"TJX": "TJX_Companies", "ROST": "Ross_Stores"},
    {"LEN": "Lennar", "DHI": "D._R._Horton"},
    {"LMT": "Lockheed_Martin", "NOC": "Northrop_Grumman"},
    {"APD": "Air_Products", "LIN": "Linde_plc"},
    {"SYK": "Stryker_Corporation", "ZBH": "Zimmer_Biomet"},
]

output = {}

spy = yf.download("SPY", interval="1d", start=stock_start_day, end=stock_end_day)[
    ["Close"]
]
spy.columns = ["SPY"]

spy_5d = spy.shift(-5) / spy - 1
spy_5d.columns = ["SPY_5d_fwd"]

for g in groups:
    wiki_df = None

    result = p.article_views(
        "en.wikipedia",
        g.values(),
        granularity="daily",
        start=wiki_start_day,
        end=wiki_end_day,
    )

    wiki_df = pd.DataFrame.from_dict(result, orient="index")

    # print(list(g.keys()))

    raw_stock_df = yf.download(
        list(g.keys()), interval="1d", start=stock_start_day, end=stock_end_day
    )

    stock_df = raw_stock_df[["Close"]].copy()
    stock_df = stock_df["Close"]

    combined_df = stock_df.join(wiki_df).join(spy_5d)

    # print(combined_df.head())

    buys = get_buys(combined_df, g)
    for buy in buys:
        # print(buy)
        columns = buy.columns
        for column in columns:
            if "5d_excess" in column:
                output[column] = buy[column].sum()

# print(output)

wins = 0
loses = 0

for key, value in output.items():
    if value > 0:
        wins += 1
    if value < 0:
        loses += 1

print(f"winrate: {wins/(wins+loses)}")
