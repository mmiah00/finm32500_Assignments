from feature_engineering import FeatureEngineering
from signal_generator import Signals
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
try:
    from xgboost import XGBClassifier
except Exception:
    XGBClassifier = None


class Backtest:
    def __init__(self, df, initial_cash=100000, position_size=1):
        self.df = df.copy()
        self.initial_cash = initial_cash
        self.position_size = position_size
        self.equity_curve = None
        self.positions_history = None

    def simulate(self, signal_col):
        """Simulate a simple strategy using per-row signals in `signal_col`.

        BUY -> buy `position_size` units; SELL -> sell `position_size` units; HOLD -> do nothing.
        Positions tracked per ticker. Portfolio value = cash + sum(position * last_price).
        """
        df = self.df
        # work on a reset index copy so positional slicing is reliable even with non-unique datetime index
        df2 = df.reset_index()
        tickers = df2['ticker'].unique()
        positions = {t: 0 for t in tickers}
        cash = float(self.initial_cash)
        equity = []
        pos_hist = []
        # iterate through rows in chronological order using positional index
        for i in range(len(df2)):
            row = df2.iloc[i]
            sig = row.get(signal_col, 'HOLD')
            price = float(row['close'])
            ticker = row['ticker']
            if sig == 'BUY':
                positions[ticker] += self.position_size
                cash -= price * self.position_size
            elif sig == 'SELL':
                positions[ticker] -= self.position_size
                cash += price * self.position_size
            # mark-to-market using last available price per ticker up to current position
            recent = df2.loc[:i].groupby('ticker').tail(1).set_index('ticker')['close'].to_dict()
            pv = cash
            for t, qty in positions.items():
                last_price = recent.get(t, np.nan)
                if not np.isnan(last_price):
                    pv += qty * float(last_price)
            equity.append(pv)
            pos_hist.append(positions.copy())

        # align equity series with original DataFrame index
        equity_series = pd.Series(equity, index=df.index)
        self.equity_curve = equity_series
        self.positions_history = pos_hist
        return equity_series

    def plot(self, title='Equity Curve', save_path=None, show=True):
        if self.equity_curve is None:
            raise RuntimeError('No equity curve. Run simulate() first.')
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(self.equity_curve.index, self.equity_curve.values, label='Portfolio Equity')
        ax.set_title(title)
        ax.set_xlabel('Time')
        ax.set_ylabel('Equity')
        ax.grid(True)
        ax.legend()
        fig.tight_layout()
        if save_path:
            fig.savefig(save_path, dpi=150)
        if show:
            plt.show()
        return fig


def plot_equity_curves(curves: dict, title='Equity Curves', save_path=None, show=True):
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, series in curves.items():
        s = pd.Series(series).sort_index()
        ax.plot(s.index, s.values, label=name)
    ax.set_title(title)
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


def plot_confusion(y_true, y_pred, labels=(0, 1), title='Confusion Matrix', save_path=None, show=True):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    fig, ax = plt.subplots(figsize=(6, 6))
    disp.plot(ax=ax)
    ax.set_title(title)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


def plot_prediction_distribution(probas, bins=50, title='Predicted Probabilities', save_path=None, show=True):
    probas = np.array(probas)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(probas, bins=bins, density=True, alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel('Predicted probability')
    ax.set_ylabel('Density')
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


def plot_feature_importance(model, feature_names, top_n=10, title='Feature Importance', save_path=None, show=True):
    fig, ax = plt.subplots(figsize=(8, 4))
    if hasattr(model, 'feature_importances_'):
        imp = np.array(model.feature_importances_)
        idx = np.argsort(imp)[-top_n:][::-1]
        ax.barh(np.array(feature_names)[idx], imp[idx])
        ax.set_title(title)
    elif hasattr(model, 'coef_'):
        coef = np.abs(np.array(model.coef_).ravel())
        idx = np.argsort(coef)[-top_n:][::-1]
        ax.barh(np.array(feature_names)[idx], coef[idx])
        ax.set_title(title + ' (abs coefficients)')
    else:
        ax.text(0.5, 0.5, 'No importance available for this model', ha='center')
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    if show:
        plt.show()
    return fig


if __name__ == "__main__":
    fe = FeatureEngineering(folder='./')
    market_data_df = fe.run()

    # features and label
    feature_cols = ['1 day', '3 day', '5 day', 'SMA 5', 'SMA 10', 'RSI', 'Signal Line', 'Z-score']
    df_features = market_data_df[feature_cols + ['Label']].dropna()

    X = df_features[feature_cols].values
    y = df_features['Label'].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # load model params
    try:
        params = json.load(open('model_params.json', 'r'))
    except Exception:
        params = {}

    log_params = params.get('LogisticRegression', {})
    log_model = LogisticRegression(**log_params)
    log_model.fit(X_train, y_train)

    if XGBClassifier is not None:
        xgb_params = params.get('XGBClassifier', {})
        xgb_model = XGBClassifier(**xgb_params)
        xgb_model.fit(X_train, y_train)
    else:
        xgb_model = None

    # generate probabilities across full DataFrame (only where features are present)
    X_full = market_data_df[feature_cols]
    valid_idx = X_full.dropna().index
    probas_log = pd.Series(index=market_data_df.index, dtype=float)
    probas_log.loc[valid_idx] = log_model.predict_proba(X_full.loc[valid_idx].values)[:, 1]
    low_log, high_log = 0.45, 0.55
    market_data_df['log signals'] = pd.Series(np.where(probas_log >= high_log, 'SELL', np.where(probas_log <= low_log, 'BUY', 'HOLD')), index=market_data_df.index).fillna('HOLD')

    probas_xgb = pd.Series(index=market_data_df.index, dtype=float)
    if xgb_model is not None:
        probas_xgb.loc[valid_idx] = xgb_model.predict_proba(X_full.loc[valid_idx].values)[:, 1]
    low_xgb, high_xgb = 0.4, 0.6
    market_data_df['bst signals'] = pd.Series(np.where(probas_xgb >= high_xgb, 'SELL', np.where(probas_xgb <= low_xgb, 'BUY', 'HOLD')), index=market_data_df.index).fillna('HOLD')

    # run backtests
    bt_xgb = Backtest(market_data_df)
    eq_xgb = bt_xgb.simulate('bst signals')

    bt_log = Backtest(market_data_df)
    eq_log = bt_log.simulate('log signals')

    plot_equity_curves({'XGB Strategy': eq_xgb, 'Logistic Strategy': eq_log}, title='Strategy Equity Comparison')

    # diagnostics on test set
    y_pred_log = log_model.predict(X_test)
    y_proba_log = log_model.predict_proba(X_test)[:, 1]
    plot_confusion(y_test, y_pred_log, title='Logistic Confusion Matrix')
    plot_prediction_distribution(y_proba_log, title='Logistic Predicted Probabilities')
    plot_feature_importance(log_model, feature_cols, title='Logistic Feature Coefficients')

    if xgb_model is not None:
        y_pred_xgb = xgb_model.predict(X_test)
        y_proba_xgb = xgb_model.predict_proba(X_test)[:, 1]
        plot_confusion(y_test, y_pred_xgb, title='XGBoost Confusion Matrix')
        plot_prediction_distribution(y_proba_xgb, title='XGBoost Predicted Probabilities')
        plot_feature_importance(xgb_model, feature_cols, title='XGBoost Feature Importance')
    else:
        print('XGBoost not installed; skip XGBoost diagnostics.')