#### rolling window
market_train_df['moving_average_7_day'] = market_train_df.groupby('assetCode')['close'].transform(lambda x: x.rolling(window=7).mean())

#### ewm
ewma = pd.Series.ewm
market_train_df['ewma'] =  market_train_df.groupby('assetCode')['close'].transform(lambda x : ewma(x, span=30).mean())

