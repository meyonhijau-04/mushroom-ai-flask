import os
import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify
from PIL import Image
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import uuid

# ------------------------------------------------------------
# INISIALISASI FLASK
# ------------------------------------------------------------
app = Flask(__name__)
app.config['UPLOAD_FOLDER']      = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # max 16MB
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ------------------------------------------------------------
# LOAD MODEL & SCALER
# Diload sekali saja saat aplikasi pertama kali dijalankan
# ------------------------------------------------------------
IMG_SIZE = (64, 64)

with open("model/random_forest_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# ------------------------------------------------------------
# HELPER: Cek format file yang diizinkan
# ------------------------------------------------------------
def allowed_file(filename):
    allowed = {"jpg", "jpeg", "png"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed

# ------------------------------------------------------------
# HELPER: Ekstrak fitur piksel dari gambar
# Resize ke 64x64, flatten jadi 12.288 nilai
# ------------------------------------------------------------
def extract_features(image_path):
    img      = Image.open(image_path).convert("RGB")
    img      = img.resize(IMG_SIZE)
    features = np.array(img).flatten()
    return features

# ------------------------------------------------------------
# HELPER: Prediksi gambar jamur
# Return dict berisi label, confidence, probabilitas
# ------------------------------------------------------------
def predict_mushroom(image_path):
    features        = extract_features(image_path)
    features_scaled = scaler.transform([features])
    prediction      = model.predict(features_scaled)[0]
    probabilities   = model.predict_proba(features_scaled)[0]

    return {
        "label"         : "Edible" if prediction == 0 else "Poisonous",
        "label_id"      : "edible" if prediction == 0 else "poisonous",
        "label_indo"    : "Dapat Dimakan" if prediction == 0 else "Beracun",
        "confidence"    : round(float(max(probabilities)) * 100, 2),
        "prob_edible"   : round(float(probabilities[0]) * 100, 2),
        "prob_poisonous": round(float(probabilities[1]) * 100, 2),
    }

# ------------------------------------------------------------
# HELPER: Ambil data evaluasi model untuk halaman evaluate
# Load dataset -> prediksi -> hitung metrik
# ------------------------------------------------------------
def get_evaluation_data():
    from train_model import load_dataset

    X, y         = load_dataset()
    X_scaled     = scaler.transform(X)
    _, X_test, _, y_test = train_test_split(
        X_scaled, y,
        test_size    = 0.2,
        random_state = 42,
        stratify     = y
    )
    y_pred = model.predict(X_test)

    # Akurasi
    acc = round(accuracy_score(y_test, y_pred) * 100, 2)

    # Classification report dalam bentuk dict
    report = classification_report(
        y_test, y_pred,
        target_names=["Edible", "Poisonous"],
        output_dict=True
    )

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred).tolist()

    # Feature importance top 10
    importances  = model.feature_importances_
    top_indices  = np.argsort(importances)[::-1][:10]
    top_features = [
        {
            "name" : f"Pixel Feature {idx+1}",
            "value": round(float(importances[i]) * 100, 4)
        }
        for idx, i in enumerate(top_indices)
    ]

    return {
        "accuracy"    : acc,
        "report"      : report,
        "cm"          : cm,
        "top_features": top_features,
        "total_train" : len(X) - len(X_test),
        "total_test"  : len(X_test),
        "total_data"  : len(X)
    }

# ------------------------------------------------------------
# ROUTES
# ------------------------------------------------------------

# Halaman utama: upload gambar dan tampilkan hasil prediksi
@app.route("/")
def index():
    return render_template("index.html")

# Halaman tentang: informasi aplikasi, dataset, teknologi
@app.route("/about")
def about():
    return render_template("about.html")

# Halaman evaluasi: akurasi, confusion matrix, feature importance
@app.route("/evaluate")
def evaluate():
    data = get_evaluation_data()
    return render_template("evaluate.html", data=data)

# API endpoint: terima gambar, kembalikan prediksi dalam JSON
@app.route("/predict", methods=["POST"])
def predict():
    # Validasi: pastikan ada file di request
    if "file" not in request.files:
        return jsonify({"error": "Tidak ada file yang dikirim"}), 400

    file = request.files["file"]

    # Validasi: pastikan file dipilih
    if file.filename == "":
        return jsonify({"error": "Tidak ada file dipilih"}), 400

    # Validasi: pastikan format file didukung
    if not allowed_file(file.filename):
        return jsonify({"error": "Format tidak didukung. Gunakan JPG atau PNG"}), 400

    # Simpan file dengan nama unik agar tidak bentrok
    ext      = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Jalankan prediksi
    result              = predict_mushroom(filepath)
    result["image_url"] = f"/static/uploads/{filename}"

    return jsonify(result)

# ------------------------------------------------------------
# RUN: PORT diambil otomatis dari environment Railway
# ------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)