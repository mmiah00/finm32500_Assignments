# ML-Based Trading Strategy Project

## Overview
This project implements a machine learning pipeline for predicting stock price direction and executing a trading strategy based on model predictions. It includes feature engineering, model training, signal generation, and backtesting.

## Project Structure

### Core Modules

1. **`feature_engineering.py`**
   - Loads multi-ticker OHLCV data (`market_data_ml.csv`)
   - Computes technical indicators:
     - Daily returns: 1-day, 3-day, 5-day pct changes
     - Moving averages: SMA 5, SMA 10
     - Momentum: RSI (14-period)
     - Trend: MACD Signal Line
     - Normalization: Z-score
   - Creates classification labels: 1 if next-day return > 0, else 0

2. **`train_model.py`**
   - Trains two classification models:
     - **Logistic Regression**: Fast, interpretable linear classifier
     - **XGBoost**: Gradient boosting ensemble (superior non-linear modeling)
   - Uses hyperparameters from `model_params.json`
   - Evaluates: accuracy, precision, recall
   - Performs 5-fold cross-validation

3. **`signal_generator.py`**
   - Converts model probabilities into trading signals:
     - **BUY**: Predicted probability < low_threshold (bearish underestimation)
     - **SELL**: Predicted probability > high_threshold (bullish overestimation)
     - **HOLD**: Between thresholds (uncertain signal)
   - Returns dict with probabilities and signals

4. **`backtest.py`**
   - **`Backtest` class**: Simulates trading strategy
     - Tracks multi-ticker positions, cash, and portfolio equity
     - Executes BUY/SELL/HOLD signals with fixed position size
     - No transaction costs or slippage
     - Computes equity curve (mark-to-market)
   - **Visualization functions**:
     - `plot_equity_curves()`: Compare strategy vs baseline
     - `plot_confusion()`: Confusion matrix of predictions
     - `plot_prediction_distribution()`: Histogram of predicted probabilities
     - `plot_feature_importance()`: Feature coefficients (Logistic) or importance (XGBoost)
   - **Main**: Trains models, generates signals, runs both backtests, produces all diagnostics

### Configuration Files

- **`features_config.json`**: Lists selected features (for future extensibility)
- **`model_params.json`**: Hyperparameters for Logistic Regression and XGBoost
- **`market_data_ml.csv`**: Historical OHLCV data (multiple tickers)
- **`tickers-1.csv`**: Ticker universe (if needed for reference)

### Analysis & Documentation

- **`comparison.md`**: Detailed analysis of model performance, feature importance, and strategy results
- **`README.md`**: This file

## Setup

### Requirements
```bash
pip install pandas numpy scikit-learn xgboost matplotlib
```

### Running the Project

1. **Feature Engineering**:
   ```bash
   python feature_engineering.py
   ```
   Generates features from raw data.

2. **Model Training**:
   ```bash
   python train_model.py
   ```
   Trains Logistic and XGBoost models (models not saved; retrain in backtest.py).

3. **Complete Pipeline** (Recommended):
   ```bash
   python backtest.py
   ```
   Executes feature engineering → model training → signal generation → backtesting → visualization.

## Key Results & Insights

### Model Performance

| Model | Accuracy | Best Use Case |
|-------|----------|---------------|
| **Logistic Regression** | ~51-52% | Interpretable, feature-driven insights |
| **XGBoost** | ~52-53% | Non-linear patterns, ensemble advantage |

- Both models perform **marginally better than random** (~50%), indicating market efficiency challenges.
- Daily next-day returns show weak predictability using simple technical indicators.

### Feature Importance

**Most Predictive Features** (by coefficient magnitude):
1. **Z-score**: Price deviation from mean (strongest signal)
2. **SMA 5 / SMA 10**: Short-term momentum
3. **RSI**: Overbought/oversold conditions
4. **Signal Line (MACD)**: Trend direction

**Weakest Features**:
- **5-day returns**: Longer lag reduces relevance for next-day prediction

### Strategy Performance

- **Equity Curves**: Both strategies show modest PnL, often slightly underperforming buy-and-hold due to whipsaw losses.
- **Confusion Matrices**: Reveal low precision in BUY signals; many false positives.
- **Prediction Distributions**: Peaked near 0.5 (50-50 confidence), indicating model uncertainty.

## Limitations of ML in Financial Forecasting

1. **Market Efficiency**: Public price/volume data is already priced in by many market participants.
2. **Non-Stationarity**: Market regimes shift; models trained on historical data may not generalize.
3. **Data Leakage**: Using close price to predict next-day return introduces look-ahead bias if not careful.
4. **Transaction Costs**: Real trading incurs fees and slippage not modeled here.
5. **Overfitting**: Complex models may fit noise rather than signal.
6. **Survivorship Bias**: Using only existing tickers excludes delisted securities.

### Recommendations for Improvement

- **Feature Engineering**: Incorporate alternative data (sentiment, economic indicators, options flow).
- **Model Architecture**: Ensemble multiple models or use deep learning (LSTM) for sequential patterns.
- **Cross-Validation**: Use time-series split (walk-forward) instead of random split to avoid lookahead bias.
- **Risk Management**: Add stop-loss, position sizing based on volatility, and drawdown limits.
- **Backtesting Realism**: Include realistic transaction costs, slippage, and market impact.
- **Ensemble & Diversification**: Trade multiple strategies across uncorrelated assets.

## Unit Testing

Basic validation can be run via:
```bash
python test_feature_engineering.py
python test_models.py
python test_backtest.py
```

(See `test_*.py` files for details.)

## Deliverables Checklist

- ✅ `feature_engineering.py` — Feature creation & labeling
- ✅ `train_model.py` — Model training & evaluation
- ✅ `signal_generator.py` — Signal generation from predictions
- ✅ `backtest.py` — Backtesting & visualizations
- ✅ `comparison.md` — Model & strategy analysis
- ✅ `market_data_ml.csv` — Historical data
- ✅ `features_config.json` — Feature config
- ✅ `model_params.json` — Model hyperparameters
- ✅ `README.md` — Setup & documentation

## Contact & References

**Authors**: Team

**Advisors**: 
- Jenn: jcolli5158
- Hunter: hyoung3

**References**:
- Scikit-learn docs: https://scikit-learn.org/stable/
- XGBoost docs: https://xgboost.readthedocs.io/
- Pandas docs: https://pandas.pydata.org/docs/
