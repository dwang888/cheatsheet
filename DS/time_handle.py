market_train_df['date'] = market_train_df['time'].dt.date
news_df['sourceTimestamp']= news_df['time'].dt.hour


market_train_df = market_train_df.loc[market_train_df['time'].dt.date>=datetime.date(2009,1,1)]