# 🚲 Bike Sharing Data Analytics Dashboard

Ini adalah proyek akhir berupa **dashboard interaktif** untuk menganalisis data penyewaan sepeda (_Bike Sharing Dataset_).

---

## 🚀 Cara Menjalankan Dashboard

### Prasyarat
Pastikan Anda telah menginstal **Python** di komputer Anda sebelum memulai.

### Langkah-langkah

**1. Buka Terminal**

Buka terminal atau command prompt, lalu navigasikan ke dalam folder proyek ini:

```bash
cd path/to/folder-proyek
```

**2. Instal Dependensi**

Instal semua library yang dibutuhkan dengan menjalankan perintah berikut:

```bash
pip install -r requirements.txt
```

**3. Jalankan Dashboard**

Setelah instalasi selesai, jalankan dashboard menggunakan Streamlit:

```bash
streamlit run dashboard.py
```

**4. Buka di Browser**

Dashboard akan secara otomatis terbuka di browser default Anda, biasanya pada alamat:

```
http://localhost:8501
```

---

## 📁 Struktur Proyek

```
├── dashboard.py               # File utama aplikasi dashboard Streamlit
├── cleaned_bike_day.csv       # Dataset harian yang sudah dibersihkan
├── cleaned_bike_hour.csv      # Dataset per jam yang sudah dibersihkan
├── requirements.txt           # Daftar library Python yang dibutuhkan
└── README.md                  # Dokumentasi cara menjalankan proyek
```

---

> 💡 **Tips:** Jika browser tidak terbuka secara otomatis, salin alamat URL di atas dan tempelkan langsung ke browser Anda.
