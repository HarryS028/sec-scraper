import yfinance as yf
import pandas as pd

msft = yf.Ticker("MSFT")
info = msft.info

# earnings, 
# quarterly_earnings
# balance_sheet, 
# quarterly_balance_sheet
# cashflow, 
# quarterly_cashflow
# financials, 
# quarterly_financials

# input_df = pd.read_excel("trouble_companies.xlsx")

# ticker_str = str(list(input_df['Yahoo ticker'])).replace(",", "")[1: -1]
# tickers = yf.Tickers("MSFT")

# for t in input_df['Yahoo ticker']:
#     df = tickers.tickers.t.financials


# main_function([1,0,1,0], upload spreadsheet):
#     if position 1 = 1 then 
#         earnings
#     if position 2 = 1 then: 
#         quarterly earnings

# ticker_str = tickers.MSFT.earnings

print(info)