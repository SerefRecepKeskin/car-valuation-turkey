"""
Vehicle Price Estimation - Synthetic Data Generation Module
Generates realistic synthetic data for the Turkish automobile market.
"""

import json
import random
import os

from src.logger import log

# Fixed seed for reproducibility
random.seed(42)

# ============================================================
# Brand-model-package definitions and base prices for Turkish market
# Prices are approximate 2024 new vehicle TL list prices
# ============================================================

VEHICLE_CATALOG = {
    "Toyota": {
        "Corolla": {
            "packages": ["Dream", "Flame", "Passion", "Vision"],
            "base_price": 1_250_000,
            "segment": "sedan_c",
        },
        "Yaris": {
            "packages": ["Dream", "Flame", "Vision"],
            "base_price": 950_000,
            "segment": "hatchback_b",
        },
        "C-HR": {
            "packages": ["Dream", "Flame", "Passion"],
            "base_price": 1_500_000,
            "segment": "suv_c",
        },
        "RAV4": {
            "packages": ["Dream", "Flame", "Passion", "Adventure"],
            "base_price": 2_200_000,
            "segment": "suv_d",
        },
        "Yaris Cross": {
            "packages": ["Dream", "Flame", "Adventure"],
            "base_price": 1_200_000,
            "segment": "suv_b",
        },
    },
    "Honda": {
        "Civic": {
            "packages": ["Elegance", "Executive", "RS"],
            "base_price": 1_350_000,
            "segment": "sedan_c",
        },
        "City": {
            "packages": ["Elegance", "Executive"],
            "base_price": 1_050_000,
            "segment": "sedan_b",
        },
        "HR-V": {
            "packages": ["Elegance", "Executive", "Advance"],
            "base_price": 1_400_000,
            "segment": "suv_c",
        },
        "ZR-V": {
            "packages": ["Elegance", "Advance", "Sport"],
            "base_price": 1_750_000,
            "segment": "suv_c",
        },
    },
    "Volkswagen": {
        "Passat": {
            "packages": ["Business", "Elegance", "R-Line"],
            "base_price": 2_100_000,
            "segment": "sedan_d",
        },
        "Golf": {
            "packages": ["Impression", "Style", "R-Line"],
            "base_price": 1_450_000,
            "segment": "hatchback_c",
        },
        "Polo": {
            "packages": ["Life", "Style", "R-Line"],
            "base_price": 1_000_000,
            "segment": "hatchback_b",
        },
        "T-Roc": {
            "packages": ["Life", "Style", "R-Line"],
            "base_price": 1_550_000,
            "segment": "suv_c",
        },
        "Tiguan": {
            "packages": ["Life", "Elegance", "R-Line"],
            "base_price": 2_300_000,
            "segment": "suv_d",
        },
        "T-Cross": {
            "packages": ["Life", "Style", "R-Line"],
            "base_price": 1_150_000,
            "segment": "suv_b",
        },
    },
    "Hyundai": {
        "Tucson": {
            "packages": ["Style", "Elite", "Elite Plus"],
            "base_price": 1_600_000,
            "segment": "suv_c",
        },
        "i20": {
            "packages": ["Jump", "Style", "Elite"],
            "base_price": 850_000,
            "segment": "hatchback_b",
        },
        "Bayon": {
            "packages": ["Jump", "Style", "Elite"],
            "base_price": 900_000,
            "segment": "suv_b",
        },
        "Elantra": {
            "packages": ["Style", "Elite", "Elite Plus"],
            "base_price": 1_250_000,
            "segment": "sedan_c",
        },
        "Kona": {
            "packages": ["Style", "Elite"],
            "base_price": 1_300_000,
            "segment": "suv_b",
        },
    },
    "Renault": {
        "Clio": {
            "packages": ["Joy", "Touch", "Icon"],
            "base_price": 850_000,
            "segment": "hatchback_b",
        },
        "Megane": {
            "packages": ["Joy", "Touch", "Icon"],
            "base_price": 1_150_000,
            "segment": "sedan_c",
        },
        "Captur": {
            "packages": ["Joy", "Touch", "Icon"],
            "base_price": 1_200_000,
            "segment": "suv_b",
        },
        "Taliant": {
            "packages": ["Joy", "Touch", "Icon"],
            "base_price": 780_000,
            "segment": "sedan_b",
        },
        "Austral": {
            "packages": ["Techno", "Iconic", "Esprit Alpine"],
            "base_price": 1_800_000,
            "segment": "suv_c",
        },
    },
    "Fiat": {
        "Egea Sedan": {
            "packages": ["Easy", "Urban", "Urban Plus", "Lounge"],
            "base_price": 800_000,
            "segment": "sedan_c",
        },
        "Egea Hatchback": {
            "packages": ["Easy", "Urban", "Urban Plus", "Lounge"],
            "base_price": 820_000,
            "segment": "hatchback_c",
        },
        "Egea Cross": {
            "packages": ["Urban", "Urban Plus", "Lounge"],
            "base_price": 950_000,
            "segment": "suv_c",
        },
        "500": {
            "packages": ["Pop", "Lounge", "Sport"],
            "base_price": 850_000,
            "segment": "hatchback_a",
        },
    },
    "BMW": {
        "3 Serisi": {
            "packages": ["First Edition", "Sport Line", "M Sport"],
            "base_price": 2_800_000,
            "segment": "sedan_d_premium",
        },
        "5 Serisi": {
            "packages": ["Sport Line", "Luxury Line", "M Sport"],
            "base_price": 4_200_000,
            "segment": "sedan_e_premium",
        },
        "X1": {
            "packages": ["sDrive", "xLine", "M Sport"],
            "base_price": 2_500_000,
            "segment": "suv_c_premium",
        },
        "X3": {
            "packages": ["xLine", "M Sport", "M Sport X"],
            "base_price": 3_400_000,
            "segment": "suv_d_premium",
        },
    },
    "Mercedes-Benz": {
        "A Serisi": {
            "packages": ["Style", "Progressive", "AMG"],
            "base_price": 2_300_000,
            "segment": "hatchback_c_premium",
        },
        "C Serisi": {
            "packages": ["Avantgarde", "AMG", "Exclusive"],
            "base_price": 3_000_000,
            "segment": "sedan_d_premium",
        },
        "E Serisi": {
            "packages": ["Avantgarde", "AMG", "Exclusive"],
            "base_price": 4_500_000,
            "segment": "sedan_e_premium",
        },
        "GLA": {
            "packages": ["Style", "Progressive", "AMG"],
            "base_price": 2_600_000,
            "segment": "suv_c_premium",
        },
    },
    "Audi": {
        "A3": {
            "packages": ["Attraction", "Design", "S Line"],
            "base_price": 2_200_000,
            "segment": "sedan_c_premium",
        },
        "A4": {
            "packages": ["Design", "S Line", "Advanced"],
            "base_price": 2_900_000,
            "segment": "sedan_d_premium",
        },
        "Q3": {
            "packages": ["Design", "S Line", "Advanced"],
            "base_price": 2_700_000,
            "segment": "suv_c_premium",
        },
        "Q5": {
            "packages": ["Design", "S Line", "Advanced"],
            "base_price": 3_600_000,
            "segment": "suv_d_premium",
        },
    },
    "Kia": {
        "Sportage": {
            "packages": ["Cool", "Prestige", "GT-Line"],
            "base_price": 1_500_000,
            "segment": "suv_c",
        },
        "Ceed": {
            "packages": ["Cool", "Prestige", "GT-Line"],
            "base_price": 1_200_000,
            "segment": "hatchback_c",
        },
        "Stonic": {
            "packages": ["Cool", "Prestige"],
            "base_price": 1_050_000,
            "segment": "suv_b",
        },
        "Picanto": {
            "packages": ["Cool", "Prestige"],
            "base_price": 700_000,
            "segment": "hatchback_a",
        },
    },
    "Peugeot": {
        "208": {
            "packages": ["Active", "Allure", "GT"],
            "base_price": 950_000,
            "segment": "hatchback_b",
        },
        "308": {
            "packages": ["Active", "Allure", "GT"],
            "base_price": 1_350_000,
            "segment": "hatchback_c",
        },
        "2008": {
            "packages": ["Active", "Allure", "GT"],
            "base_price": 1_250_000,
            "segment": "suv_b",
        },
        "3008": {
            "packages": ["Active", "Allure", "GT"],
            "base_price": 1_700_000,
            "segment": "suv_c",
        },
    },
    "Skoda": {
        "Octavia": {
            "packages": ["Ambition", "Style", "RS"],
            "base_price": 1_400_000,
            "segment": "sedan_c",
        },
        "Superb": {
            "packages": ["Ambition", "Style", "Laurin & Klement"],
            "base_price": 2_000_000,
            "segment": "sedan_d",
        },
        "Karoq": {
            "packages": ["Ambition", "Style"],
            "base_price": 1_500_000,
            "segment": "suv_c",
        },
        "Fabia": {
            "packages": ["Ambition", "Style"],
            "base_price": 900_000,
            "segment": "hatchback_b",
        },
    },
    "Dacia": {
        "Duster": {
            "packages": ["Essential", "Comfort", "Prestige"],
            "base_price": 1_050_000,
            "segment": "suv_c",
        },
        "Sandero": {
            "packages": ["Essential", "Comfort", "Stepway"],
            "base_price": 700_000,
            "segment": "hatchback_b",
        },
        "Jogger": {
            "packages": ["Essential", "Comfort", "Extreme"],
            "base_price": 950_000,
            "segment": "mpv",
        },
    },
    "Nissan": {
        "Qashqai": {
            "packages": ["Visia", "Acenta", "Tekna"],
            "base_price": 1_500_000,
            "segment": "suv_c",
        },
        "Juke": {
            "packages": ["Visia", "Acenta", "Tekna"],
            "base_price": 1_150_000,
            "segment": "suv_b",
        },
        "X-Trail": {
            "packages": ["Acenta", "N-Connecta", "Tekna"],
            "base_price": 2_000_000,
            "segment": "suv_d",
        },
    },
    "Opel": {
        "Corsa": {
            "packages": ["Edition", "Elegance", "GS Line"],
            "base_price": 900_000,
            "segment": "hatchback_b",
        },
        "Astra": {
            "packages": ["Edition", "Elegance", "GS Line"],
            "base_price": 1_200_000,
            "segment": "hatchback_c",
        },
        "Crossland": {
            "packages": ["Edition", "Elegance", "GS Line"],
            "base_price": 1_100_000,
            "segment": "suv_b",
        },
        "Grandland": {
            "packages": ["Edition", "Elegance", "GS Line"],
            "base_price": 1_600_000,
            "segment": "suv_c",
        },
    },
    "Citroen": {
        "C3": {
            "packages": ["Feel", "Shine", "Max"],
            "base_price": 850_000,
            "segment": "hatchback_b",
        },
        "C4": {
            "packages": ["Feel", "Shine", "Max"],
            "base_price": 1_200_000,
            "segment": "hatchback_c",
        },
        "C5 Aircross": {
            "packages": ["Feel", "Shine", "Max"],
            "base_price": 1_600_000,
            "segment": "suv_c",
        },
    },
    "Volvo": {
        "XC40": {
            "packages": ["Core", "Plus", "Ultimate"],
            "base_price": 2_400_000,
            "segment": "suv_c_premium",
        },
        "XC60": {
            "packages": ["Core", "Plus", "Ultimate"],
            "base_price": 3_500_000,
            "segment": "suv_d_premium",
        },
        "S60": {
            "packages": ["Core", "Plus", "Ultimate"],
            "base_price": 2_800_000,
            "segment": "sedan_d_premium",
        },
    },
    "TOGG": {
        "T10X": {
            "packages": ["Standart", "Uzun Menzil", "Ileri"],
            "base_price": 1_350_000,
            "segment": "suv_c",
        },
    },
    "Cupra": {
        "Formentor": {
            "packages": ["V", "VZ"],
            "base_price": 1_800_000,
            "segment": "suv_c",
        },
        "Leon": {
            "packages": ["V", "VZ"],
            "base_price": 1_500_000,
            "segment": "hatchback_c",
        },
    },
    "Seat": {
        "Ibiza": {
            "packages": ["Reference", "Style", "FR"],
            "base_price": 900_000,
            "segment": "hatchback_b",
        },
        "Arona": {
            "packages": ["Reference", "Style", "FR"],
            "base_price": 1_050_000,
            "segment": "suv_b",
        },
    },
}

# Years: 2020-2025 (new / stock vehicles)
YEARS = [2020, 2021, 2022, 2023, 2024, 2025]

# Year-based price multiplier (2024 is base year = 1.0)
YEAR_MULTIPLIER = {
    2020: 0.68,
    2021: 0.74,
    2022: 0.82,
    2023: 0.91,
    2024: 1.00,
    2025: 1.08,
}


def _package_multiplier(package_index, total_packages):
    """Returns price multiplier based on package tier."""
    if total_packages == 1:
        return 1.0
    return 1.0 + (package_index / (total_packages - 1)) * 0.18


def generate_data(n=10000):
    """
    Generates realistic new vehicle data.

    Each record: {year, brand, model, package, price}
    Price = base_price * year_multiplier * package_multiplier * random_noise
    """
    records = []

    combinations = []
    for brand, models in VEHICLE_CATALOG.items():
        for model_name, info in models.items():
            for year in YEARS:
                for pkg_idx, package in enumerate(info["packages"]):
                    combinations.append({
                        "brand": brand,
                        "model": model_name,
                        "package": package,
                        "year": year,
                        "base_price": info["base_price"],
                        "pkg_idx": pkg_idx,
                        "total_packages": len(info["packages"]),
                    })

    log.info(f"Total possible combinations: {len(combinations)}")

    while len(records) < n:
        combo = random.choice(combinations)

        year_mult = YEAR_MULTIPLIER[combo["year"]]
        pkg_mult = _package_multiplier(combo["pkg_idx"], combo["total_packages"])
        noise = random.uniform(0.93, 1.07)

        price = combo["base_price"] * year_mult * pkg_mult * noise
        price = round(price / 10_000) * 10_000

        records.append({
            "year": combo["year"],
            "brand": combo["brand"],
            "model": combo["model"],
            "package": combo["package"],
            "price": int(price),
        })

    return records


def save_data(data, path="output/cars.json"):
    """Saves data to a JSON file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log.success(f"{len(data)} records saved to '{path}'")


if __name__ == "__main__":
    records = generate_data(10000)
    save_data(records)

    prices = [r["price"] for r in records]
    brands = set(r["brand"] for r in records)
    models = set(r["model"] for r in records)

    log.section("Dataset Summary")
    log.metric("Total records", f"{len(records):,}")
    log.metric("Brand count", len(brands))
    log.metric("Model count", len(models))
    log.metric("Min price", f"{min(prices):>12,} TL")
    log.metric("Max price", f"{max(prices):>12,} TL")
    log.metric("Average price", f"{sum(prices)//len(prices):>12,} TL")
