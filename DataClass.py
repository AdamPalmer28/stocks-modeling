"""

"""
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

class StockData:
    "Class for data handelling given a stock ticker"
    def __init__(self, ticker: str, start = '2018-01-01', end = '2022-08-01', interval='1d'):

        self.ticker = ticker # stock ticker
        
        self.start = start
        self.end = end
        self.time_interval = interval # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

        self.data = yf.Ticker(self.ticker).history(start = self.start,
                                    end = self.end,
                                    interval = self.time_interval,
                                    actions = False)

        self.basic_analysis() # runs basic analysis 

    def basic_analysis(self):
        "Runs basic analysis on stock data"
        # growth ratio
        self.data['prev growth'] = self.data["Close"] / self.data["Close"].shift(1)
        self.data['next growth'] = self.data["Close"].shift(-1) / self.data["Close"]
        self.data['Increases'] = 0
        self.data['Increases'][self.data['next growth'] > 1] = 1
        # Simple MA
        self.data['30 MA'] = self.data['Close'].rolling(30).mean() # 30 point moving average
        self.data['10 MA'] = self.data['Close'].rolling(10).mean() # 10 point moving average
        
    # ==================================================
    # Financial measurements 
    # ==================================================

    def MACD(sef, fast = 12, slow = 26, signal = 9):
        "Apply MACD measure"
        self.data['MACD'] = self.data['Close'].ewm(span=fast).mean() - self.data['Close'].ewm(span=slow).mean()
        self.data['signal'] = self.data['MACD'].ewm(span=signal).mean()

    def ATR(self, n = 14):
        "function to calculate True Range and Average True Range"
        df = self.data.copy()
        df["H-L"] = df["High"] - df["Low"]
        df["H-PC"] = abs(df["High"] - df["Close"].shift(1))
        df["L-PC"] = abs(df["Low"] - df["Close"].shift(1))
        df["TR"] = df[["H-L","H-PC","L-PC"]].max(axis=1, skipna=False)
        df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
        self.data['ATR'] = df['ATR']

    def Boll_Band(self, n=14):
        "Calculate Bollinger Band"
        self.data = self.data.copy()
        self.data["MB"] = self.data["Close"].rolling(n).mean()
        self.data["UB"] = self.data["MB"] + 2*self.data["Close"].rolling(n).std(ddof=0)
        self.data["LB"] = self.data["MB"] - 2*self.data["Close"].rolling(n).std(ddof=0)
        self.data["BB_Width"] = self.data["UB"] - self.data["LB"]

    def RSI(self, n=14):
        "Calculate RSI"
        df = self.data.copy()
        df["change"] = df["Close"] - df["Close"].shift(1)
        df["gain"] = np.where(df["change"]>=0, df["change"], 0)
        df["loss"] = np.where(df["change"]<0, -1*df["change"], 0)
        df["avgGain"] = df["gain"].ewm(alpha=1/n, min_periods=n).mean()
        df["avgLoss"] = df["loss"].ewm(alpha=1/n, min_periods=n).mean()
        df["rs"] = df["avgGain"]/df["avgLoss"]
        df["rsi"] = 100 - (100/ (1 + df["rs"]))
        self.data['rsi'] = df['rsi'] # adds RSI col to data

    # =======================================
    # Plotter
    # =======================================

    def plot(self):
        "Basic plotter to visulise data"
        pass


if __name__ == '__main__':
    tsla = StockData('TSLA')
    #tsla.RSI()
    print(tsla.data.head(10))

