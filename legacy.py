# print(raw_wiki_df)
# wiki_df = raw_wiki_df.resample("W-MON").sum()
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

# print(stock_df)
# weekly_stock_df = stock_df.resample("W").sum()
# print(weekly_stock_df)

# print(raw_stock_df.columns.tolist())
# df.to_csv("stocks.csv", index=False)
