# MushroomAI - Klasifikasi Jamur Edible & Poisonous

Aplikasi web berbasis kecerdasan buatan menggunakan algoritma **Random Forest** 
untuk mengklasifikasikan jamur sebagai dapat dimakan (Edible) atau beracun (Poisonous) 
berdasarkan gambar yang diunggah.

---

## Deskripsi

MushroomAI adalah aplikasi web yang dikembangkan sebagai tugas praktikum mata kuliah 
Kecerdasan Buatan. Aplikasi ini memanfaatkan algoritma Random Forest dari library 
Scikit-Learn untuk melakukan klasifikasi gambar jamur secara otomatis.

---

## Fitur

- Upload gambar jamur dengan drag and drop atau pilih file
- Klasifikasi otomatis menggunakan model Random Forest
- Menampilkan hasil prediksi beserta tingkat kepercayaan model
- Menampilkan probabilitas tiap kelas (Edible & Poisonous)
- Halaman evaluasi model (Confusion Matrix, Classification Report, Feature Importance)
- Halaman informasi aplikasi, dataset, dan teknologi yang digunakan
- Desain responsif menggunakan Bootstrap 5

---

## Dataset

| Keterangan | Detail |
|---|---|
| Sumber | Kaggle |
| Nama | Edible and Poisonous Mushroom Images |
| Total Gambar | 83 gambar |
| Edible | 38 gambar |
| Poisonous | 45 gambar |
| Format | JPG / JPEG |

---

## Detail Model

| Parameter | Nilai |
|---|---|
| Algoritma | Random Forest Classifier |
| Jumlah Pohon | 100 estimators |
| Max Depth | 10 |
| Ukuran Input Gambar | 64 x 64 piksel |
| Total Fitur | 12.288 fitur piksel RGB |
| Akurasi | 76.47% |
| Split Data | 80% training / 20% testing |
| Normalisasi | StandardScaler |

---

## Teknologi

- Python 3.11
- Flask 3.0.0
- Scikit-Learn
- NumPy
- Pillow
- Bootstrap 5
- JavaScript
- Gunicorn
- Docker

---

## Struktur Proyek
mushroom-app/
│
├── app.py                  ← Flask backend (routing & prediksi)
├── train_model.py          ← Script training model Random Forest
├── requirements.txt        ← Daftar dependensi Python
├── Dockerfile              ← Konfigurasi deploy Railway
├── railway.json            ← Konfigurasi Railway
├── .gitignore              ← File yang diabaikan Git
├── README.md               ← Dokumentasi proyek
│
├── model/                  ← Model hasil training (auto-generate)
│   ├── random_forest_model.pkl
│   └── scaler.pkl
│
├── dataset/                ← Dataset gambar jamur dari Kaggle
│   └── edible and poisonous mushroom/
│       ├── edible mushroom/
│       └── poisonous mushroom/
│
├── templates/              ← HTML Templates
│   ├── index.html          ← Halaman utama (upload & prediksi)
│   ├── evaluate.html       ← Halaman evaluasi model
│   └── about.html          ← Halaman tentang aplikasi
│
└── static/
├── css/
│   └── style.css       ← Custom styling
├── js/
│   └── scripts.js      ← Logic upload, preview, fetch API
└── uploads/            ← Gambar upload user (auto-generate)

---

## Cara Menjalankan Lokal

### 1. Clone repository

```bash
git clone https://github.com/SelsaShaf/mushroom-ai-flask.git
cd mushroom-ai-flask
```

### 2. Buat virtual environment

```bash
python -m venv venv
```

### 3. Aktifkan virtual environment

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

### 4. Install dependensi

```bash
pip install -r requirements.txt
```

### 5. Training model

```bash
python train_model.py
```

### 6. Jalankan aplikasi

```bash
python app.py
```

### 7. Buka browser
http://localhost:5000

---

## Cara Penggunaan

1. Buka aplikasi di browser
2. Klik **Mulai Analisis** atau scroll ke bagian upload
3. Drag & drop gambar jamur atau klik **Pilih Gambar**
4. Klik tombol **Analisis Gambar**
5. Tunggu hasil prediksi tampil
6. Lihat label, tingkat kepercayaan, dan probabilitas tiap kelas

---

## Halaman Aplikasi

| Halaman | URL | Keterangan |
|---|---|---|
| Beranda | `/` | Upload gambar dan hasil prediksi |
| Evaluasi | `/evaluate` | Akurasi, confusion matrix, feature importance |
| Tentang | `/about` | Informasi aplikasi, dataset, teknologi |

---

## Deployment

Link aplikasi: 
https://mushroom-ai-flask-production.up.railway.app/
https://mushroom.mushroom-ai.my.id/

---

## Peringatan

Aplikasi ini dikembangkan semata-mata untuk keperluan **akademik dan edukasi**. 
Hasil prediksi tidak boleh dijadikan satu-satunya acuan dalam menentukan keamanan 
jamur untuk dikonsumsi. Selalu konsultasikan dengan ahli sebelum mengonsumsi jamur liar.

---

## Referensi

- [Kaggle Dataset - Edible and Poisonous Mushroom Images](https://www.kaggle.com/datasets/mdismielhossenabir/edible-and-poisonous-mushroom-images)
- [Scikit-Learn Random Forest Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/)
