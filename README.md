# Sifir Oto Degerleme Modeli

Hasarsiz ve sifir araclar icin makine ogrenmesi tabanli fiyat tahmin sistemi.

> EminEvim - Teknik Degerlendirme Projesi

---

## Kurulum ve Calistirma

```bash
# 1. Sanal ortam olustur
python -m venv .venv

# 2. Sanal ortami aktif et
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Bagimlilikari yukle
pip install -r requirements.txt

# 4. Projeyi calistir
python main.py
```

`python main.py` calistiginda sirasiyla:
1. Eksik paketleri kontrol eder (varsa otomatik yukler)
2. 10.000 kayitlik sentetik veri seti uretir
3. Veriyi temizler ve on isler
4. 3 farkli ML modeli egitir, karsilastirir, en iyisini kaydeder
5. Ornek tahminler gosterir
6. Interaktif tahmin moduna gecer (kullanicidan yil/marka/model/paket alir)

---

## Tek Arac Fiyat Tahmini (Terminalden)

Model egitildikten sonra dogrudan terminalden tahmin yapabilirsiniz:

```bash
python main.py predict 2024 Toyota Corolla Dream
# -> Tahmini Fiyat: 1,200,000 TL
```

## Python'dan Kullanim

```python
from src.model import predict_price

fiyat = predict_price(2024, "Toyota", "Corolla", "Dream")
print(f"{fiyat:,} TL")  # 1,200,000 TL

# Odev gereksinimi icin Turkce fonksiyon:
from src.model import fiyat_tahmin_et
fiyat = fiyat_tahmin_et(2024, "Toyota", "Corolla", "Dream")
```

---

## Proje Yapisi

```
emingroup/
├── main.py                     Ana giris noktasi. Pipeline'i calistirir,
│                                interaktif tahmin modu ve CLI predict destegi.
│
├── requirements.txt            Python bagimlilik listesi.
├── README.md                   Bu dosya.
├── v.pdf                       Orijinal odev dokumani (EminEvim).
│
├── src/                        Kaynak kod modulleri
│   ├── __init__.py             Paket tanimlayici.
│   ├── logger.py               Renkli ve formatli terminal cikti sinifi.
│   ├── data_generator.py       Sentetik veri uretimi. 20 marka, 80+ model,
│   │                            yil/paket bazli gercekci fiyat hesaplama.
│   ├── preprocessing.py        Veri temizleme: eksik deger, aykiri deger (IQR),
│   │                            duplike kontrolu, LabelEncoder kodlama.
│   └── model.py                Linear Regression, Random Forest, Gradient Boosting
│                                egitimi. predict_price() ve fiyat_tahmin_et().
│
├── notebooks/
│   └── analysis.ipynb          Detayli analiz notebook'u: EDA, Eta-kare analizi,
│                                model egitimi, performans gorselleri.
│
├── output/                     Calisma zamaninda uretilen dosyalar:
│   ├── cars.json                 Uretilen veri seti (10.000 kayit)
│   ├── model.pkl                 Egitilmis en iyi model (Gradient Boosting)
│   ├── encoders.pkl              Kategorik degisken kodlayicilari
│   └── analysis/                 Notebook'tan kaydedilen analiz gorselleri
│
└── docs/
    └── rapor.docx              Detayli Turkce teknik rapor (EminEvim icin).
```

---

## Model Sonuclari

| Model              | RMSE (TL) | MAE (TL) | R²     |
|--------------------|-----------|----------|--------|
| Linear Regression  | ~616K     | ~494K    | ~0.06  |
| Random Forest      | ~78K      | ~62K     | ~0.98  |
| Gradient Boosting  | ~74K      | ~58K     | ~0.99  |

En iyi model: **Gradient Boosting** (en dusuk RMSE, en yuksek R²)

---

## Gereksinimler

- Python 3.10+
- numpy, pandas, scikit-learn, matplotlib, seaborn, python-docx

Tumu `requirements.txt` icinde tanimlidir, `pip install -r requirements.txt` ile kurulur.
