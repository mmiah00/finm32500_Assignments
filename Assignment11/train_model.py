import json
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score
from xgboost import XGBClassifier
from feature_engineering import market_data_df


featuresjson = 'features_config.json'
modeljson = 'model_params.json'

folder = './Assignment11/'
features = json.load(open(folder+featuresjson, 'r'))
model_params = json.load(open(folder+modeljson, 'r'))

C, max_iter = model_params['LogisticRegression'].values()
X, y = market_data_df[['close']].values, market_data_df[['Label']].values.ravel()
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
logistic_model = LogisticRegression(C=C, max_iter=max_iter)
logistic_model.fit(X_train, y_train)
acc_log = round(accuracy_score(y_test, logistic_model.predict(X_test)) * 100, 2)
prc_log = round(precision_score(y_test, logistic_model.predict(X_test)) * 100, 2)
rec_log = round(recall_score(y_test, logistic_model.predict(X_test)) * 100, 2)
print(acc_log, prc_log, rec_log)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
n_estimators, learning_rate, max_depth = model_params['XGBClassifier'].values()
bst = XGBClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, objective='binary:logistic')
bst.fit(X_train, y_train)
preds = bst.predict(X_test)
acc_xgb = round(accuracy_score(y_test, preds)*100, 2)
prc_xgb = round(precision_score(y_test, preds)*100, 2)
rec_xgb = round(recall_score(y_test, preds)*100, 2)
print(acc_xgb, prc_xgb, rec_xgb)

num_folds = 5
kf = KFold(n_splits=num_folds, shuffle=True, random_state=42)
cross_val_results = cross_val_score(bst, X, y, cv=kf)
print(cross_val_results.round(2), cross_val_results.mean())

