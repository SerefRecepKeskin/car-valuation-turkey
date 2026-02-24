#!/usr/bin/env python3
"""
Vehicle Price Estimation Model - Main Entry Point
==================================================
Usage:
    python main.py                                    # Full pipeline + interactive prediction
    python main.py predict 2024 Toyota Corolla Dream  # Single prediction (model must be trained)
"""

import subprocess
import sys
import os

# Project root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)


def install_dependencies():
    """Auto-installs required Python packages."""
    required = {
        "numpy": "numpy",
        "pandas": "pandas",
        "scikit-learn": "sklearn",
        "matplotlib": "matplotlib",
        "seaborn": "seaborn",
        "python-docx": "docx",
    }

    missing = []
    for pkg, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg)

    if missing:
        from src.logger import log
        log.warning(f"Installing: {', '.join(missing)}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet"] + missing
        )
        log.success("Packages installed successfully")
    else:
        from src.logger import log
        log.success("All dependencies available")


def main():
    from src.logger import log

    log.header(
        "VEHICLE PRICE ESTIMATION MODEL",
        "New & Undamaged Car Price Prediction"
    )

    # 1. Dependencies
    log.step(1, 4, "Checking dependencies...")
    install_dependencies()

    # 2. Generate data
    log.step(2, 4, "Generating synthetic dataset (10,000 records)...")
    from src.data_generator import generate_data, save_data
    data = generate_data(10000)
    save_data(data, os.path.join(BASE_DIR, "output", "cars.json"))

    # 3. Clean + Train
    log.step(3, 4, "Cleaning data & training models...")
    from src.preprocessing import load_data, clean_data, encode_features
    from src.model import train_models, save_model, show_sample_predictions

    df = load_data(os.path.join(BASE_DIR, "output", "cars.json"))
    df = clean_data(df)
    _, encoders = encode_features(df)
    best_model, _, encoders, _, _ = train_models(df, encoders)

    save_model(best_model, encoders)
    show_sample_predictions()

    # 4. Interactive prediction
    log.step(4, 4, "Interactive prediction mode...")
    interactive_prediction()


def cli_predict(args):
    """Handle: python main.py predict 2024 Toyota Corolla Dream"""
    from src.logger import log
    from src.model import predict_price

    if len(args) != 4:
        log.error("Usage: python main.py predict <year> <brand> <model> <package>")
        log.info("Example: python main.py predict 2024 Toyota Corolla Dream")
        sys.exit(1)

    try:
        price = predict_price(int(args[0]), args[1], args[2], args[3])
        log.header("PRICE PREDICTION")
        log.metric("Year", args[0])
        log.metric("Brand", args[1])
        log.metric("Model", args[2])
        log.metric("Package", args[3])
        log.result(f"Estimated Price: {price:,} TL")
    except ValueError as e:
        log.error(str(e))
        sys.exit(1)


def interactive_prediction():
    """Kullanicidan tek tek bilgi alarak fiyat tahmini yapar."""
    from src.model import predict_price, load_model
    from src.logger import log

    log.section("INTERAKTIF FIYAT TAHMINI")
    log.info("Cikmak icin 'exit' yazin.")

    _, encoders = load_model()
    brands = sorted(encoders["brand"].classes_)
    log.info(f"Mevcut markalar: {', '.join(brands)}")

    while True:
        print()
        year_input = input("  Yil (orn. 2024): ").strip()
        if year_input.lower() == "exit":
            break

        brand = input("  Marka (orn. Toyota): ").strip()
        if brand.lower() == "exit":
            break

        model_name = input("  Model (orn. Corolla): ").strip()
        if model_name.lower() == "exit":
            break

        package = input("  Paket (orn. Dream): ").strip()
        if package.lower() == "exit":
            break

        try:
            price = predict_price(int(year_input), brand, model_name, package)
            log.result(f"Tahmini Fiyat: {price:,} TL")
        except ValueError as e:
            log.error(str(e))
        except Exception as e:
            log.error(f"Beklenmeyen hata: {e}")

    log.info("Program sonlandirildi.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "predict":
        cli_predict(sys.argv[2:])
    else:
        main()
