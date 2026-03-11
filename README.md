# 🚲 Bike Sharing Data Analytics Dashboard

Ini adalah proyek akhir berupa **dashboard interaktif** untuk menganalisis data penyewaan sepeda (_Bike Sharing Dataset_).

---

## 🛠️ Setup Environment

### Menggunakan Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Menggunakan Shell/Terminal

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## 🚀 Cara Menjalankan Dashboard

Setelah setup environment selesai, jalankan dashboard menggunakan Streamlit:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan secara otomatis terbuka di browser default Anda, biasanya pada alamat:

```
http://localhost:8501
```

---
## 📁 Struktur Proyek

```
├── dashboard/
│   ├── dashboard.py              # File utama dashboard
│   ├── cleaned_bike_day.csv      # Dataset penggunaan sepeda per hari
│   └── cleaned_bike_hour.csv     # Dataset penggunaan sepeda per jam
├── requirements.txt              # Daftar library yang dibutuhkan
└── README.md                     # Dokumentasi proyek
```

---

> 💡 **Tips:** Jika browser tidak terbuka secara otomatis, salin alamat URL di atas dan tempelkan langsung ke browser Anda.
