from sklearn.model_selection import TimeSeriesSplit, cross_val_score, GridSearchCV
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV

## define scorer
def f1_positive(ys_truth, ys_pred):
    rpt = classification_report(ys_truth, ys_pred, output_dict = True)
    return rpt['YOUR_SPECIFIC_CLASS']['f1-score']

scorer_custom = make_scorer(f1_positive, greater_is_better=True)
skf = StratifiedKFold(n_splits = 5, shuffle = True, random_state = 7)
tscv = TimeSeriesSplit(n_splits=3)

lgb_clf = xgb.XGBClassifier()

tune_params = {
    'eta':[0.1],
    'n_estimators': [400],
    'max_depth': [6],
    'subsample': [0.8],
    'colsample_bytree': [0.9],
    'lambda':[0.8]}

fit_params = {'early_stopping_rounds':20,
              'eval_metric': 'roc_auc',
              'eval_set': [(X_val, y_val)],
              'verbose': 20
             }

gs = RandomizedSearchCV(estimator=lgb_clf,
                        param_distributions=tune_params,
                        n_iter=100,
                        n_jobs=1,
                        scoring=scorer_custom,
                        cv=skf,
                        random_state=1,
                        verbose=20)

print('Grid searching...')
gs.fit(X_train, y_train)

opt_params = gs.best_params_
lgb_clf.set_params(**opt_params)
# lgb_clf.fit(X_train, y_train,**fit_params)
lgb_clf.fit(X_train, y_train)

filename = 'LGBMClassifier.sav'
pickle.dump(lgb_clf, open(filename, 'wb'))
lgb_clf = pickle.load(open(filename, 'rb'))
print('Training accuracy: ', accuracy_score(y_train, lgb_clf.predict(X_train)))
print('F1 accuracy : ', f1_score(y_val, lgb_clf.predict(X_val)))
print('Validation accuracy: ', accuracy_score(y_val, lgb_clf.predict(X_val)))
