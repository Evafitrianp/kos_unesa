"""
utils/algoritma.py
══════════════════════════════════════════════════════════════════════════════
Modul inti algoritma Sistem Rekomendasi Kos UNESA Ketintang.
Berisi implementasi lengkap:
  - Tahap 1 : Pra-pemrosesan & Filtering (Strict / Relaxed)
  - Tahap 2 : K-Means Clustering (scikit-learn, k=3)
  - Tahap 3 : MOORA (Multi-Objective Optimization on the basis of Ratio Analysis)
  - Tahap 4 : Format Output → list[dict] siap render UI

Catatan kolom CSV  (data_kos.csv):
  - Fasilitas dikodekan 'Y' (Ya) / 'T' (Tidak)
  - Jarak   → float, satuan KM
  - Harga   → int,   satuan Rupiah/bulan
  - Kontak (WA) → float64 (ada 10 baris NaN)
  - Ukuran Kamar (M2) → float (luas dalam m²)
══════════════════════════════════════════════════════════════════════════════
"""

import math
import numpy  as np
import pandas as pd
from sklearn.cluster      import KMeans
from sklearn.preprocessing import MinMaxScaler


# ─────────────────────────────────────────────────────────────────────────────
#  KONSTANTA & TABEL PEMETAAN
# ─────────────────────────────────────────────────────────────────────────────

# Path ke file dataset CSV (relatif terhadap root proyek)
CSV_PATH = "data_kos.csv"

# Nama kolom fasilitas di CSV (urutan ini dipakai untuk loop)
KOLOM_FASILITAS = [
    "Kasur", "Lemari", "Listrik", "Wifi", "Air",
    "KM Dalam", "Meja Belajar", "Kursi", "AC", "TV",
    "Satpam", "Dapur Bersama", "Parkiran Motor",
]

# Pemetaan: nama fasilitas di form UI → nama kolom di CSV
# Key  = label yang tampil di multiselect Streamlit (pages/search.py)
# Value = nama kolom di data_kos.csv (None = tidak ada kolom padanannya)
FASILITAS_UI_KE_CSV: dict[str, str | None] = {
    "WiFi"              : "Wifi",
    "AC"                : "AC",
    "Kamar Mandi Dalam" : "KM Dalam",
    "Lemari"            : "Lemari",
    "Meja Belajar"      : "Meja Belajar",
    "Kursi"             : "Kursi",
    "Kasur"             : "Kasur",
    "Dapur Bersama"     : "Dapur Bersama",
    "Parkiran Motor"    : "Parkiran Motor",
    "Satpam"            : "Satpam",
    "Air PDAM"          : "Air",
    "TV"                : "TV",
    "Listrik"           : "Listrik",
}

# Pemetaan: pilihan dropdown Ukuran Kamar di UI → luas minimum (m²)
UKURAN_UI_KE_M2: dict[str, float] = {
    "Semua Ukuran"       : 0.0,
    "2x3 m (Kecil)"      : 6.0,
    "3x3 m (Standar Kecil)": 9.0,
    "3x4 m (Standar)"    : 12.0,
    "4x4 m (Luas)"       : 16.0,
    "4x5 m (Sangat Luas)": 20.0,
}

# Pool foto placeholder (Unsplash) — dipakai karena CSV tidak menyimpan URL foto.
# Foto dipilih secara round-robin berdasarkan indeks baris agar bervariasi.
FOTO_POOL = [
    "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=600&q=80",
    "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600&q=80",
    "https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=600&q=80",
    "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=600&q=80",
    "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=600&q=80",
    "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=600&q=80",
    "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=600&q=80",
    "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&q=80",
    "https://images.unsplash.com/photo-1631049552057-403cdb8f0658?w=600&q=80",
    "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600&q=80",
]

# ─────────────────────────────────────────────────────────────────────────────
#  TAHAP 0 : LOAD & PRA-PEMROSESAN DATASET
# ─────────────────────────────────────────────────────────────────────────────

def _load_dataset() -> pd.DataFrame:

    # Baca CSV dari path yang sudah didefinisikan
    df = pd.read_csv(CSV_PATH)

    # 1. Hapus spasi dari nama kolom
    df.columns = df.columns.str.strip()
    # 2. Bersihkan kolom Kontak WA 
    df["Kontak (WA)"] = df["Kontak (WA)"].apply(
        lambda x: f"62{int(x)}" if pd.notna(x) else "0"
    )
    # 3. Konversi kolom fasilitas 'Y'/'T' → 1/0 (string ke integer)
    for kolom in KOLOM_FASILITAS:
        df[kolom] = df[kolom].map({"Y": 1, "T": 0}).fillna(0).astype(int)

    return df


# ─────────────────────────────────────────────────────────────────────────────
#  TAHAP 1A : STRICT FILTERING
# ─────────────────────────────────────────────────────────────────────────────

def _strict_filter(
    df          : pd.DataFrame,
    budget      : int,          # Rp — batas atas harga dari slider UI
    jarak_max_km: float,        # km — sudah dikonversi dari meter ke km
    fac_cols    : list[str],    # daftar kolom CSV fasilitas yang dipilih user
    ukuran_min  : float,        # m² minimum dari pilihan dropdown UI
    jenis       : str,          # 'Putra' | 'Putri' | 'Campur'
) -> pd.DataFrame:
    hasil = df.copy()
    # a. Filter Harga 
    hasil = hasil[hasil["Harga (Bulan)"] <= budget]
    # b. Filter Jarak 
    hasil = hasil[hasil["Jarak (km)"] <= jarak_max_km]
    # c. Filter Ukuran Kamar 
    if ukuran_min > 0:  # 0 berarti "Semua Ukuran" → tidak filter
        hasil = hasil[hasil["Ukuran Kamar (M2)"] >= ukuran_min]
    # d. Filter Jenis Kos 
    if jenis in ("Putra", "Putri", "Campur"):
        hasil = hasil[hasil["Jenis"] == jenis]
    # e. Filter Fasilitas 
    for col in fac_cols:
        hasil = hasil[hasil[col] == 1]

    return hasil


# ─────────────────────────────────────────────────────────────────────────────
#  TAHAP 1B : RELAXED FILTERING
# ─────────────────────────────────────────────────────────────────────────────

def _relaxed_filter(
    df          : pd.DataFrame,
    budget      : int,
    jarak_max_km: float,
    fac_cols    : list[str],
    ukuran_min  : float,
    jenis       : str,
) -> pd.DataFrame:
    hasil = df.copy()
    # Budget +20% 
    budget_relax = budget * 1.20
    hasil = hasil[hasil["Harga (Bulan)"] <= budget_relax]
    # Jarak +0.5 km 
    jarak_relax = jarak_max_km + 0.15
    hasil = hasil[hasil["Jarak (km)"] <= jarak_relax]
    # Ukuran tetap (tidak dilonggarkan) 
    if ukuran_min > 0:
        hasil = hasil[hasil["Ukuran Kamar (M2)"] >= ukuran_min]
    # Jenis tetap (tidak dilonggarkan) 
    if jenis in ("Putra", "Putri", "Campur"):
        hasil = hasil[hasil["Jenis"] == jenis]
    # Fasilitas: minimal 75% cocok 
    if fac_cols:
        # Hitung jumlah fasilitas yang dimiliki setiap kos dari daftar pilihan user
        hasil["_fac_match_count"] = hasil[fac_cols].sum(axis=1)
        # Tentukan ambang batas: 75% dari total fasilitas yang diminta
        min_match = math.ceil(len(fac_cols) * 0.75)
        hasil = hasil[hasil["_fac_match_count"] >= min_match]
        hasil = hasil.drop(columns=["_fac_match_count"])

    return hasil


# ─────────────────────────────────────────────────────────────────────────────
#  TAHAP 2 : K-MEANS CLUSTERING
# ─────────────────────────────────────────────────────────────────────────────

def _kmeans_clustering(df: pd.DataFrame) -> pd.DataFrame:

    # 1. Pilih 4 atribut sebagai fitur K-Means
    fitur_kmeans = ["Harga (Bulan)", "Jarak (km)", "Total Fasilitas", "Ukuran Kamar (M2)"]
    X = df[fitur_kmeans].values   # konversi ke numpy array 

    # 2. Normalisasi Min-Max 
    scaler   = MinMaxScaler() # X_norm = (X - X_min) / (X_max - X_min)
    X_normal = scaler.fit_transform(X)
    
    # 3. Jalankan K-Means 
    kmeans = KMeans(
        n_clusters   = 3, # jumlah cluster yang diinginkan (Ekonomis/Standar/Premium)
        max_iter     = 300, # iterasi maksimal sebelum konvergensi dianggap gagal
        n_init       = 10, # dijalankan 10 kali dengan centroid awal berbeda, diambil hasil terbaik (inertia terkecil)
        random_state = 42, # seed agar hasil reproducible di setiap run
    )
    df = df.copy()
    df["_cluster_id"] = kmeans.fit_predict(X_normal)  # angka: 0, 1, atau 2

    # 4. Tentukan label cluster berdasarkan rata-rata harga 
    rata_harga = (
        df.groupby("_cluster_id")["Harga (Bulan)"]
        .mean()
        .sort_values()   # urut dari terendah ke tertinggi
    )
    # rata_harga.index[0] = cluster_id dengan harga terendah (Ekonomis)
    # rata_harga.index[1] = cluster_id dengan harga menengah (Standar)
    # rata_harga.index[2] = cluster_id dengan harga tertinggi (Premium)
    label_map = {
        rata_harga.index[0]: ("Ekonomis", "badge-ekonomis"),
        rata_harga.index[1]: ("Standar",  "badge-standar"),
        rata_harga.index[2]: ("Premium",  "badge-premium"),
    }

    # Terapkan label ke dataframe
    df["cluster"]       = df["_cluster_id"].map(lambda cid: label_map[cid][0])
    df["cluster_badge"] = df["_cluster_id"].map(lambda cid: label_map[cid][1])
    df = df.drop(columns=["_cluster_id"])   # hapus kolom bantu

    return df


# ─────────────────────────────────────────────────────────────────────────────
#  TAHAP 3 : MOORA
# ─────────────────────────────────────────────────────────────────────────────

def _moora_ranking(df: pd.DataFrame, jenis_user: str) -> pd.DataFrame:

    df = df.copy()
    # 1. Konversi 'Jenis' menjadi skor numerik
    def skor_jenis(jenis_kos: str) -> float:
        if jenis_user == "Campur": # User tidak memilih jenis spesifik → semua jenis sama baiknya
            return 1.0
        elif jenis_kos == jenis_user: # kos yang sesuai preferensi user
            return 1.0
        elif jenis_kos == "Campur": # kos 'Campur' selalu bisa diterima
            return 0.8
        else:
            return 0.3 # kos yang tidak sesuai sama sekali

    df["_skor_jenis"] = df["Jenis"].apply(skor_jenis)

    # 2. Buat matriks keputusan X 
    kolom_moora = [
        "Harga (Bulan)",       # Cost
        "Jarak (km)",          # Cost
        "Total Fasilitas",     # Benefit
        "Ukuran Kamar (M2)",   # Benefit
        "_skor_jenis",         # Benefit
    ]
    X = df[kolom_moora].values.astype(float)  # shape: (n_kos, 5)

    # 3. Normalisasi Vektor 
    norm       = np.sqrt(np.sum(X ** 2, axis=0))   # Menghitung penyebut: Akar kuadrat dari total/jumlah kuadrat (X^2) pada setiap kolom kriteria
    norm       = np.where(norm == 0, 1e-9, norm)   # Jika ada penyebut bernilai 0, diganti dengan angka sangat kecil (0.000000001)
    X_norm     = X / norm                          # Membagi matriks asli (X) dengan penyebut (norm) untuk mendapatkan Matriks Ternormalisasi

    # 4. Matriks Terbobot
    # w = [w_harga, w_jarak, w_fasilitas, w_ukuran, w_jenis]
    bobot = np.array([0.25, 0.25, 0.25, 0.15, 0.10])   # total = 1.00
    V     = X_norm * bobot   

    # 5. Hitung Nilai Akhir Y
    # Indeks kolom:  0=Harga(Cost), 1=Jarak(Cost), 2=Fasilitas(Benefit),
    #                3=Ukuran(Benefit), 4=Jenis(Benefit)
    idx_cost    = [0, 1]        # kolom yang bersifat Cost (diminimalkan)
    idx_benefit = [2, 3, 4]     # kolom yang bersifat Benefit (dimaksimalkan)

    total_benefit = V[:, idx_benefit].sum(axis=1)  # Σ benefit per kos
    total_cost    = V[:, idx_cost   ].sum(axis=1)  # Σ cost    per kos

    # Nilai MOORA akhir: Y = Benefit - Cost
    Y = total_benefit - total_cost   

    # Normalisasi Y ke rentang [0, 1] untuk kemudahan tampilan
    Y_min, Y_max = Y.min(), Y.max()
    if Y_max > Y_min:
        Y_norm = (Y - Y_min) / (Y_max - Y_min)
    else:
        # Semua kos punya skor sama → berikan nilai 0.5
        Y_norm = np.full_like(Y, 0.5)

    # Simpan skor ke dataframe
    df["skor_moora"] = Y_norm

    # Hapus kolom bantu sementara
    df = df.drop(columns=["_skor_jenis"])

    # 6. Urutkan dari skor MOORA tertinggi ke terendah
    df = df.sort_values("skor_moora", ascending=False).reset_index(drop=True)

    return df


# ─────────────────────────────────────────────────────────────────────────────
#  TAHAP 4 : HITUNG KESESUAIAN & FORMAT OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

def _hitung_kesesuaian(
    row         : pd.Series,
    budget      : int,
    jarak_max_km: float,
    fac_cols    : list[str],
    ukuran_min  : float,
    jenis       : str,
) -> int:

    skor = 0.0
    total_kriteria = 5.0 

    # 1. Kriteria Harga (Diberi poin penuh 1.0 jika harga kos <= batas budget user)
    if row["Harga (Bulan)"] <= budget:
        skor += 1.0
        
    # 2. Kriteria Jarak (Diberi poin penuh 1.0 jika jarak kos <= batas jarak user)
    if row["Jarak (km)"] <= jarak_max_km:
        skor += 1.0
        
    # 3. Kriteria Ukuran (Diberi poin penuh 1.0 jika user tidak milih, atau ukuran asli kos >= pilihan user)
    if ukuran_min == 0 or row["Ukuran Kamar (M2)"] >= ukuran_min:
        skor += 1.0
        
    # 4. Kriteria Jenis (Diberi poin penuh 1.0 HANYA jika gender kos cocok 100% dengan user)
    if row["Jenis"] == jenis:
        skor += 1.0                  
        
    # 5. Kriteria Fasilitas (Dihitung proporsional. Contoh: minta 4 fasilitas, ada 3, maka dapat 3/4 = 0.75 poin)
    if fac_cols:
        fasilitas_cocok = sum(1 for col in fac_cols if row[col] == 1)
        skor += (fasilitas_cocok / len(fac_cols))
    else:
        skor += 1.0  # Otomatis dapat poin 1.0 jika user tidak mensyaratkan fasilitas apa-apa
    
    # Hitung persentase akhir: (Total poin yang didapat / 5 kriteria) dikali 100%
    persentase = (skor / total_kriteria) * 100

    return round(persentase, 2)


def _buat_deskripsi(row: pd.Series) -> str:

    # Gunakan Catatan asli jika tersedia
    if pd.notna(row.get("Catatan", None)) and str(row["Catatan"]).strip():
        tambahan = f" {str(row['Catatan']).strip()}."
    else:
        tambahan = ""

    # Daftar fasilitas yang ada (nilai 1)
    fas_ada = [k for k in KOLOM_FASILITAS if row[k] == 1]
    fas_str = ", ".join(fas_ada[:5])  # tampilkan max 5 fasilitas di deskripsi
    if len(fas_ada) > 5:
        fas_str += f", dan {len(fas_ada)-5} fasilitas lainnya"

    jarak_m = int(row["Jarak (km)"] * 1000)
    harga   = f"Rp {int(row['Harga (Bulan)']):,}".replace(",", ".")

    return (
        f"Kos {row['Jenis'].lower()} di daerah {row['Daerah']}, berjarak "
        f"{jarak_m} meter dari Kampus UNESA Ketintang. "
        f"Tersedia dengan harga {harga}/bulan dan dilengkapi fasilitas: {fas_str}. "
        f"Ukuran kamar {row['UK 1']:.1f}×{row['UK 2']:.1f} m "
        f"({row['Ukuran Kamar (M2)']:.1f} m²).{tambahan}"
    )

def _format_ke_list_dict(
    df          : pd.DataFrame,
    budget      : int,
    jarak_max_km: float,
    fac_cols    : list[str],
    ukuran_min  : float,
    jenis       : str,
    top_n       : int = 10,
) -> list[dict]:

    hasil = []

    for i, (_, row) in enumerate(df.head(top_n).iterrows()):

        # Foto: pilih dari pool secara round-robin berdasarkan posisi ke-i
        foto_url = FOTO_POOL[i % len(FOTO_POOL)]
        # Buat daftar 3 foto untuk galeri detail (variasi dari pool)
        foto_list = [
            FOTO_POOL[(i    ) % len(FOTO_POOL)],
            FOTO_POOL[(i + 1) % len(FOTO_POOL)],
            FOTO_POOL[(i + 2) % len(FOTO_POOL)],
        ]

        # Format nomor WhatsApp
        no_wa = row["Kontak (WA)"]   # sudah dikonversi ke string "62xxx" saat load

        # Buat daftar nama fasilitas yang tersedia (nilai 1) untuk UI
        # Konversi nama kolom CSV → nama tampilan yang lebih ramah pengguna
        csv_ke_ui = {v: k for k, v in FASILITAS_UI_KE_CSV.items() if v is not None}
        fasilitas_tampil = [
            csv_ke_ui.get(k, k)   # gunakan nama UI jika ada, else nama kolom CSV
            for k in KOLOM_FASILITAS
            if row[k] == 1
        ]

        # Hitung persentase kesesuaian untuk kos ini
        kesesuaian = _hitung_kesesuaian(
            row, budget, jarak_max_km, fac_cols, ukuran_min, jenis
        )

        # Susun dict sesuai format yang diharapkan UI 
        kos_dict = {
            # Identitas
            "id"            : int(row["No"]),
            "nama"          : str(row["Nama Kos"]),
            "alamat"        : str(row["Alamat"]),
            "daerah"        : str(row["Daerah"]),

            # Atribut Utama
            "harga"         : int(row["Harga (Bulan)"]),
            "jarak_km"      : float(row["Jarak (km)"]),
            "jenis"         : str(row["Jenis"]),
            "ukuran"        : f"{row['UK 1']:.1f}×{row['UK 2']:.1f} m",

            # Hasil K-Means 
            "cluster"       : str(row["cluster"]),
            "cluster_badge" : str(row["cluster_badge"]),

            # Hasil MOORA 
            "skor_moora"    : round(float(row["skor_moora"]), 3),
            "kesesuaian_pct": kesesuaian,

            # Fasilitas 
            "fasilitas"     : fasilitas_tampil,

            # Teks & Media 
            "deskripsi"     : _buat_deskripsi(row),
            "no_wa"         : no_wa,
            "foto_thumb"    : foto_url,
            "foto_list"     : foto_list,
            "foto_tersedia" : str(row.get("Foto Kos", "T")).strip().upper(),

            # Info Tambahan (untuk halaman detail) 
            "pemilik"       : f"Pemilik {row['Nama Kos']}",
            "sumber_data"   : str(row["Sumber Data"]),
            "total_fasilitas": int(row["Total Fasilitas"]),
        }

        hasil.append(kos_dict)

    return hasil


# ─────────────────────────────────────────────────────────────────────────────
#  FUNGSI PUBLIK UTAMA — dipanggil dari pages/search.py
# ─────────────────────────────────────────────────────────────────────────────

def cari_rekomendasi(
    budget          : int,
    jarak_meter     : int,
    fasilitas_dipilih: list[str],
    ukuran_str      : str,
    jenis           : str,
    top_n           : int = 10,
) -> tuple[list[dict], str]:

    # Load & pra-pemrosesan dataset 
    df = _load_dataset()

    # Konversi satuan dari UI ke satuan CSV 
    # Form slider menggunakan METER, CSV menggunakan KM
    jarak_max_km = jarak_meter / 1000.0

    # Ambil luas minimum (m²) dari pilihan dropdown ukuran
    ukuran_min = UKURAN_UI_KE_M2.get(ukuran_str, 0.0)

    # Terjemahkan nama fasilitas UI → nama kolom CSV
    # Hanya ambil fasilitas yang memiliki kolom padanan di CSV (value tidak None)
    fac_cols = [
        FASILITAS_UI_KE_CSV[f]
        for f in fasilitas_dipilih
        if f in FASILITAS_UI_KE_CSV and FASILITAS_UI_KE_CSV[f] is not None
    ]

    # 1. Filtering 
    df_hasil = _strict_filter(df, budget, jarak_max_km, fac_cols, ukuran_min, jenis)
    mode_filter = "strict"

    if df_hasil.empty:
        # Strict Filtering tidak menghasilkan kos apapun → aktifkan Relaxed
        df_hasil    = _relaxed_filter(df, budget, jarak_max_km, fac_cols, ukuran_min, jenis)
        mode_filter = "relaxed"

    # Jika relaxed pun kosong → kembalikan list kosong
    if df_hasil.empty:
        return [], mode_filter

    # 2. K-Means Clustering 
    # K-Means membutuhkan minimal 3 baris (karena k=3)
    # Jika data kurang dari 3, jalankan dengan k yang disesuaikan
    if len(df_hasil) < 3:
        # Beri label manual berdasarkan harga jika data terlalu sedikit
        df_hasil = df_hasil.copy()
        df_hasil["cluster"]       = "Standar"
        df_hasil["cluster_badge"] = "badge-standar"
    else:
        df_hasil = _kmeans_clustering(df_hasil)

    # 3. MOORA Ranking 
    df_hasil = _moora_ranking(df_hasil, jenis)

    # 4. Format ke list[dict] 
    hasil_list = _format_ke_list_dict(
        df_hasil, budget, jarak_max_km, fac_cols, ukuran_min, jenis, top_n
    )

    return hasil_list, mode_filter


def format_harga(harga: int) -> str:
    """Format angka harga menjadi string Rupiah yang rapi."""
    return f"Rp {harga:,.0f}".replace(",", ".")


def format_jarak(jarak_km: float) -> str:
    """Format jarak dalam meter atau km."""
    if jarak_km < 1:
        return f"{int(jarak_km * 1000)} m dari kampus"
    return f"{jarak_km:.1f} km dari kampus"
