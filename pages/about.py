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
        <h1 style="font-family:'Sora',sans-serif;font-size:1.5rem;font-weight:700;
                   color:var(--text-primary);margin-bottom:1rem">
            Tentang Sistem Rekomendasi Kos UNESA
        </h1>
        <p style="font-size:1rem;color:var(--text-secondary);line-height:1.8;margin-bottom:1.5rem">
            Sistem Rekomendasi Kos UNESA adalah platform berbasis web yang dirancang khusus untuk membantu mahasiswa 
            Universitas Negeri Surabaya (UNESA) kampus Ketintang dalam menemukan tempat tinggal yang sesuai dengan kebutuhan 
            dan kemampuan finansial mereka. Platform ini memanfaatkan metode <strong>K-Means Clustering</strong> dan <strong>MOORA (Multi-Objective Optimization on the Basis of Ratio Analysis)</strong> 
            untuk memberikan rekomendasi kos yang akurat dan relevan berdasarkan preferensi pengguna.</p></div>
    <div style="background-color: var(--bg-card, #FFFFFF); padding: 1.8rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 2rem; border: 1px solid #E5E7EB;">
        <h1 style="font-family:'Sora',sans-serif;font-size:1.5rem;font-weight:700;color:var(--text-primary);margin-bottom:1rem">
            Teknologi yang Digunakan</h1>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.2rem">K-Means Clustering</h4>
        <p style="color:var(--text-secondary);font-size:1rem;line-height:1.7">
            Algoritma K-Means digunakan untuk mengelompokkan kos ke dalam 3 kategori utama:
            <strong>Ekonomis</strong>, <strong>Standar</strong>, dan <strong>Premium</strong>. 
            Pengelompokan ini membantu dalam proses awal penyaringan data sehingga lebih terstruktur.</p>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.2rem">MOORA (Multi-Objective Optimization on Basis of Ratio Analysis)</h4>
        <p style="color:var(--text-secondary);font-size:1rem;line-height:1.7">
            Metode MOORA digunakan untuk melakukan perhitungan multi-kriteria berdasarkan beberapa aspek seperti harga, jarak, 
            ukuran kamar, fasilitas, dan jenis kos. Hasil perhitungan ini menghasilkan skor yang digunakan untuk memberikan peringkat kos 
            dari yang paling sesuai hingga yang kurang sesuai.</p></div>
    <div style="background-color: var(--bg-card, #FFFFFF); padding: 1.8rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 2rem; border: 1px solid #E5E7EB;">
        <h1 style="font-family:'Sora',sans-serif;font-size:1.5rem;font-weight:700;
                   color:var(--text-primary);margin-bottom:1rem">
            Cara Kerja Platform</h1>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.2rem">1. Isi Kriteria</h4>
        <p style="color:var(--text-secondary);font-size:1rem;line-height:1.7">
            Masukkan preferensi Anda seperti budget, jarak, fasilitas, ukuran kamar, dan jenis kos yang diinginkan.</p>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.2rem">2. Analisis Otomatis</h4>
        <p style="color:var(--text-secondary);font-size:1rem;line-height:1.7">
            Sistem akan memproses dan menganalisis kriteria yang dimasukkan 
            untuk mengelompokkan serta menentukan tingkat kecocokan setiap kos.</p>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.2rem">3. Dapatkan Rekomendasi</h4>
        <p style="color:var(--text-secondary);font-size:1rem;line-height:1.7">
            Platform menampilkan daftar kos yang paling sesuai dengan preferensi Anda, diurutkan berdasarkan hasil perhitungan tingkat kecocokan.</p>
        <h4 style="color:var(--text-primary);font-weight:700;margin-bottom:.2rem">4. Hubungi Pemilik</h4>
        <p style="color:var(--text-secondary);font-size:1rem;line-height:1.7">
            Anda dapat langsung menghubungi pemilik kos melalui WhatsApp untuk mendapatkan informasi lebih lanjut atau melakukan booking.</p>
    </div>
    """, unsafe_allow_html=True)
