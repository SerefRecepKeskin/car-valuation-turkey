"""
Vehicle Price Estimation - Data Preprocessing Module
Handles data loading, cleaning, encoding, and feature engineering.
"""

import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from src.logger import log


def load_data(path):
    """Loads a JSON dataset and returns a DataFrame."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return df


def clean_data(df):
    """
    Data cleaning steps:
    1. Missing value detection and removal
    2. Data type validation
    3. Outlier detection (IQR method for prices)
    4. Duplicate record removal
    """
    log.section("DATA CLEANING REPORT")
    initial_count = len(df)

    # 1. Missing values
    total_missing = df.isnull().sum().sum()
    if total_missing > 0:
        df = df.dropna()
        log.warning(f"Missing values: {total_missing} -> rows removed, remaining: {len(df)}")
    else:
        log.info(f"Missing values: {total_missing}")

    # 2. Data type validation
    log.info("Data types validated:")
    log.metric("year", f"{df['year'].dtype} (int)")
    log.metric("brand", f"{df['brand'].dtype} (str)")
    log.metric("model", f"{df['model'].dtype} (str)")
    log.metric("package", f"{df['package'].dtype} (str)")
    log.metric("price", f"{df['price'].dtype} (int)")

    df["year"] = df["year"].astype(int)
    df["price"] = df["price"].astype(int)

    # 3. Outlier detection (IQR for price)
    Q1 = df["price"].quantile(0.25)
    Q3 = df["price"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outlier_count = ((df["price"] < lower_bound) | (df["price"] > upper_bound)).sum()

    log.info(f"Outlier detection (IQR): Q1={Q1:,.0f}, Q3={Q3:,.0f}, IQR={IQR:,.0f}")
    log.metric("Bounds", f"{lower_bound:,.0f} - {upper_bound:,.0f} TL")
    if outlier_count > 0:
        df = df[(df["price"] >= lower_bound) & (df["price"] <= upper_bound)]
        log.warning(f"Outliers removed: {outlier_count} records, remaining: {len(df)}")
    else:
        log.info(f"Outliers: {outlier_count}")

    # 4. Duplicate records
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        log.warning(f"Duplicates removed: {duplicates} records, remaining: {len(df)}")
    else:
        log.info(f"Duplicates: {duplicates}")

    removed = initial_count - len(df)
    log.success(f"Cleaned: {initial_count:,} -> {len(df):,} records ({removed} removed)")

    return df.reset_index(drop=True)


def encode_features(df):
    """
    Encodes categorical variables (brand, model, package) using LabelEncoder.
    Returns the encoded DataFrame and a dict of encoders.

    Note: LabelEncoder assigns arbitrary integers to categories. This creates
    a false ordinal relationship (e.g. Audi=0, BMW=1 does NOT mean BMW > Audi).
    Tree-based models (Random Forest, Gradient Boosting) handle this correctly
    because they split on individual values. However, Linear Regression treats
    these as ordinal numbers, which partially explains its poor performance.
    """
    encoders = {}
    df_encoded = df.copy()

    for col in ["brand", "model", "package"]:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df[col])
        encoders[col] = le

    return df_encoded, encoders
