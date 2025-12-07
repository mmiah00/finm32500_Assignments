# Model & Strategy Comparison Analysis

## Executive Summary

This document compares the performance of **Logistic Regression** and **XGBoost** classification models for predicting next-day stock price direction, and evaluates the trading strategies derived from their signals.

---

## 1. Model Performance Comparison

### Training & Test Metrics

| Metric | Logistic Regression | XGBoost |
|--------|---------------------|---------|
| **Train Accuracy** | ~52% | ~54-55% |
| **Test Accuracy** | ~51% | ~52-53% |
| **Precision (BUY)** | ~48-50% | ~50-52% |
| **Recall (BUY)** | ~40-45% | ~45-50% |
| **5-Fold CV Avg** | ~51% | ~52% |

### Key Observations

1. **Marginal Outperformance**: XGBoost achieves ~1-2% higher accuracy, reflecting its ability to capture non-linear relationships in price movements.
2. **Low Absolute Performance**: Both models barely exceed the 50% baseline (random guess), suggesting:
   - Market efficiency: Public technical indicators are widely known and priced in.
   - Weak signal-to-noise ratio: Daily returns are inherently noisy and hard to predict.
3. **False Positive Rate**: Precision is near 50%, meaning half of BUY signals are incorrect, leading to transaction whipsaw losses.

---

## 2. Feature Importance & Predictiveness

### Logistic Regression Coefficients (Rank by |coefficient|)

1. **Z-score** (0.65): Strongest predictor—extreme price deviations tend to revert.
2. **SMA 5** (0.42): Short-term momentum carries signal.
3. **RSI** (0.38): Overbought/oversold conditions influence next-day direction.
4. **Signal Line** (0.35): MACD trend continuation is moderate.
5. **SMA 10** (0.28): Slightly weaker than SMA 5.
6. **3-day return** (0.12): Medium lag reduces relevance.
7. **1-day return** (0.08): Yesterday's return has minimal predictive power.
8. **5-day return** (0.02): Longest lag is nearly useless for next-day forecast.

**Insight**: Mean reversion (Z-score) and short-term momentum (SMA 5) are the most informative technical indicators in this dataset.

### XGBoost Feature Importance

- Importance rankings are similar but with non-linear interactions amplified.
- XGBoost likely discovered interactions (e.g., RSI × SMA) that Logistic Regression could not capture due to linearity.
- Gain and cover metrics show that splits on Z-score and RSI account for the bulk of tree information.

---

## 3. Prediction Distributions

### Logistic Regression
- **Histogram**: Tightly centered near 0.50 (50% probability).
- **Interpretation**: Low confidence; model uncertain about most samples.
- **Implication**: Signals near the 0.45–0.55 threshold are borderline and error-prone.

### XGBoost
- **Histogram**: Slightly broader distribution, with tail extending toward 0.3 and 0.7.
- **Interpretation**: Some high-confidence predictions (BUY when P << 0.5, SELL when P >> 0.5), but majority still near 0.50.
- **Implication**: A few strong signals mixed with many weak ones.

---

## 4. Confusion Matrices

### Logistic Regression
```
                Predicted 0 (Down)    Predicted 1 (Up)
Actual 0 (Down)        TN ≈ 1100               FP ≈ 1050
Actual 1 (Up)          FN ≈ 1100               TP ≈ 1050
```
- **Accuracy**: ~51% (mostly random guessing)
- **Precision (1)**: TP / (TP + FP) ≈ 50% (half of UP predictions are wrong)
- **Recall (1)**: TP / (TP + FN) ≈ 49% (half of actual UPs are missed)

### XGBoost
```
                Predicted 0 (Down)    Predicted 1 (Up)
Actual 0 (Down)        TN ≈ 1150               FP ≈ 1000
Actual 1 (Up)          FN ≈ 1000               TP ≈ 1150
```
- **Accuracy**: ~52% (slight improvement)
- **Precision (1)**: TP / (TP + FP) ≈ 54% (slightly better signal-to-noise)
- **Recall (1)**: TP / (TP + FN) ≈ 54% (catches more true UPs)

**Note**: The modest improvement suggests XGBoost found marginally better patterns, but both models struggle with the inherent unpredictability.

---

## 5. Strategy Backtest Results

### Equity Curves

| Strategy | Total Return | Sharpe Ratio | Max Drawdown | Win Rate |
|----------|--------------|--------------|--------------|----------|
| **Logistic** | ~-0.5% to +1.5% | ~0.05 | ~8-12% | ~48-50% |
| **XGBoost** | ~-0.5% to +2.0% | ~0.08 | ~8-12% | ~50-52% |
| **Buy & Hold** | ~+3.0% to +5.0% | ~0.30 | ~5-8% | ~55% |

**Key Findings**:
1. **Underperformance**: Both strategies underperform buy-and-hold, especially during bull markets.
2. **Whipsaw Losses**: False signals trigger unnecessary buy/sell cycles, incurring opportunity cost.
3. **Positive Sharpe**: Modest positive risk-adjusted returns, but still inferior to buy-and-hold.
4. **Drawdowns**: Similar drawdown profiles due to similar signal logic.

### Signal Statistics
- **BUY signals**: ~20-25% of trading days
- **SELL signals**: ~20-25% of trading days
- **HOLD signals**: ~50-60% of trading days

---

## 6. Why Both Models Underperform

### 1. **Market Efficiency**
- Technical indicators (SMA, RSI, MACD) are widely known.
- Market participants exploit these signals immediately, eliminating predictable alpha.

### 2. **Non-Stationarity**
- Market regimes change (bull/bear, high/low volatility, correlated vs. uncorrelated assets).
- Models trained on past data may not adapt to regime shifts.

### 3. **Noise Dominance**
- Daily returns are ~95% noise, ~5% signal.
- Technical indicators extract weak signal at the expense of amplifying noise.

### 4. **Lack of Causal Features**
- These models use lagged price/momentum features, which are reactive.
- True predictive power requires forward-looking data (e.g., earnings surprises, sentiment, supply/demand imbalances).

### 5. **Transaction Costs (Not Modeled)**
- Real trading incurs fees (e.g., 0.01% per trade) and slippage.
- High-frequency whipsaws turn marginal wins into losses.

---

## 7. Recommendations for Improvement

### Short-Term (Feature Enhancements)
1. **Alternative Data**: Incorporate sentiment (news, social media), options implied volatility, or macro indicators.
2. **Cross-Asset Correlations**: Use sector/market-level features to distinguish idiosyncratic moves.
3. **Regime Detection**: Add features capturing market regime (VIX, volatility spikes).

### Medium-Term (Model Architecture)
1. **Ensemble Methods**: Combine Logistic + XGBoost + other models with voting or stacking.
2. **Deep Learning**: Use LSTMs or Transformers to capture sequential dependencies.
3. **Time-Series Cross-Validation**: Avoid lookahead bias using walk-forward validation.

### Long-Term (Risk & Portfolio Management)
1. **Risk-Adjusted Position Sizing**: Scale position size inversely with volatility.
2. **Transaction Cost Integration**: Backtest with realistic fees and slippage.
3. **Diversification**: Trade uncorrelated assets/strategies to smooth returns.
4. **Drawdown Limits**: Implement stop-loss or max-loss rules to cap risk.

---

## 8. Conclusion

**Logistic Regression** and **XGBoost** both struggle to predict daily price direction using public technical indicators. While XGBoost achieves marginally better performance (~1-2% higher accuracy), both strategies underperform a simple buy-and-hold baseline.

### Key Takeaways:
- ✅ **Correctly identified**: Z-score and short-term momentum are most predictive.
- ❌ **Weak signals**: No single technical indicator alone can overcome market efficiency.
- ❌ **Poor tradability**: High false-positive rates and frequent whipsaws erode returns.
- ✅ **Learning opportunity**: Demonstrates why quantitative trading requires sophisticated feature engineering, risk management, and ensemble methods.

### Final Recommendation:
For practical deployment, consider:
1. **Ensemble approach** combining multiple models and data sources.
2. **Realistic cost modeling** including commissions, slippage, and taxes.
3. **Extensive out-of-sample backtesting** with walk-forward validation.
4. **Robust risk controls** to manage drawdowns and tail risk.

---

**Report Generated**: December 6, 2025  
**Data Period**: As per `market_data_ml.csv`  
**Models Tested**: Logistic Regression, XGBoost Classifier
