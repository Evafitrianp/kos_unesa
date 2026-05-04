"""
pages/about.py
──────────────
Halaman About — Informasi tentang platform KosKu UNESA.
"""

import streamlit as st


def render():
    # ── HEADER ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:2rem">
        <span class="section-label">Tentang Platform</span>
        <h1 class="section-title" style="margin-top:.5rem">
            Tentang KosKu <span style="color:var(--primary)">UNESA</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # ── KONTEN ABOUT ───────────────────────────────────────────────
    st.markdown("""
    <div style="background-color: var(--bg-card, #FFFFFF); padding: 1.8rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 2rem; border: 1px solid #E5E7EB;">
        <h1 style="font-family:'Sora',sans-serif;font-size:1.25rem;font-weight:700;
                   color:var(--text-primary);margin-bottom:1rem">
            Tentang Sistem Rekomendasi Kos UNESA
        </h1>
        <p style="font-size:.95rem;color:var(--text-secondary);line-height:1.8;margin-bottom:1.5rem">
            Sistem Rekomendasi Kos UNESA adalah platform berbasis web yang dirancang khusus untuk membantu mahasiswa 
            Universitas Negeri Surabaya (UNESA) kampus Ketintang menemukan tempat tinggal yang sesuai dengan kebutuhan 
            dan kemampuan finansial mereka. Platform ini menggunakan metode <strong>K-Means Clustering</strong> dan <strong>MOORA (Multi-Objective Optimization on the Basis of Ratio Analysis)</strong> 
            untuk memberikan rekomendasi kos yang akurat dan relevan berdasarkan kriteria yang diinputkan pengguna.</p></div>
    <div style="background-color: var(--bg-card, #FFFFFF); padding: 1.8rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 2rem; border: 1px solid #E5E7EB;">
        <h1 style="font-family:'Sora',sans-serif;font-size:1.25rem;font-weight:700;color:var(--text-primary);margin-bottom:1rem">
            Teknologi yang Digunakan</h1>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.25rem">K-Means Clustering</h4>
        <p style="color:var(--text-secondary);font-size:.9rem;line-height:1.7">
            Algoritma K-Means digunakan untuk mengelompokkan kos ke dalam 3 kategori utama:
            <strong>Ekonomis</strong> (budget hemat), <strong>Standar</strong> (balans harga-fasilitas), 
            dan <strong>Premium</strong> (fasilitas lengkap). Pengelompokan ini membantu dalam proses awal penyaringan.</p>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.25rem">MOORA (Multi-Objective Optimization on Basis of Ratio Analysis)</h4>
        <p style="color:var(--text-secondary);font-size:.9rem;line-height:1.7">
            MOORA adalah teknik multi-kriteria decision making yang mengevaluasi 5 parameter utama:
            harga, jarak, ukuran kamar, fasilitas, dan jenis kos. Algoritma ini menghasilkan skor komprehensif 
            yang digunakan untuk merangking kos dari yang paling sesuai hingga yang kurang sesuai.</p></div>
    <div style="background-color: var(--bg-card, #FFFFFF); padding: 1.8rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 2rem; border: 1px solid #E5E7EB;">
        <h1 style="font-family:'Sora',sans-serif;font-size:1.25rem;font-weight:700;
                   color:var(--text-primary);margin-bottom:1rem">
            Cara Kerja Platform</h1>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.25rem">1. Isi Kriteria</h4>
        <p style="color:var(--text-secondary);font-size:.9rem;line-height:1.7">
            Masukkan preferensi Anda: budget, jarak, fasilitas, ukuran kamar, dan jenis kos yang diinginkan.</p>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.25rem">2. Proses AI</h4>
        <p style="color:var(--text-secondary);font-size:.9rem;line-height:1.7">
            Platform akan menganalisis kriteria yang dimasukkan dan menggunakan algoritma K-Means serta MOORA untuk memberikan rekomendasi kos yang paling sesuai.</p>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.25rem">3. Dapatkan Rekomendasi</h4>
        <p style="color:var(--text-secondary);font-size:.9rem;line-height:1.7">
            Lihat daftar kos terbaik yang paling sesuai dengan kriteria Anda, diranking berdasarkan skor MOORA.</p>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.25rem">4. Hubungi Pemilik</h4>
        <p style="color:var(--text-secondary);font-size:.9rem;line-height:1.7">
            Kontak pemilik kos langsung melalui WhatsApp untuk survei dan booking hunian.</p>
    </div>
    """, unsafe_allow_html=True)
