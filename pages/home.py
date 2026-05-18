import streamlit as st
from utils.logo import LOGO_B64


def render():
    # ── HERO SECTION ──────────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">Khusus Mahasiswa UNESA Ketintang</div>
        <h1 class="hero-title">
            Temukan kos yang cocok dengan kebutuhanmu</h1>
        <p class="hero-subtitle" style="text-align:center; color: #9CA3AF; font-size: 1.1rem; max-width: 600px; margin: 0 auto 2rem auto; line-height: 1.6;">
            Platform rekomendasi kos berbasis <strong>AI — K-Means &amp; MOORA</strong>
            yang membantu mahasiswa UNESA menemukan hunian terbaik sesuai
            budget, jarak, dan fasilitas yang diinginkan.
        </p>
        <div class="stat-row">
            <div class="stat-pill">
                <div class="stat-pill-num">100+</div>
                <div class="stat-pill-label">Data Kos</div>
            </div>
            <div class="stat-pill">
                <div class="stat-pill-num">3</div>
                <div class="stat-pill-label">Kategori Cluster</div>
            </div>
            <div class="stat-pill">
                <div class="stat-pill-num">≤3km</div>
                <div class="stat-pill-label">Radius Kampus</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Spacer setelah hero
    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # ── CTA BUTTON ─────────────────────────────────────────────────
    col_l, col_btn, col_r = st.columns([3, 2, 3])
    with col_btn:
        st.markdown('<div data-testid="stButton" class="btn-primary">', unsafe_allow_html=True)
        if st.button("Mulai Cari Kos", key="hero_cta", use_container_width=True):
            st.session_state.current_page = "search"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

    # ── FITUR UNGGULAN ─────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;margin-bottom:2rem">
        <span class="section-label">Keunggulan Platform</span>
        <h2 class="section-title">Mengapa Memilih KosKu UNESA?</h2>
        <p class="section-subtitle" style="margin:0 auto">
            Kami menggunakan algoritma machine learning untuk memberikan
            rekomendasi yang objektif dan personal.
        </p>
    </div>
    """, unsafe_allow_html=True)

    feat_col1, feat_col2, feat_col3 = st.columns(3, gap="large")

    with feat_col1:
        st.markdown("""
        <div class="feature-card">
            <div style="margin-bottom: 1rem;">
                <img src="https://cdn-icons-png.flaticon.com/512/1693/1693746.png" width="45" height="45" style="object-fit: contain; border-radius: 50%; border: 2px solid #111827; padding: 8px;">
            </div>
            <div class="feature-title">Rekomendasi Berbasis AI</div>
            <p class="feature-desc">
                Algoritma <strong>K-Means Clustering</strong> mengelompokkan kos
                berdasarkan karakteristik, lalu <strong>MOORA</strong> meranking
                hasil terbaik secara objektif — bukan sekadar iklan berbayar.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with feat_col2:
        st.markdown("""
        <div class="feature-card">
            <div style="margin-bottom: 1rem;">
                <img src="https://cdn-icons-png.flaticon.com/512/54/54481.png" width="45" height="45" style="object-fit: contain; border-radius: 50%; border: 2px solid #111827; padding: 8px;">
            </div>
            <div class="feature-title">Filter Presisi 5 Kriteria</div>
            <p class="feature-desc">
                Masukkan <strong>budget, jarak, fasilitas, ukuran kamar,</strong>
                dan <strong>jenis kos</strong> yang Anda inginkan. Sistem kami akan
                mencarikan yang paling sesuai — bahkan dengan toleransi cerdas
                jika hasil ketat tidak tersedia.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with feat_col3:
        st.markdown("""
        <div class="feature-card">
            <div style="margin-bottom: 1rem;">
                <img src="https://cdn-icons-png.flaticon.com/512/455/455705.png" width="45" height="45" style="object-fit: contain; border-radius: 50%; border: 2px solid #111827; padding: 8px;">
            </div>
            <div class="feature-title">Kontak Langsung via WhatsApp</div>
            <p class="feature-desc">
                Tidak ada perantara. Setelah menemukan kos impian, Anda langsung
                terhubung dengan pemilik kos via <strong>WhatsApp</strong> untuk
                survei dan negosiasi. Cepat, mudah, transparan.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:3.5rem'></div>", unsafe_allow_html=True)

    # ── CARA KERJA ─────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;margin-bottom:2rem">
        <span class="section-label">Alur Sistem</span>
        <h2 class="section-title">Bagaimana Cara Kerjanya?</h2>
    </div>
    """, unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4, gap="medium")

    steps = [
        ("01", "https://cdn-icons-png.flaticon.com/512/1055/1055685.png", "Isi Kriteria", "Masukkan budget, jarak, fasilitas, dan preferensi kos Anda."),
        ("02", "https://cdn-icons-png.flaticon.com/512/1693/1693746.png", "Proses AI", "Sistem menjalankan K-Means & MOORA untuk meranking kos terbaik."),
        ("03", "https://cdn-icons-png.flaticon.com/512/1150/1150599.png", "Lihat Hasil", "Tampilkan 5–10 kos terbaik beserta skor kesesuaian dan label cluster."),
        ("04", "https://cdn-icons-png.flaticon.com/512/455/455705.png", "Hubungi Pemilik", "Klik tombol WhatsApp dan langsung survei atau booking kos pilihan."),
    ]

    for col, (num, icon_url, title, desc) in zip([s1, s2, s3, s4], steps):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center">
                <div style="font-family:'Sora',sans-serif;font-size:.7rem;font-weight:700;
                            color:var(--text-muted);letter-spacing:.1em;margin-bottom:.5rem">
                    LANGKAH {num}
                </div>
                <div style="margin-bottom: 1rem;">
                    <img src="{icon_url}" width="45" height="45" style="object-fit: contain; border-radius: 50%; border: 2px solid #111827; padding: 8px;"></div>
                <div class="feature-title">{title}</div>
                <p class="feature-desc">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

    # ── FOOTER INFO ────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center;padding:2rem 0 1rem;border-top:1px solid var(--border)">
        <p style="color:var(--text-muted);font-size:.8rem;margin:0">
            <img src="{LOGO_B64}" width="20"
                 style="vertical-align:middle;margin-right:6px;margin-bottom:3px">
            <strong>KosKu UNESA</strong> — Sistem Rekomendasi Kos Berbasis K-Means &amp; MOORA<br>
            Dikembangkan sebagai Tugas Akhir · Universitas Negeri Surabaya
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close content-container
