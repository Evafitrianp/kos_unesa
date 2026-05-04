# 🏠 KosKu UNESA — Sistem Rekomendasi Kos
**Tugas Akhir · K-Means Clustering + MOORA · Universitas Negeri Surabaya**

---

## 📁 Struktur Proyek

```
kos_unesa_app/
├── app.py                  ← Entry point utama (jalankan ini)
├── utils/
│   ├── __init__.py
│   ├── styles.py           ← Semua CSS custom (design tokens, komponen, halaman)
│   └── dummy_data.py       ← Data dummy 3 kos (ganti dengan data asli + hasil algoritma)
├── pages/
│   ├── __init__.py
│   ├── home.py             ← Halaman Beranda (hero, fitur, cara kerja)
│   ├── search.py           ← Halaman Cari Kos (form 5 kriteria + loading state)
│   ├── results.py          ← Halaman Hasil Rekomendasi (card grid + skor)
│   └── detail.py           ← Halaman Detail Kos (galeri + fasilitas + WA button)
└── README.md
```

---

## 🚀 Cara Menjalankan

### 1. Install dependencies
```bash
pip install streamlit
```

### 2. Jalankan aplikasi
```bash
cd kos_unesa_app
streamlit run app.py
```

Buka browser di `http://localhost:8501`

---


## 🎨 Kustomisasi Tampilan

Semua warna dan desain ada di `utils/styles.py` pada bagian CSS Variables:
```css
:root {
    --primary:      #059669;   /* Warna hijau utama */
    --accent:       #F59E0B;   /* Warna aksen amber */
    --bg:           #F0FDF4;   /* Background halaman */
    /* ... lihat file lengkap */
}
```

---

## 📌 Catatan Penting untuk Sidang

| Komponen | Lokasi | Keterangan |
|---|---|---|
| Navbar + Routing | `app.py` | Session state-based navigation |
| Global CSS | `utils/styles.py` | Semua style, tidak ada duplikasi |
| Form Input | `pages/search.py` | 5 kriteria + loading state mockup |
| Card Hasil | `pages/results.py` | Score bars + badge cluster |
| Detail + WA | `pages/detail.py` | Link WA otomatis dengan pesan template |
| **TODO Algoritma** | `pages/search.py` | Tandai dengan komentar `# TODO` |
