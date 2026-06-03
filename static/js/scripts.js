// ============================================================
// MUSHROOM AI - SCRIPTS.JS
// Handle upload, preview, prediksi, dan tampilkan hasil
// ============================================================

// ------------------------------------------------------------
// AMBIL SEMUA ELEMEN DOM YANG DIBUTUHKAN
// ------------------------------------------------------------
const dropZone     = document.getElementById("dropZone");
const fileInput    = document.getElementById("fileInput");
const dropDefault  = document.getElementById("dropDefault");
const dropPreview  = document.getElementById("dropPreview");
const previewImg   = document.getElementById("previewImg");
const previewName  = document.getElementById("previewName");
const analyzeBtn   = document.getElementById("analyzeBtn");
const changeBtn    = document.getElementById("changeBtn");
const loadingState = document.getElementById("loadingState");
const resultCard   = document.getElementById("resultCard");
const resetBtn     = document.getElementById("resetBtn");

// File yang sedang dipilih user
let selectedFile = null;

// ------------------------------------------------------------
// DRAG & DROP — seret gambar ke area upload
// ------------------------------------------------------------

// Saat file diseret masuk ke drop zone
dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

// Saat file keluar dari drop zone tanpa dilepas
dropZone.addEventListener("dragleave", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
});

// Saat file dilepas di drop zone
dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
});

// Klik drop zone untuk membuka file picker
dropZone.addEventListener("click", (e) => {
    // Hanya trigger jika klik bukan dari tombol di dalam
    if (
        e.target === dropZone ||
        e.target.closest("#dropDefault")
    ) {
        fileInput.click();
    }
});

// Saat user memilih file dari file picker
fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) handleFile(fileInput.files[0]);
});

// Tombol ganti gambar — kembali ke state default
changeBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.click();
});

// ------------------------------------------------------------
// HANDLE FILE — validasi dan tampilkan preview
// ------------------------------------------------------------
function handleFile(file) {
    // Validasi format file
    const allowed = ["image/jpeg", "image/jpg", "image/png"];
    if (!allowed.includes(file.type)) {
        showNotif("Format file tidak didukung. Gunakan JPG atau PNG.", "error");
        return;
    }

    // Validasi ukuran file (max 16MB)
    if (file.size > 16 * 1024 * 1024) {
        showNotif("Ukuran file terlalu besar. Maksimal 16MB.", "error");
        return;
    }

    // Simpan file ke variabel global
    selectedFile = file;

    // Tampilkan preview gambar menggunakan FileReader
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src    = e.target.result;
        previewName.textContent = file.name + " — " + formatSize(file.size);

        // Ganti tampilan drop zone ke state preview
        dropDefault.style.display = "none";
        dropPreview.style.display = "block";

        // Aktifkan tombol analisis
        analyzeBtn.disabled = false;

        // Sembunyikan hasil sebelumnya jika ada
        resultCard.style.display = "none";
    };
    reader.readAsDataURL(file);
}

// ------------------------------------------------------------
// FORMAT UKURAN FILE — ubah bytes ke KB / MB
// ------------------------------------------------------------
function formatSize(bytes) {
    if (bytes < 1024 * 1024) {
        return (bytes / 1024).toFixed(1) + " KB";
    }
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

// ------------------------------------------------------------
// TOMBOL ANALISIS — kirim gambar ke server Flask
// ------------------------------------------------------------
analyzeBtn.addEventListener("click", async () => {
    if (!selectedFile) return;

    // Tampilkan loading, sembunyikan tombol dan hasil lama
    analyzeBtn.style.display  = "none";
    loadingState.style.display = "block";
    resultCard.style.display   = "none";

    // Buat form data untuk dikirim ke endpoint /predict
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        // Kirim request POST ke Flask
        const response = await fetch("/predict", {
            method : "POST",
            body   : formData,
        });

        // Parsing response JSON
        const data = await response.json();

        if (data.error) {
            // Tampilkan pesan error dari server
            showNotif(data.error, "error");
        } else {
            // Tampilkan hasil prediksi
            showResult(data);
        }

    } catch (err) {
        // Error jaringan atau server tidak merespons
        showNotif("Terjadi kesalahan. Pastikan server berjalan.", "error");
        console.error("Fetch error:", err);

    } finally {
        // Sembunyikan loading, tampilkan kembali tombol analisis
        loadingState.style.display = "none";
        analyzeBtn.style.display   = "block";
    }
});

// ------------------------------------------------------------
// TAMPILKAN HASIL PREDIKSI
// ------------------------------------------------------------
function showResult(data) {
    const isEdible = data.label_id === "edible";

    // --- Header ---
    // Set warna header sesuai hasil prediksi
    const resultHeader = document.getElementById("resultHeader");
    resultHeader.className = `result-header ${data.label_id}`;

    // Set ikon Font Awesome sesuai kelas
    document.getElementById("resultIcon").className = isEdible
        ? "fa-solid fa-circle-check"
        : "fa-solid fa-skull-crossbones";

    // Set tag kecil di atas judul
    document.getElementById("resultTag").textContent = isEdible
        ? "HASIL KLASIFIKASI — AMAN"
        : "HASIL KLASIFIKASI — BERBAHAYA";

    // Set judul hasil
    document.getElementById("resultTitle").textContent =
        data.label + " — " + data.label_indo;

    // Set subjudul
    document.getElementById("resultSub").textContent = isEdible
        ? "Jamur ini diprediksi aman untuk dikonsumsi"
        : "Jamur ini diprediksi berbahaya dan beracun";

    // --- Gambar hasil ---
    document.getElementById("resultImage").src = data.image_url;

    // --- Confidence Bar ---
    // Animasi bar berjalan setelah 100ms agar transisi CSS terlihat
    const bar = document.getElementById("confidenceBar");
    bar.className = `metric-bar ${data.label_id}`;
    bar.style.width = "0%";
    setTimeout(() => {
        bar.style.width = data.confidence + "%";
    }, 100);

    // Set nilai teks confidence
    document.getElementById("confidenceVal").textContent =
        data.confidence + "%";

    // --- Probabilitas per kelas ---
    document.getElementById("probEdible").textContent    = data.prob_edible + "%";
    document.getElementById("probPoisonous").textContent = data.prob_poisonous + "%";

    // --- Alert / Peringatan ---
    const alertEl = document.getElementById("resultAlert");
    alertEl.className = isEdible
        ? "result-alert alert-edible show"
        : "result-alert alert-poisonous show";

    alertEl.innerHTML = isEdible
        ? "<i class='fa-solid fa-circle-info me-2'></i><strong>Catatan:</strong> Meskipun diprediksi aman, selalu konsultasikan dengan ahli sebelum mengonsumsi jamur liar."
        : "<i class='fa-solid fa-triangle-exclamation me-2'></i><strong>Peringatan:</strong> Jamur ini diprediksi beracun. Jangan dikonsumsi dalam kondisi apapun.";

    // --- Tampilkan result card dengan animasi ---
    resultCard.style.display = "block";

    // Scroll halus ke result card
    setTimeout(() => {
        resultCard.scrollIntoView({
            behavior: "smooth",
            block   : "nearest"
        });
    }, 100);
}

// ------------------------------------------------------------
// TOMBOL RESET — kembali ke state awal untuk analisis baru
// ------------------------------------------------------------
resetBtn.addEventListener("click", () => {
    // Kosongkan file terpilih
    selectedFile   = null;
    fileInput.value = "";

    // Reset preview
    previewImg.src = "";
    previewName.textContent = "";

    // Kembali ke tampilan default drop zone
    dropDefault.style.display = "block";
    dropPreview.style.display = "none";

    // Nonaktifkan tombol analisis
    analyzeBtn.disabled = true;

    // Sembunyikan result card
    resultCard.style.display = "none";

    // Scroll kembali ke area upload
    document.getElementById("upload-section").scrollIntoView({
        behavior: "smooth",
        block   : "start"
    });
});

// ------------------------------------------------------------
// NOTIFIKASI — tampilkan pesan error atau sukses sementara
// ------------------------------------------------------------
function showNotif(message, type = "info") {
    // Hapus notifikasi sebelumnya jika masih ada
    const existing = document.getElementById("notif-toast");
    if (existing) existing.remove();

    // Buat elemen notifikasi
    const notif = document.createElement("div");
    notif.id = "notif-toast";
    notif.style.cssText = `
        position        : fixed;
        top             : 80px;
        right           : 24px;
        z-index         : 9999;
        background      : ${type === "error" ? "#b5172f" : "#2d6a4f"};
        color           : white;
        padding         : 14px 20px;
        border-radius   : 12px;
        font-family     : 'Inter', sans-serif;
        font-size       : 0.875rem;
        font-weight     : 600;
        box-shadow      : 0 8px 32px rgba(0,0,0,0.2);
        display         : flex;
        align-items     : center;
        gap             : 10px;
        max-width       : 340px;
        animation       : notif-in 0.3s cubic-bezier(0.4,0,0.2,1);
    `;

    // Ikon sesuai tipe notifikasi
    const icon = type === "error"
        ? "fa-solid fa-circle-xmark"
        : "fa-solid fa-circle-check";

    notif.innerHTML = `<i class="${icon}"></i><span>${message}</span>`;
    document.body.appendChild(notif);

    // Hapus notifikasi otomatis setelah 3.5 detik
    setTimeout(() => {
        notif.style.opacity   = "0";
        notif.style.transform = "translateX(20px)";
        notif.style.transition = "all 0.3s ease";
        setTimeout(() => notif.remove(), 300);
    }, 3500);
}

// Tambahkan keyframe animasi notifikasi ke head
const style = document.createElement("style");
style.textContent = `
    @keyframes notif-in {
        from { opacity: 0; transform: translateX(20px); }
        to   { opacity: 1; transform: translateX(0); }
    }
`;
document.head.appendChild(style);