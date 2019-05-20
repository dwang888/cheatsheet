#### output feature importance
clf = clf.fit(X_all, Y_all)
if isinstance(clf, RandomForestClassifier):
    df_imp = pd.DataFrame(clf.feature_importances_, index = X_all.columns,
                                    columns=['IMPORTANCE']).sort_values('IMPORTANCE', ascending=False)
    print(df_imp.iloc[:10])

if isinstance(clf, xgb.XGBClassifier):
    df_imp = pd.DataFrame( list(clf.get_booster().get_fscore().items() ), columns=['FEATURE', 'IMPORTANCE']  )
    df_imp = df_imp.sort_values('IMPORTANCE', ascending=False)
    print(df_imp.iloc[:10]
    
