import os
import numpy as np
import pickle
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# ------------------------------------------------------------
# KONFIGURASI
# ------------------------------------------------------------
IMG_SIZE     = (64, 64)
DATASET_PATH = "dataset/edible and poisonous mushroom"
MODEL_PATH   = "model/random_forest_model.pkl"
SCALER_PATH  = "model/scaler.pkl"

# ------------------------------------------------------------
# FUNGSI: Ekstrak fitur dari 1 gambar
# Buka gambar -> resize -> flatten piksel RGB
# Hasil: 64x64x3 = 12.288 nilai fitur
# ------------------------------------------------------------
def extract_features(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize(IMG_SIZE)
    return np.array(img).flatten()

# ------------------------------------------------------------
# FUNGSI: Load semua gambar dari folder dataset
# Label 0 = edible, Label 1 = poisonous
# ------------------------------------------------------------
def load_dataset():
    X, y = [], []
    labels = {
        "edible mushroom"   : 0,
        "poisonous mushroom": 1
    }

    for label_name, label_val in labels.items():
        folder = os.path.join(DATASET_PATH, label_name)
        files  = [
            f for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        print(f"\n  [LOAD] Folder  : {label_name}")
        print(f"         Jumlah  : {len(files)} gambar")

        for i, fname in enumerate(files):
            fpath = os.path.join(folder, fname)
            try:
                features = extract_features(fpath)
                X.append(features)
                y.append(label_val)
                print(f"         Progress: [{i+1}/{len(files)}] {fname}", end="\r")
            except Exception as e:
                print(f"\n  [ERROR] Gagal membaca {fname} -> {e}")

        print(f"\n  [DONE]  Selesai membaca {label_name}")

    return np.array(X), np.array(y)


# ------------------------------------------------------------
# MAIN: Proses training dari awal hingga simpan model
# ------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 60)
    print("  MUSHROOM AI - TRAINING RANDOM FOREST MODEL")
    print("=" * 60)

    # --------------------------------------------------
    # LANGKAH 1: Membaca dataset
    # --------------------------------------------------
    print("\n[STEP 1/6] Membaca dataset gambar dari folder dataset/")
    X, y = load_dataset()
    print(f"\n  Total gambar terbaca  : {len(X)}")
    print(f"  Edible  (label 0)     : {sum(y == 0)} gambar")
    print(f"  Poisonous (label 1)   : {sum(y == 1)} gambar")

    # --------------------------------------------------
    # LANGKAH 2: Normalisasi fitur
    # Agar nilai piksel antar gambar seragam skalanya
    # --------------------------------------------------
    print("\n[STEP 2/6] Normalisasi fitur menggunakan StandardScaler")
    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("  Normalisasi selesai")

    # --------------------------------------------------
    # LANGKAH 3: Split data training dan testing
    # 80% untuk melatih, 20% untuk menguji model
    # --------------------------------------------------
    print("\n[STEP 3/6] Membagi data -> 80% training / 20% testing")
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y,
        test_size    = 0.2,
        random_state = 42,
        stratify     = y
    )
    print(f"  Data training : {len(X_train)} gambar")
    print(f"  Data testing  : {len(X_test)} gambar")

    # --------------------------------------------------
    # LANGKAH 4: Training model Random Forest
    # n_estimators = jumlah pohon keputusan
    # max_depth    = kedalaman maksimal tiap pohon
    # n_jobs       = pakai semua core CPU
    # --------------------------------------------------
    print("\n[STEP 4/6] Melatih model Random Forest...")
    print("  n_estimators = 100")
    print("  max_depth    = 10")
    print("  Harap tunggu proses training selesai...")
    model = RandomForestClassifier(
        n_estimators = 100,
        max_depth    = 10,
        random_state = 42,
        n_jobs       = -1
    )
    model.fit(X_train, y_train)
    print("  Training selesai")

    # --------------------------------------------------
    # LANGKAH 5: Evaluasi performa model
    # --------------------------------------------------
    print("\n[STEP 5/6] Evaluasi model pada data testing")
    y_pred = model.predict(X_test)
    acc    = accuracy_score(y_test, y_pred)

    print(f"\n  Akurasi Model : {acc * 100:.2f}%")
    print("\n  Classification Report:")
    print("  " + "-" * 50)
    report = classification_report(
        y_test, y_pred,
        target_names=["Edible", "Poisonous"]
    )
    for line in report.split("\n"):
        print(f"  {line}")

    print("\n  Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  {'':20} Pred Edible  Pred Poisonous")
    print(f"  {'Actual Edible':20} {cm[0][0]:^12} {cm[0][1]:^14}")
    print(f"  {'Actual Poisonous':20} {cm[1][0]:^12} {cm[1][1]:^14}")

    # --------------------------------------------------
    # LANGKAH 6: Simpan model dan scaler ke folder model/
    # --------------------------------------------------
    print("\n[STEP 6/6] Menyimpan model ke folder model/")
    os.makedirs("model", exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"  Tersimpan : {MODEL_PATH}")

    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)
    print(f"  Tersimpan : {SCALER_PATH}")

    print("\n" + "=" * 60)
    print("  TRAINING SELESAI")
    print("  Jalankan aplikasi dengan perintah: python app.py")
    print("  Lalu buka browser di: http://localhost:5000")
    print("=" * 60)