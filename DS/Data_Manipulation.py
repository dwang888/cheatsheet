#### increase data
start_dt = "2017-01-01"
end_dt = (datetime.datetime.strptime(start_dt, '%Y-%m-%d') + datetime.timedelta(days=5)).strftime('%Y-%m-%d')


######### handle inf and null
df = df.loc[( df['x'].notnull() ) & ( np.isfinite(df['x']) )]
df['x'] = df['x'].replace([np.inf, -np.inf], mean_x)

     A    B   C  D
0  NaN  2.0 NaN  0
1  3.0  4.0 NaN  1
2  NaN  NaN NaN  5
>>> df.dropna(axis=1, how='all')
     A    B  D
0  NaN  2.0  0
1  3.0  4.0  1
2  NaN  NaN  5

######### is null
pd.isnull(YOUR_VARIABLE)

######### merge df
def join_dfs(ldf, rdf):
    cols_to_use = rdf.columns.difference(ldf.columns)
    res = pd.merge(ldf, rdf[cols_to_use], left_index=True, right_index=True, how='inner')
    return res
df_merged = reduce(join_dfs, dfs)

res = pd.merge(df1, df2, left_on=column_left, right_on=column_right, how='inner')
market_df = pd.merge(market_df, news_df, how='left', left_on=['date', 'assetCode'], right_on=['firstCreated', 'assetCodes'])

#### copy value
market_train_df = market_train_orig.copy()


#set value in dataframe
df.set_value(index, 'row_name', some_value)

#### drop duplicate
df1 = df1.drop_duplicates(subset=['COL1_DROPPED', 'COL2_DROPPED'], keep='first', inplace=False)

#### select value
market_train_df = market_train_df.loc[market_train_df['close_open_ratio'] > 0.5]


#### rename
df1 = df1.rename(columns={'old_col1':'new_col1', 'old_col2':'new_col2'})

#### sort
df1 = df1.sort_values(by=['col1', 'col2', 'col3'])


### groupby and sort
df_count = df.groupby('sub_cause').count()
df_count = df_count.sort_values('claim_number', ascending=False)

#### groupby and operation
data.groupby(['month', 'item']).agg({'duration':sum,      # find the sum of the durations for each group
                                     'network_type': "count", # find the number of network type entries
                                     'date': 'first'})    # get the first date per group

#### count and sort
df_dnb_tiern.groupby('KEY')['SOME_COL'].count().reset_index(name='count').sort_values(['count'],ascending=False).head(20)


#### transform pd
df['Most_Common_Price'] = df.groupby('Item').Price.transform(lambda x: x.value_counts().idxmax())
     Item  Price  Minimum  Most_Common_Price
0  Coffee      1        1                  2
1  Coffee      2        1                  2
2  Coffee      2        1                  2
3     Tea      3        3                  4
4     Tea      4        3                  4
5     Tea      4        3                  4
market_obs_df['moving_average_7_day'] = market_obs_df.groupby('assetCode')['close'].transform(lambda x: x.rolling(window=7).mean())
market_obs_df['rolling_average_close_std'] = market_obs_df.groupby('assetCode')['close'].transform('std')


#### fillna a column using another column in same shape
df[COLM_OLD] = df[COLM_OLD].fillna(df[COLM_NEW])

#### scale
from sklearn.preprocessing import StandardScaler
scaler_in = StandardScaler()
data_in = scaler_in.fit_transform(data_in)

#### column wise divsion
market_train_df['close_open_ratio'] = np.abs(market_train_df['close']/market_train_df['open'])

#### remove outliers
def remove_outliers(data_frame, column_list, low=0.02, high=0.98):
    for column in column_list:
        this_column = data_frame[column]
        quant_df = this_column.quantile([low,high])
        low_limit = quant_df[low]
        high_limit = quant_df[high]
        data_frame[column] = data_frame[column].clip(lower=low_limit, upper=high_limit)
    return data_frame

#### column wise processing
news_df['assetCodesLen'] = news_df['assetCodes'].map(lambda x: len(x))


#### text similarity
def compute_similarity(v1, v2):
    # sim = -spatial.distance.cosine(v1,v2)# higher cosine mean lower similarity
    # sim = -spatial.distance.euclidean(v1,v2)# higher euclidean mean lower similarity

    # v1 = np.where(v1 > 0, 1, 0)
    # v2 = np.where(v2 > 0, 1, 0)
    # sim = np.dot(v1,v2)# higher the better; BUT ONLY for 0-1 vector
    # sim = jaccard_similarity_score(v1,v2)# higher the jaccard; the better similarity
    sim = -spatial.distance.cosine(v1, v2)
    # sim = -spatial.distance.euclidean(v1, v2)
    return sim
