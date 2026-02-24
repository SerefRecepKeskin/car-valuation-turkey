"""
Vehicle Price Estimation - ML Model Module
Random Forest, Linear Regression, and Gradient Boosting for price prediction.
"""

import os
import pickle
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from src.logger import log

warnings.filterwarnings("ignore")

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "output", "cars.json")
MODEL_PATH = os.path.join(BASE_DIR, "output", "model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "output", "encoders.pkl")


def train_models(df, encoders=None):
    """
    Trains and compares models:
    1. Linear Regression
    2. Random Forest
    3. Gradient Boosting

    Returns the best model, its name, encoders, results dict, and test data.
    """
    from src.preprocessing import encode_features

    if encoders is None:
        df_encoded, encoders = encode_features(df)
    else:
        df_encoded = df.copy()
        for col in ["brand", "model", "package"]:
            df_encoded[col] = encoders[col].transform(df[col])

    X = df_encoded[["year", "brand", "model", "package"]]
    y = df_encoded["price"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    log.section("MODEL TRAINING RESULTS")
    log.info(f"Training set: {len(X_train):,} | Test set: {len(X_test):,}")

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=200, max_depth=15, random_state=42, n_jobs=-1
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42
        ),
    }

    results = {}
    best_rmse = float("inf")
    best_model = None
    best_model_name = None

    table_rows = []

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        results[name] = {
            "model": model,
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
            "y_test": y_test,
            "y_pred": y_pred,
        }

        table_rows.append([name, f"{rmse:,.0f}", f"{mae:,.0f}", f"{r2:.4f}"])

        if rmse < best_rmse:
            best_rmse = rmse
            best_model = model
            best_model_name = name

    log.table(["Model", "RMSE (TL)", "MAE (TL)", "R²"], table_rows)
    log.result(f"Best model: {best_model_name} (RMSE: {best_rmse:,.0f} TL)")

    return best_model, best_model_name, encoders, results, (X_test, y_test)


def save_model(model, encoders, path=None):
    """Saves trained model and encoders to disk."""
    model_path = path or MODEL_PATH
    encoder_path = os.path.join(os.path.dirname(model_path), "encoders.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    with open(encoder_path, "wb") as f:
        pickle.dump(encoders, f)
    log.success(f"Model saved to '{model_path}'")
    log.success(f"Encoders saved to '{encoder_path}'")


def load_model(path=None):
    """Loads saved model and encoders from disk."""
    model_path = path or MODEL_PATH
    encoder_path = os.path.join(os.path.dirname(model_path), "encoders.pkl")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(encoder_path, "rb") as f:
        encoders = pickle.load(f)
    return model, encoders


def predict_price(year, brand, model_name, package):
    """
    Predicts the price of a new vehicle.

    Parameters:
        year (int): Model year (e.g. 2024)
        brand (str): Vehicle brand (e.g. "Toyota")
        model_name (str): Vehicle model (e.g. "Corolla")
        package (str): Trim package (e.g. "Dream")

    Returns:
        int: Estimated price (TL)
    """
    model, encoders = load_model()

    try:
        brand_encoded = encoders["brand"].transform([brand])[0]
    except ValueError:
        raise ValueError(
            f"Unknown brand: '{brand}'. "
            f"Valid brands: {list(encoders['brand'].classes_)}"
        )

    try:
        model_encoded = encoders["model"].transform([model_name])[0]
    except ValueError:
        raise ValueError(
            f"Unknown model: '{model_name}'. "
            f"Valid models: {list(encoders['model'].classes_)}"
        )

    try:
        package_encoded = encoders["package"].transform([package])[0]
    except ValueError:
        raise ValueError(
            f"Unknown package: '{package}'. "
            f"Valid packages: {list(encoders['package'].classes_)}"
        )

    X_input = pd.DataFrame(
        [[year, brand_encoded, model_encoded, package_encoded]],
        columns=["year", "brand", "model", "package"],
    )

    predicted_price = model.predict(X_input)[0]
    return int(round(predicted_price / 10_000) * 10_000)


# Assignment-required Turkish function name (wraps predict_price)
def fiyat_tahmin_et(yil, marka, model, paket):
    """
    Sifir arac fiyat tahmini yapar.
    Odev gereksinimi icin Turkce fonksiyon adi.

    Parametreler:
        yil (int): Arac model yili (orn. 2024)
        marka (str): Arac markasi (orn. "Toyota")
        model (str): Arac modeli (orn. "Corolla")
        paket (str): Donanim paketi (orn. "Dream")

    Dondurur:
        int: Tahmini fiyat (TL)
    """
    return predict_price(yil, marka, model, paket)


def show_sample_predictions():
    """Shows sample predictions for various vehicles."""
    log.section("SAMPLE PREDICTIONS")

    samples = [
        (2024, "Toyota", "Corolla", "Dream"),
        (2023, "Honda", "Civic", "Elegance"),
        (2024, "Volkswagen", "Passat", "Business"),
        (2025, "BMW", "3 Serisi", "M Sport"),
        (2024, "Hyundai", "Tucson", "Elite"),
        (2023, "Fiat", "Egea Sedan", "Urban"),
        (2024, "Mercedes-Benz", "C Serisi", "AMG"),
        (2025, "Renault", "Clio", "Icon"),
        (2024, "Dacia", "Duster", "Comfort"),
        (2022, "Skoda", "Octavia", "Style"),
    ]

    rows = []
    for year, brand, model_name, package in samples:
        try:
            price = predict_price(year, brand, model_name, package)
            rows.append([str(year), brand, model_name, package, f"{price:>12,} TL"])
        except ValueError as e:
            rows.append([str(year), brand, model_name, package, f"ERROR: {e}"])

    log.table(["Year", "Brand", "Model", "Package", "Predicted Price"], rows)
