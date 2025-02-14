import yfinance as yf
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

# Função para baixar e tratar os dados
def get_brent_data(ticker='BZ=F', start="2014-01-01", end="2024-01-01"):
    brent = yf.download(ticker, start=start, end=end, interval="1d")
    df = brent[['Close']].reset_index()
    df.columns = ['data', 'valor']
    df.set_index('data', inplace=True)
    df['valor'] = df['valor'].interpolate()  # Preenchendo valores ausentes
    return df

# Função para criar features de séries temporais
def create_features(df, lags=[1, 5, 10, 20], windows=[5, 10, 20]):
    for lag in lags:
        df[f'lag_{lag}'] = df['valor'].shift(lag)

    for window in windows:
        df[f'media_movel_{window}'] = df['valor'].rolling(window=window).mean()

    return df.dropna()

# Função para treinar o modelo XGBoost
def train_xgboost(X_train, y_train):
    model = xgb.XGBRegressor(objective='reg:squarederror',
                             n_estimators=300,
                             learning_rate=0.03,
                             max_depth=7,
                             subsample=0.8,
                             colsample_bytree=0.8,
                             random_state=42)
    model.fit(X_train, y_train)
    return model

# Função para calcular métricas de avaliação
def evaluate_model(y_true, y_pred):
    metrics = {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R²": r2_score(y_true, y_pred),
        "MAPE": np.mean(np.abs((y_true - y_pred) / y_true)) * 100,
        "MBD": np.mean((y_pred - y_true) / y_true) * 100,
        "sMAPE": np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100
    }
    return metrics

# Função para prever os próximos 30 dias
def forecast_future(model, df, lags, windows, days=30):
    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=days, freq='D')
    future_predictions = []

    # Cálculo da tendência linear
    X_trend = np.arange(30).reshape(-1, 1)
    y_trend = df['valor'].iloc[-30:].values.reshape(-1, 1)

    trend_model = LinearRegression()
    trend_model.fit(X_trend, y_trend)
    trend_factor = trend_model.coef_[0][0]

    latest_values = df.iloc[-1].copy()

    for date in future_dates:
        new_input = latest_values.drop("valor").values.reshape(1, -1)
        predicted_value = model.predict(new_input)[0]

        # Aplicação da tendência linear
        predicted_value += trend_factor
        future_predictions.append(predicted_value)

        latest_values['valor'] = predicted_value
        for lag in reversed(lags):
            if f'lag_{lag}' in latest_values:
                latest_values[f'lag_{lag}'] = predicted_value if lag == 1 else latest_values.get(f'lag_{lag-1}', predicted_value)
        for window in windows:
            if f'media_movel_{window}' in latest_values:
                latest_values[f'media_movel_{window}'] = np.mean(future_predictions[-window:]) if len(future_predictions) >= window else np.mean(future_predictions)

    return pd.DataFrame({'Previsao': future_predictions}, index=future_dates)