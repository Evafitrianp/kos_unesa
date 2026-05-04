"""
pages/results.py
────────────────────────────────────────────────────────────────
Halaman Hasil Rekomendasi — K-Means + MOORA.

FIX utama bug HTML mentah:
  Gunakan st.container(border=True) + st.image() + st.progress()
  sebagai struktur card. st.markdown() HANYA untuk snippet HTML
  kecil dengan inline-style, BUKAN satu blok besar.
"""

import os
import base64
import streamlit as st
import io
from PIL import Image
from utils.dummy_data import format_harga, format_jarak


# ─────────────────────────────────────────────────────────────
#  HELPER: foto dari folder lokal atau placeholder abu-abu
# ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _foto_src(kos: dict) -> str | None:
    # Mencari path gambar lokal berdasarkan kolom 'No'. Jika 'Foto Kos' = 'T' atau file tidak ditemukan, akan mereturn None.
    # Cek nilai kolom 'Foto Kos' dari CSV
    if str(kos.get("foto_tersedia", "T")).strip().upper() != "Y":
        return None
    # Mencari foto di folder 'foto/' dengan format [No].jpg atau png
    for ext in ("jpg", "jpeg", "png"):
        path = os.path.join(BASE_DIR, "foto", f"{kos['id']}.{ext}")
        if os.path.isfile(path):
            return path
    return None  # file tidak ada → fallback placeholder

def crop_image(path, size=(400, 220)):
    """Crop & resize foto ke ukuran seragam — dipakai untuk card hasil."""
    img = Image.open(path)
    target_w, target_h = size
    target_ratio = target_w / target_h
    w, h = img.size
    current_ratio = w / h
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
    return img.resize(size)

def _tampil_foto(kos: dict, height: int = 190):
    path = _foto_src(kos)
        
    if path:
        # Jika gambar ditemukan, tampilkan secara langsung menggunakan Streamlit
        img = crop_image(path, size=(400, 220))
        st.image(img, use_container_width=True)
    else:
        # Jika tidak ditemukan, buat kotak abu-abu bertuliskan No Image Available
        st.markdown(
            f"<div style='background:#E5E7EB;height:{height}px;border-radius:8px 8px 0 0;"
            f"display:flex;flex-direction:column;align-items:center;"
            f"justify-content:center;color:#9CA3AF;font-size:.85rem;gap:.4rem'>"
            f"<span style='font-size:2rem'>📷</span>"
            f"<span>No Image Available</span></div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────
#  RENDER SATU CARD KOS
# ─────────────────────────────────────────────────────────────

def _render_kos_card(kos: dict, rank: int):
    """
    Render card kos menggunakan st.container(border=True).
    Setiap elemen di-render terpisah — TIDAK ada satu blok HTML besar.
    Ini menghindari bug Streamlit yang menampilkan HTML sebagai teks mentah.
    """
    # ── Pre-compute semua nilai ────────────────────────────────
    cluster     = kos.get("cluster", "Standar")
    badge_cls   = kos.get("cluster_badge", "badge-standar")
    harga_str   = format_harga(kos["harga"])
    jarak_str   = format_jarak(kos["jarak_km"])
    moora_val   = kos.get("skor_moora", 0.0)
    kesesuaian  = kos.get("kesesuaian_pct", 0)
    nama        = kos.get("nama", "—")
    alamat      = kos.get("alamat", "—")
    jenis       = kos.get("jenis", "—")
    ukuran      = kos.get("ukuran", "—")
    daerah      = kos.get("daerah", "")

    cluster_icon = {"Ekonomis": "🌿", "Standar": "⭐"}.get(cluster, "💎")

    badge_bg    = {"Ekonomis": "#D1FAE5", "Standar": "#FEF3C7"}.get(cluster, "#DBEAFE")
    badge_color = {"Ekonomis": "#065F46", "Standar": "#92400E"}.get(cluster, "#1E3A5F")
    jenis_color = {"Putra": "#3B82F6", "Putri": "#EC4899"}.get(jenis, "#6B7280")
    rank_bg     = {1: "#059669", 2: "#0284C7", 3: "#F59E0B"}.get(rank, "#6B7280")

    fasilitas_list = kos.get("fasilitas", [])
    fas_tampil  = fasilitas_list[:4]
    fas_sisa    = len(fasilitas_list) - 4 if len(fasilitas_list) > 4 else 0

    # ── Container card (border bawaan Streamlit) ──────────────
    with st.container(border=True):

        # 1. FOTO dengan overlay rank & jenis menggunakan kolom trick
        col_foto_main, _ = st.columns([1, 0.001])
        with col_foto_main:
            _tampil_foto(kos, height=190)

        # Rank badge + jenis badge (baris terpisah, teks kecil)
        st.markdown(
            f"""
            <div style="display:flex;justify-content:space-between;
                        align-items:center;margin:4px 0 6px">
                <span style="
                    background:{rank_bg};color:#fff;
                    font-size:.75rem;font-weight:800;
                    padding:.2rem .65rem;border-radius:99px;
                    font-family:'Sora',sans-serif">
                    # {rank}
                </span>
                <span style="background:#F0FDF4;color:#fff;
                    font-size:.72rem;font-weight:600;
                    padding:.2rem .6rem;border-radius:99px;
                    font-family:'Sora',sans-serif">
                    {daerah}
                </span>
                <span style="
                    background:{jenis_color};color:#fff;
                    font-size:.72rem;font-weight:600;
                    padding:.2rem .6rem;border-radius:99px">
                    {jenis}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 2. CLUSTER BADGE
        st.markdown(
            f"""
            <span style="
                background:{badge_bg};color:{badge_color};
                font-size:.72rem;font-weight:700;
                padding:.22rem .8rem;border-radius:99px;
                letter-spacing:.03em;text-transform:uppercase;
                display:inline-block;margin-bottom:6px">
                {cluster_icon} {cluster}
            </span>
            """,
            unsafe_allow_html=True,
        )

        # 3. NAMA & ALAMAT
        st.markdown(
            f"""
            <div style="font-family:'Sora',sans-serif;font-size:.95rem;
                        font-weight:700;color:#111827;margin-bottom:2px">
                {nama}
            </div>
            <div style="font-size:.78rem;color:#9CA3AF;margin-bottom:8px">
                <img src="https://cdn-icons-png.flaticon.com/512/535/535188.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px">
                 {alamat}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 4. HARGA & JARAK & UKURAN
        st.markdown(
            f"""
            <div style="font-size:.85rem;color:#4B5563;line-height:1.9">
                <img src="https://cdn-icons-png.flaticon.com/512/631/631180.png"
                    width="22" style="border-radius:50%;background:#E5E7EB;padding:3px">
                    <span style="font-family:'Sora',sans-serif;font-weight:700;
                                color:#047857"> {harga_str}</span>
                   <span style="color:#9CA3AF;font-size:.75rem">/bln</span><br>
                <img src="https://cdn-icons-png.flaticon.com/512/484/484141.png" 
                    width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> {jarak_str}<br>
                <img src="https://cdn-icons-png.flaticon.com/512/8112/8112972.png" 
                    width="22" style="border-radius:50%;background:#E5E7EB;padding:3px">{ukuran}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr style='margin:8px 0;border-color:#E5E7EB'>",
                    unsafe_allow_html=True)

        # 5. SKOR MOORA (gunakan st.progress — 100% native, pasti render)
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;"
            f"font-size:.78rem;color:#4B5563;margin-bottom:3px'>"
            f"<span><img src='https://cdn-icons-png.flaticon.com/512/3558/3558884.png' width='16' style='vertical-align:middle;margin-right:4px'>Skor MOORA</span>"
            f"<strong>{moora_val:.3f}</strong></div>",
            unsafe_allow_html=True,
        )
        st.progress(float(moora_val))

        # 6. KESESUAIAN KRITERIA
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;"
            f"font-size:.78rem;color:#4B5563;margin:6px 0 3px'>"
            f"<span><img src='https://cdn-icons-png.flaticon.com/512/845/845646.png' width='16' style='vertical-align:middle;margin-right:4px'>Kesesuaian</span>"
            f"<strong>{kesesuaian}%</strong></div>",
            unsafe_allow_html=True,
        )
        st.progress(kesesuaian / 100)

        # 7. FASILITAS TAG (max 4 + sisa)
        if fas_tampil:
            fas_spans = "".join(
                f'<span style="background:#F0FDF4;color:#047857;'
                f'border:1px solid #BBF7D0;padding:.15rem .5rem;'
                f'border-radius:99px;font-size:.7rem;white-space:nowrap">'
                f'{f}</span>'
                for f in fas_tampil
            )
            if fas_sisa > 0:
                fas_spans += (
                    f'<span style="background:#F3F4F6;color:#9CA3AF;'
                    f'padding:.15rem .5rem;border-radius:99px;font-size:.7rem">'
                    f'+{fas_sisa}</span>'
                )
            st.markdown(
                f'<div style="display:flex;flex-wrap:wrap;gap:4px;margin-top:6px">'
                f'{fas_spans}</div>',
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────
#  RINGKASAN PENCARIAN
# ─────────────────────────────────────────────────────────────

def _render_ringkasan(params: dict):
    if not params:
        return
    budget    = params.get("budget", 0)
    jarak     = params.get("jarak", 0)
    ukuran    = params.get("ukuran", "—")
    jenis     = params.get("jenis", "—")
    fasilitas = params.get("fasilitas", [])
    budget_str = f"Rp {budget:,.0f}".replace(",", ".")
    fas_str    = ", ".join(fasilitas) if fasilitas else "Semua"

    st.markdown(
        f"""
        <div style="
            background:#FFFFFF;border:1px solid #E5E7EB;
            border-radius:12px;padding:14px 18px;
            margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,.07)">
            <div style="font-size:.72rem;font-weight:700;color:#9CA3AF;
                        text-transform:uppercase;letter-spacing:.07em;margin-bottom:7px">
                Ringkasan Pencarian
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:6px 20px;
                        font-size:.85rem;color:#4B5563">
                <span><img src="https://cdn-icons-png.flaticon.com/512/631/631180.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> <b>Budget:</b> Rp {budget:,.0f}/bln</span>
                <span><img src="https://cdn-icons-png.flaticon.com/512/484/484141.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> <b>Jarak:</b> ≤ {jarak} m</span>
                <span><img src="https://cdn-icons-png.flaticon.com/512/8112/8112972.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> <b>Ukuran:</b> {ukuran}</span>
                <span><img src="https://cdn-icons-png.flaticon.com/512/33/33308.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> <b>Jenis:</b> {jenis}</span>
                <span><img src="https://cdn-icons-png.flaticon.com/512/4350/4350275.png" width="22" style="border-radius:50%;background:#E5E7EB;padding:3px"> <b>Fasilitas:</b> {fas_str}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
#  RENDER UTAMA
# ─────────────────────────────────────────────────────────────

def render():
    kos_list    = st.session_state.get("search_results") or []
    params      = st.session_state.get("search_params", {})
    filter_mode = st.session_state.get("filter_mode", "strict")

    # Jika belum ada hasil → tampilkan info
    if not kos_list:
        st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
        col_c, = st.columns([1])
        with col_c:
            st.info(
                "Belum ada hasil pencarian. "
                "Silakan gunakan menu **Cari Kos** untuk memulai."
            )
        return

    # ── HEADER BAR ───────────────────────────────────────────
    filter_color = "#059669" if filter_mode == "strict" else "#F59E0B"
    filter_label = "Strict Filtering" if filter_mode == "strict" else "Relaxed Filtering"

    st.markdown(
        f"""
        <div style="background:#FFFFFF;border-bottom:1px solid #E5E7EB;
                    padding:18px 2rem 14px">
            <div style="display:flex;justify-content:space-between;
                        flex-wrap:wrap;gap:50px;align-items:flex-start;width:100%">
                <div>
                    <span style="background:#D1FAE5;color:#065F46;font-size:.72rem;
                                 font-weight:700;padding:.22rem .75rem;border-radius:99px;
                                 letter-spacing:.06em;text-transform:uppercase">
                        Hasil Rekomendasi
                    </span>
                    <div style="font-family:'Sora',sans-serif;font-size:1.5rem;
                                font-weight:800;color:#111827;margin:.3rem 0 .15rem">
                        Ditemukan <span style="color:#059669">{len(kos_list)}</span>
                        Kos Terbaik
                    </div>
                    <div style="font-size:.82rem;color:#4B5563">
                        Diurutkan dari skor MOORA tertinggi ke terendah
                    </div>
                </div>
                <div style="font-size:.82rem;color:#9CA3AF;text-align:right;padding-top:4px">
                    Algoritma: <b style="color:#047857">K-Means + MOORA</b><br>
                    Mode: <b style="color:{filter_color}">{filter_label}</b>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── KONTEN ───────────────────────────────────────────────
    st.markdown("<div style='max-width:1180px;margin:0 auto;padding:1.5rem 1rem'>",
                unsafe_allow_html=True)

    # Ringkasan pencarian
    _render_ringkasan(params)
    
    semua_daerah = sorted({k.get("daerah","") for k in kos_list if k.get("daerah","")})
    
    col_filter, col_back = st.columns([5, 2])
    with col_filter:
        daerah_dipilih = st.selectbox(
            "Filter Daerah", options=["Semua Daerah"] + semua_daerah,
            key="filter_daerah",)
    with col_back:
        st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
        if st.button("← Cari Ulang", key="btn_back_search", use_container_width=True):
            st.session_state.current_page = "search"
            st.rerun()

    kos_tampil = (
        [k for k in kos_list if k.get("daerah", "") == daerah_dipilih]
        if daerah_dipilih != "Semua Daerah" else kos_list
    )
    
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── GRID 3 KOLOM ─────────────────────────────────────────
    cols_per_row = 3
    for i in range(0, len(kos_tampil), cols_per_row):
        row_kos = kos_tampil[i: i + cols_per_row]
        grid    = st.columns(len(row_kos), gap="medium")

        for col_idx, (col, kos) in enumerate(zip(grid, row_kos)):
            rank = i + col_idx + 1
            with col:
                _render_kos_card(kos, rank)
                # Tombol Lihat Detail
                if st.button(
                    "Lihat Detail",
                    key=f"detail_{kos['id']}",
                    use_container_width=True,
                    type="primary",
                ):
                    st.session_state.selected_kos = kos["id"]
                    st.session_state.current_page = "detail"
                    st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── CATATAN SISTEM ────────────────────────────────────────
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    if filter_mode == "relaxed":
        st.warning(
            "**Mode Relaxed Filtering Aktif** — Tidak ada kos yang 100% sesuai "
            "kriteria Anda. Sistem memperlebar toleransi: budget +20%, "
            "jarak +1.5 km, dan minimal 75% fasilitas tersedia."
        )
    else:
        st.success(
            "**Strict Filtering Berhasil** — Semua kos memenuhi 100% kriteria Anda. "
            "Urutan ditentukan oleh skor MOORA tertinggi ke terendah."
        )

    st.markdown("</div>", unsafe_allow_html=True)