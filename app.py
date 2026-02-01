import streamlit as st
import requests

# =========================
# CONFIG (tanpa secrets.toml)
# =========================
APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzzx1oBq47slEDYc32Iw4hAAccDpit55E7GHh0SNQwonLZuNVlz31PZyNr3B09xt9eU/exec"
SECRET_KEY = "rp-2026"

# =========================
# DATA PILIHAN
# =========================
KATEGORI_TOPIK = {
    "A. Pendidikan TIK (strategi/metode/evaluasi/kurikulum)": [
        "Strategi pembelajaran TIK (model/metode mengajar)",
        "Evaluasi hasil belajar TIK (asesmen, penilaian, CBT)",
        "Analisis kesulitan belajar TIK/pemrograman",
        "Motivasi & minat belajar TIK",
        "Literasi digital siswa",
        "Kompetensi pedagogik guru TIK/Informatika",
        "Implementasi/Telaah kurikulum Informatika/TIK",
        "Manajemen kelas digital",
        "STEM dalam pembelajaran TIK/Informatika",
    ],
    "B. E-Learning & Kelas Digital": [
        "Implementasi LMS (Moodle/Google Classroom)",
        "Desain pembelajaran online (sinkron/asinkron)",
        "Pengelolaan pembelajaran kelas digital (Digital Classroom Management)",
        "Efektivitas pembelajaran online vs tatap muka",
        "Efektivitas kuis online / CBT",
        "Analisis aktivitas belajar di LMS (learning analytics sederhana)",
    ],
    "C. Media Pembelajaran Digital (Multimedia/Animasi/DKV)": [
        "Pengembangan media pembelajaran interaktif berbasis multimedia",
        "E-modul / bahan ajar digital",
        "Video pembelajaran interaktif",
        "Animasi pembelajaran (motion graphic)",
        "Desain komunikasi visual untuk pembelajaran",
        "Teknik multimedia untuk meningkatkan pemahaman materi",
    ],
    "D. Game Edukasi & Gamifikasi": [
        "Pengembangan game edukasi",
        "Gamifikasi pembelajaran TIK",
        "Quiz game untuk pembelajaran TIK",
        "Evaluasi efektivitas game edukasi",
        "Game edukasi untuk materi pemrograman/jaringan",
    ],
    "E. Pemrograman untuk Pendidikan (OOP/Web/Mobile/Struktur Data/DB)": [
        "Pembelajaran pemrograman dasar (Scratch/Python)",
        "Pembelajaran OOP (Object-Oriented Programming)",
        "Pembelajaran struktur data",
        "Pembelajaran pemrograman web",
        "Pembelajaran pemrograman mobile",
        "Pembelajaran database programming",
        "Analisis kesalahan umum siswa dalam coding",
        "Pengembangan platform latihan coding sederhana",
        "Computational Thinking dalam pembelajaran Informatika",
    ],
    "F. Produk TIK untuk Pendidikan (Web/Mobile/App/RPL)": [
        "Pengembangan website pembelajaran / Web App",
        "Pengembangan aplikasi mobile pembelajaran",
        "Pengembangan aplikasi edukasi berbasis web",
        "Pengembangan aplikasi edukasi berbasis mobile",
        "Sistem presensi/tugas/nilai sederhana untuk pembelajaran",
    ],
    "G. UI/UX & HCI untuk Pendidikan": [
        "Perancangan UI/UX aplikasi edukasi",
        "Evaluasi usability aplikasi pembelajaran (misal SUS)",
        "User experience siswa dalam aplikasi edukasi",
        "Aksesibilitas aplikasi pembelajaran",
    ],
    "H. Sistem Informasi Pendidikan & Database": [
        "Perancangan sistem informasi pendidikan/sekolah",
        "Sistem informasi akademik sederhana",
        "Sistem informasi perpustakaan sekolah sederhana",
        "Sistem informasi manajemen nilai/tugas",
        "Perancangan database untuk kebutuhan sekolah",
    ],
    "I. Artificial Intelligence (AI) untuk Pendidikan": [
        "Chatbot pembelajaran (AI tutor)",
        "Pemanfaatan AI sebagai asisten belajar (etis)",
        "AI untuk pembuatan soal/latihan",
        "Rekomendasi materi belajar berbasis AI",
        "AI untuk evaluasi otomatis (penilaian)",
    ],
    "J. IoT untuk Pendidikan": [
        "Pengembangan alat peraga IoT untuk pembelajaran",
        "Smart classroom sederhana (IoT)",
        "IoT untuk pembelajaran STEM",
        "Monitoring kelas/lab berbasis IoT",
    ],
    "K. Data Mining / Learning Analytics untuk Pendidikan": [
        "Analisis pola belajar siswa dari data",
        "Prediksi hasil belajar siswa (dasar)",
        "Dashboard analisis hasil belajar",
        "Data warehouse untuk data akademik (dasar)",
    ],
    "L. Jaringan Komputer & Keamanan untuk Pendidikan": [
        "Pembelajaran jaringan komputer (analisis kesulitan)",
        "Media pembelajaran jaringan komputer",
        "Literasi keamanan digital siswa",
        "Edukasi cyber safety di sekolah",
        "Pengenalan kriptografi untuk siswa",
        "Keamanan jaringan lab sekolah (konsep)",
    ],
    "M. Sistem Pakar & Sistem Penunjang Keputusan (Pendidikan)": [
        "Sistem pakar untuk rekomendasi belajar",
        "Sistem pakar untuk pemetaan kesulitan belajar",
        "Sistem penunjang keputusan untuk pemetaan kemampuan siswa",
        "Sistem rekomendasi pembelajaran sederhana",
    ],
    "N. Technopreneur / Kewirausahaan (produk edukasi)": [
        "Rencana produk edukasi berbasis technopreneur",
        "Model bisnis aplikasi edukasi (sederhana)",
        "Inovasi produk TIK untuk sekolah",
    ],
    "O. Lainnya (tulis sendiri)": []
}

RENCANA_OUTPUT = ["Non-produk", "Produk", "Produk dan uji efektivitas"]
JENIS_PRODUK = [
    "Media pembelajaran interaktif",
    "E-modul / bahan ajar digital",
    "Website pembelajaran / Web App",
    "Aplikasi mobile",
    "Game edukasi",
    "Chatbot/AI tutor",
    "IoT alat peraga / smart classroom",
    "Sistem informasi pendidikan sederhana",
    "Dashboard evaluasi / learning analytics",
    "Lainnya"
]

KONTEKS = ["KKN", "PLP", "KKN/PLP (gabungan)", "Di luar KKN/PLP", "Belum menentukan"]
TEMPAT = ["SMP", "SMA", "SMK", "Perguruan tinggi", "Komunitas/kursus", "Pembelajaran online", "Belum menentukan"]
SUBJEK = ["Siswa SMP", "Siswa SMA", "Siswa SMK", "Mahasiswa", "Guru TIK/Informatika", "Lainnya"]

METODE = [
    "R&D / Penelitian Pengembangan",
    "Eksperimen / Quasi Eksperimen",
    "Survei (kuesioner/angket)",
    "Deskriptif Kuantitatif",
    "Deskriptif Kualitatif",
    "Studi Kasus",
    "Korelasional",
    "Komparatif",
    "Evaluasi",
    "Analisis Kebutuhan (needs analysis)",
    "Mixed Method",
    "Belum menentukan"
]

# =========================
# Helper
# =========================
def is_empty(x) -> bool:
    return x is None or str(x).strip() == ""

def send_to_sheet(payload: dict, url: str, secret: str):
    payload = dict(payload)
    payload["secret"] = secret
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()
    return r.json()

# =========================
# UI
# =========================
st.set_page_config(page_title="Rencana Penelitian TIK", page_icon="", layout="centered")
st.title("Form Rencana Penelitian (Menuju Proposal)")

st.subheader("Minat Topik Penelitian")

kategori = st.selectbox(
    "4) Kategori minat penelitian *",
    [""] + list(KATEGORI_TOPIK.keys()),
    key="kategori"
)

if kategori and kategori != "O. Lainnya (tulis sendiri)":
    topik = st.selectbox(
        "5) Pilih topik minat penelitian (sesuai kategori) *",
        [""] + KATEGORI_TOPIK[kategori],
        key="topik"
    )
elif kategori == "O. Lainnya (tulis sendiri)":
    topik = st.text_input(
        "5) Tulis topik minat penelitian kamu *",
        key="topik_lainnya"
    )
else:
    topik = ""

with st.form("rencana_penelitian_9"):
    st.subheader("Identitas")
    nama = st.text_input("1) Nama lengkap *")
    nim = st.text_input("2) NIM *")
    kelas = st.text_input("3) Kelas *")

    st.subheader("Rencana Output Penelitian")
    output = st.radio("6) Rencana output penelitian *", RENCANA_OUTPUT, horizontal=True)

    jenis_produk = []
    if output in ["Produk", "Produk dan uji efektivitas"]:
        jenis_produk = st.multiselect(
            "Jika produk, pilih jenis produk (maks 2) *",
            JENIS_PRODUK,
            max_selections=2
        )

    st.subheader("Tempat & Subjek Penelitian (menyesuaikan KKN/PLP)")
    konteks = st.selectbox("7a) Konteks kegiatan (KKN/PLP) *", [""] + KONTEKS)
    tempat = st.selectbox("7b) Tempat penelitian *", [""] + TEMPAT)
    subjek = st.selectbox("7c) Subjek penelitian *", [""] + SUBJEK)

    st.subheader("Metode Penelitian")
    metode = st.selectbox("8) Metode penelitian *", [""] + METODE)

    st.subheader("Judul Sementara")
    judul = st.text_input("9) Judul sementara penelitian *")

    submitted = st.form_submit_button("Kirim")

if submitted:
    errors = []

    # Validasi config
    if is_empty(APPS_SCRIPT_URL):
        errors.append("APPS_SCRIPT_URL belum diisi (konfigurasi aplikasi).")
    if is_empty(SECRET_KEY):
        errors.append("SECRET_KEY belum diisi (konfigurasi aplikasi).")

    # Validasi input user
    if is_empty(nama): errors.append("Nama lengkap wajib diisi.")
    if is_empty(nim): errors.append("NIM wajib diisi.")
    if is_empty(kelas): errors.append("Kelas wajib diisi.")
    if is_empty(kategori): errors.append("Kategori minat wajib dipilih.")
    if is_empty(topik): errors.append("Topik minat wajib dipilih/diisi.")

    if output in ["Produk", "Produk dan uji efektivitas"] and len(jenis_produk) == 0:
        errors.append("Karena memilih output produk, pilih minimal 1 jenis produk.")

    if is_empty(konteks): errors.append("Konteks (KKN/PLP) wajib dipilih.")
    if is_empty(tempat): errors.append("Tempat penelitian wajib dipilih.")
    if is_empty(subjek): errors.append("Subjek penelitian wajib dipilih.")
    if is_empty(metode): errors.append("Metode penelitian wajib dipilih.")
    if is_empty(judul): errors.append("Judul sementara wajib diisi.")

    if errors:
        st.error("Mohon perbaiki:\n- " + "\n- ".join(errors))
    else:
        payload = {
            "nama_lengkap": nama,
            "nim": nim,
            "kelas": kelas,
            "kategori_minat": kategori,
            "topik_minat": topik,
            "rencana_output": output,
            "jenis_produk": jenis_produk,
            "konteks_kkn_plp": konteks,
            "tempat_penelitian": tempat,
            "subjek_penelitian": subjek,
            "metode_penelitian": metode,
            "judul_sementara": judul,
        }

        try:
            res = send_to_sheet(payload, APPS_SCRIPT_URL, SECRET_KEY)
            if res.get("ok") is True:
                st.success("Tersimpan ke Google Sheet. Terima kasih!")
            else:
                st.error(f"Gagal menyimpan: {res}")
        except Exception as e:
            st.error(f"Error saat mengirim ke Apps Script: {e}")
