"""
pages/search.py
───────────────
Halaman Cari Kos — Formulir 5 Kriteria.
Logika algoritma K-Means & MOORA akan diintegrasikan pada bagian
yang ditandai dengan komentar # TODO.
"""

import time
import streamlit as st
from utils.algoritma import cari_rekomendasi


def render():

    # ── SECTION HEADER ─────────────────────────────────────────────
    st.markdown("""
    <span class="section-label">Pencarian Kos</span>
    <h2 class="section-title">Masukkan Kriteria Anda</h2>
    <p class="section-subtitle">
        Isi semua kriteria di bawah ini. Sistem kami akan mencarikan
        kos yang paling sesuai dengan kebutuhan Anda.
    </p>
    <div style="height:1.75rem"></div>
    """, unsafe_allow_html=True)

    # ── FORM CARD ──────────────────────────────────────────────────
    with st.container():

        # ── ROW 1: Budget & Jarak ──────────────────────────────────
        col_budget, col_jarak = st.columns(2, gap="large")

        with col_budget:
            st.markdown("""
            <h3 style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:700;
                    color:var(--text-primary);margin-bottom:1.25rem;
                    padding-bottom:.75rem;border-bottom:1px solid var(--border)">
                <img src="https://cdn-icons-png.flaticon.com/512/631/631180.png"
                    width="22" style="border-radius:50%;background:#E5E7EB;padding:3px">
                Budget per Bulan</h3>
            """, unsafe_allow_html=True)
            
            budget = st.slider(
                "Budget / Harga Maksimal per Bulan",
                min_value=400_000,
                max_value=2_300_000,
                value=1_000_000,
                step=50_000,
                format="Rp %d",
                help="Geser untuk mengatur batas harga maksimal kos per bulan.",
                key="sl_budget",
            )
            # Tampilkan nilai yang dipilih secara eksplisit
            st.markdown(
                f'<div style="font-size:.82rem;color:var(--text-secondary);margin-top:-.25rem">'
                f'Maksimal: <strong style="color:var(--primary-dark)">Rp {budget:,.0f}</strong>'
                f"</div>".replace(",", "."),
                unsafe_allow_html=True,
            )

        with col_jarak:
            st.markdown("""
            <h3 style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:700;
                    color:var(--text-primary);margin-bottom:1.25rem;
                    padding-bottom:.75rem;border-bottom:1px solid var(--border)">
                <img src="https://cdn-icons-png.flaticon.com/512/484/484141.png" 
                    width="22" style="border-radius:50%;background:#E5E7EB;padding:3px">
                Jarak Maksimal ke Kampus</h3>
            """, unsafe_allow_html=True)
            jarak = st.slider(
                "Jarak Maksimal ke Kampus (meter)",
                min_value=100,
                max_value=3000,
                value=800,
                step=50,
                format="%d m",
                help="Jarak kos dari Kampus UNESA Ketintang.",
                key="sl_jarak",
            )
            st.markdown(
                f'<div style="font-size:.82rem;color:var(--text-secondary);margin-top:-.25rem">'
                f'Maksimal: <strong style="color:var(--primary-dark)">{jarak} meter</strong>'
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

        # ── ROW 2: Fasilitas ───────────────────────────────────────
        st.markdown("""
        <div class="divider"></div>
        <h3 style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:700;
                   color:var(--text-primary);margin:1.25rem 0">
            <img src="https://cdn-icons-png.flaticon.com/512/4350/4350275.png"
                 width="22" style="border-radius:50%;background:#E5E7EB;padding:3px">
            Fasilitas yang Diinginkan
        </h3>
        <p style="font-size:.875rem;color:var(--text-secondary);margin-bottom:1rem">
            Pilih fasilitas yang Anda butuhkan (bisa lebih dari satu)
        </p>
        """, unsafe_allow_html=True)

        # ── Initialize state untuk fasilitas ───────────────────────
        if "fas_dipilih" not in st.session_state:
            st.session_state.fas_dipilih = ["WiFi"]

        FASILITAS_OPTIONS = [
            "WiFi",
            "AC",
            "Kamar Mandi Dalam",
            "Lemari",
            "Meja Belajar",
            "Kursi",
            "Kasur",
            "Dapur Bersama",
            "Parkiran Motor",
            "Satpam",
            "Air PDAM",
            "TV",
            "Listrik",
        ]

        # ── Grid toggle button 4 kolom ─────────────────────────────
        cols = st.columns(4, gap="small")
        for idx, fas in enumerate(FASILITAS_OPTIONS):
            col_idx = idx % 4
            with cols[col_idx]:
                is_active = fas in st.session_state.fas_dipilih
                # Styling untuk active/inactive button
                btn_style = """
                style="
                    width: 100%;
                    padding: 0.75rem 0.5rem;
                    border-radius: 0.5rem;
                    font-size: 0.875rem;
                    font-weight: 600;
                    cursor: pointer;
                    border: 2px solid;
                    transition: all 0.2s ease;
                    text-align: center;
                    font-family: 'Sora', sans-serif;
                """ if is_active else """
                style="
                    width: 100%;
                    padding: 0.75rem 0.5rem;
                    border-radius: 0.5rem;
                    font-size: 0.875rem;
                    font-weight: 600;
                    cursor: pointer;
                    border: 2px solid;
                    transition: all 0.2s ease;
                    text-align: center;
                    font-family: 'Sora', sans-serif;
                """
                
                if st.button(
                    f"{'✓ ' if is_active else ''}{fas}",
                    key=f"btn_fas_{fas}",
                    use_container_width=True,
                ):
                    if fas in st.session_state.fas_dipilih:
                        st.session_state.fas_dipilih.remove(fas)
                    else:
                        st.session_state.fas_dipilih.append(fas)
                    st.rerun()

        # ── Info fasilitas yang dipilih ────────────────────────────
        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        if st.session_state.fas_dipilih:
            count = len(st.session_state.fas_dipilih)
            st.markdown(
                f'<div style="font-size:.82rem;color:var(--text-secondary)">'
                f'<strong>{count}</strong> fasilitas dipilih</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="font-size:.82rem;color:#F59E0B">'
                "Pilih minimal 1 fasilitas untuk pencarian optimal</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

        # ── ROW 3: Ukuran & Jenis ──────────────────────────────────
        col_ukuran, col_jenis = st.columns([1, 1], gap="large")

        with col_ukuran:
            st.markdown("""
            <h3 style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:700;
                    color:var(--text-primary);margin-bottom:1.25rem;
                    padding-bottom:.75rem;border-bottom:1px solid var(--border)">
                <img src="https://cdn-icons-png.flaticon.com/512/8112/8112972.png" 
                    width="22" style="border-radius:50%;background:#E5E7EB;padding:3px">
                Ukuran Kamar Minimum</h3>
            """, unsafe_allow_html=True)
            
            ukuran = st.radio(
                "Ukuran Kamar Minimum",
                options=[
                    "Semua Ukuran",
                    "3x3 m (Standar Kecil)",
                    "3x4 m (Standar)",
                    "4x4 m (Luas)",
                    "4x5 m (Sangat Luas)",
                ],
                index=2,
                horizontal=True,
                help="Pilih ukuran minimum kamar yang Anda inginkan.",
                key="sb_ukuran",
            )
          
        with col_jenis:    
            st.markdown("""
            <h3 style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:700;
                    color:var(--text-primary);margin-bottom:1.25rem;
                    padding-bottom:.75rem;border-bottom:1px solid var(--border)">
                <img src="https://cdn-icons-png.flaticon.com/512/33/33308.png"
                    width="22" style="border-radius:50%;background:#E5E7EB;padding:3px">
                Tipe Kamar
            </h3>
            """, unsafe_allow_html=True)

            jenis = st.radio(
                "Jenis Kos",
                options=["Putra", "Putri", "Campur", "Semua"],
                index=3,
                horizontal=True,
                help="Putra = Khusus laki-laki, Putri = Khusus perempuan, Campur = Campur, Semua = Tidak ada batasan.",
                key="rb_jenis",
            )

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

        # ── RINGKASAN INPUT ────────────────────────────────────────
        st.markdown("""
        <div class="divider"></div>
        <h3 style="font-family:'Sora',sans-serif;font-size:1rem;font-weight:700;
                   color:var(--text-primary);margin:1.25rem 0 .75rem">
            Ringkasan Pencarian
        </h3>
        """, unsafe_allow_html=True)

        fas_str = ", ".join(st.session_state.fas_dipilih) if st.session_state.fas_dipilih else "—"
        st.markdown(
            f"""
            <div style="background:var(--bg);border-radius:var(--radius-sm);
                        padding:1rem 1.25rem;font-size:.875rem;line-height:2">
                <img src="https://cdn-icons-png.flaticon.com/512/631/631180.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> <b>Budget:</b> Rp {budget:,.0f}/bln &nbsp;|&nbsp;
                <img src="https://cdn-icons-png.flaticon.com/512/484/484141.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> <b>Jarak:</b> ≤ {jarak} m &nbsp;|&nbsp;
                <img src="https://cdn-icons-png.flaticon.com/512/8112/8112972.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> <b>Ukuran:</b> {ukuran} &nbsp;|&nbsp;
                <img src="https://cdn-icons-png.flaticon.com/512/33/33308.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> <b>Jenis:</b> {jenis} &nbsp;|&nbsp;
                <img src="https://cdn-icons-png.flaticon.com/512/4350/4350275.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> <b>Fasilitas:</b> {fas_str}
            </div>
            """.replace(",", "."),
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)  # close card

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── SEARCH BUTTON ──────────────────────────────────────────────
    col_l2, col_btn2, col_r2 = st.columns([2, 3, 2])
    with col_btn2:
        st.markdown('<div data-testid="stButton" class="btn-primary">', unsafe_allow_html=True)
        search_clicked = st.button(
            "Cari Kos Rekomendasi",
            key="btn_search",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ── LOADING STATE & PROSES ─────────────────────────────────────
    if search_clicked:
        with st.empty():
            # Tampilkan loading overlay
            st.markdown("""
            <div class="loading-overlay">
                <div class="spinner"></div>
                <div class="loading-text">Menganalisis Data Kos...</div>
                <div class="loading-sub">
                    K-Means sedang mengelompokkan kos &amp; MOORA sedang meranking hasil terbaik
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.3)

            st.markdown("""
            <div class="loading-overlay">
                <div class="spinner"></div>
                <div class="loading-text">Memproses Strict Filtering...</div>
                <div class="loading-sub">Mencari kecocokan 100% berdasarkan kriteria Anda</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.3)

            st.markdown("""
            <div class="loading-overlay">
                <div class="spinner"></div>
                <div class="loading-text">Menghitung Skor MOORA...</div>
                <div class="loading-sub">Meranking kos berdasarkan multi-criteria decision making</div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.3)

        # ══════════════════════════════════════════════════════════
        #  INTEGRASI ALGORITMA K-MEANS & MOORA
        #  Memanggil utils/algoritma.py yang berisi:
        #    Tahap 1 → Strict / Relaxed Filtering
        #    Tahap 2 → K-Means Clustering (scikit-learn, k=3)
        #    Tahap 3 → MOORA (Vector Normalization + Weighted Score)
        #    Tahap 4 → Format list[dict] siap render
        # ══════════════════════════════════════════════════════════
        try:
            # ── Panggil fungsi utama algoritma ───────────────────
            # Parameter dikirim persis dari nilai widget form di atas.
            # `cari_rekomendasi` mengembalikan tuple:
            #   hasil_kos  → list[dict], sudah diurutkan by skor MOORA
            #   mode_filter → 'strict' atau 'relaxed'
            hasil_kos, mode_filter = cari_rekomendasi(
                budget           = budget,                        # int  : Rp dari slider
                jarak_meter      = jarak,                          # int  : meter dari slider
                fasilitas_dipilih= st.session_state.fas_dipilih,   # list : dari grid toggle button
                ukuran_str       = ukuran,                         # str  : dari selectbox
                jenis            = jenis,                          # str  : dari radio button
                top_n            = 12,                             # int  : maks hasil ditampilkan
            )

            # ── Tangani kasus tidak ada hasil sama sekali ─────────
            # Terjadi jika bahkan Relaxed Filtering pun tidak menemukan
            # kos yang memenuhi syarat minimum toleransi.
            if not hasil_kos:
                st.error(
                    "**Tidak ada kos yang ditemukan** sesuai kriteria Anda, "
                    "bahkan setelah toleransi diperlebar.\n\n"
                    "**Saran:** Naikkan budget, perbesar jarak, atau kurangi "
                    "fasilitas yang diminta, lalu coba cari ulang."
                )
                # Hentikan eksekusi dan tetap di halaman form (tidak redirect)
                st.stop()

            # ── Simpan semua state ke session ─────────────────────
            # session_state berfungsi sebagai "memori antar halaman" di Streamlit.
            # Nilai-nilai ini akan dibaca oleh pages/results.py dan pages/detail.py.

            # Parameter pencarian — ditampilkan sebagai ringkasan di halaman hasil
            st.session_state.search_params = {
                "budget"   : budget,
                "jarak"    : jarak,
                "fasilitas": st.session_state.fas_dipilih,
                "ukuran"   : ukuran,
                "jenis"    : jenis,
            }

            # Daftar kos hasil algoritma (list[dict], urutan = ranking MOORA)
            st.session_state.search_results = hasil_kos

            # Mode filter — untuk ditampilkan sebagai keterangan di halaman hasil
            # ('strict' = semua kriteria 100% terpenuhi,
            #  'relaxed' = menggunakan toleransi budget/jarak/fasilitas)
            st.session_state.filter_mode = mode_filter

        except FileNotFoundError:
            # Terjadi jika file data_kos.csv tidak ditemukan di root proyek
            st.error(
                "**File dataset tidak ditemukan.**\n\n"
                "Pastikan file `data_kos.csv` berada di folder yang sama "
                "dengan `app.py` (root proyek), lalu jalankan ulang aplikasi."
            )
            st.stop()

        except Exception as e:
            # Tangkap semua error tak terduga lainnya (mis. kolom CSV berubah nama,
            # data corrupt, error scikit-learn, dsb.) dan tampilkan pesannya.
            st.error(
                f"**Terjadi kesalahan saat memproses data.**\n\n"
                f"Detail error (untuk debugging): `{type(e).__name__}: {e}`\n\n"
                f"Silakan periksa konsol terminal untuk traceback lengkapnya."
            )
            st.stop()
        # ══════════════════════════════════════════════════════════
        #  END ALGORITMA
        # ══════════════════════════════════════════════════════════

        # Navigasi ke halaman hasil
        st.session_state.current_page = "results"
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
