import json
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score
from xgboost import XGBClassifier
from feature_engineering import FeatureEngineering

class ModelRunner:
    def __init__(self, folder='./Assignment11/'):
        self.folder = folder
        featuresjson = 'features_config.json'
        modeljson = 'model_params.json'
        self.features = json.load(open(folder + featuresjson, 'r'))
        self.model_params = json.load(open(folder + modeljson, 'r'))
        self.X = market_data_df[['close']].values
        self.y = market_data_df[['Label']].values.ravel()

    def run_logistic(self):
        C, max_iter = self.model_params['LogisticRegression'].values()
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, random_state=42)

        logistic_model = LogisticRegression(C=C, max_iter=max_iter)
        logistic_model.fit(X_train, y_train)

        acc_log = round(accuracy_score(y_test, logistic_model.predict(X_test)) * 100, 2)
        prc_log = round(precision_score(y_test, logistic_model.predict(X_test)) * 100, 2)
        rec_log = round(recall_score(y_test, logistic_model.predict(X_test)) * 100, 2)

        print(acc_log, prc_log, rec_log)
        return logistic_model

    def run_xgb(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, random_state=42)

        n_estimators, learning_rate, max_depth = self.model_params['XGBClassifier'].values()
        bst = XGBClassifier(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            objective='binary:logistic'
        )

        bst.fit(X_train, y_train)
        preds = bst.predict(X_test)

        acc_xgb = round(accuracy_score(y_test, preds) * 100, 2)
        prc_xgb = round(precision_score(y_test, preds) * 100, 2)
        rec_xgb = round(recall_score(y_test, preds) * 100, 2)

        print(acc_xgb, prc_xgb, rec_xgb)
        return bst

    def run_cross_val(self, model, num_folds=5):
        kf = KFold(n_splits=num_folds, shuffle=True, random_state=42)
        cross_val_results = cross_val_score(model, self.X, self.y, cv=kf)
        print(cross_val_results.round(2), cross_val_results.mean())
        return cross_val_results

if __name__ == "__main__":
    fe = FeatureEngineering()
    market_data_df = fe.run()
    runner = ModelRunner()

    bst = runner.run_xgb()
    runner.run_logistic()       
    runner.run_cross_val(bst)    


