import os
import streamlit as st
import io
import urllib.parse
from PIL import Image
from utils.algoritma import format_harga, format_jarak


# ─────────────────────────────────────────────────────────────
#  HELPER FOTO (sama dengan results.py)
# ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _foto_path(kos: dict) -> str | None:
    if str(kos.get("foto_tersedia", "T")).strip().upper() != "Y":
        return None
    for ext in ("jpg", "jpeg", "png"):
        path = os.path.join(BASE_DIR, "foto", f"{kos['id']}.{ext}")
        if os.path.isfile(path):
            return path
    return None

def crop_image(path, size=(800, 420)):
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

# ─────────────────────────────────────────────────────────────
#  RENDER UTAMA
# ─────────────────────────────────────────────────────────────

def render():
    # ── Ambil data dari session ───────────────────────────────
    kos_id   = st.session_state.get("selected_kos")
    kos_list = st.session_state.get("search_results") or []

    if not kos_list:
        st.warning("Sesi pencarian berakhir. Silakan cari kos terlebih dahulu.")
        if st.button("← Kembali ke Pencarian", key="btn_no_data"):
            st.session_state.current_page = "search"
            st.rerun()
        return

    # Cari kos berdasarkan id, fallback ke index 0
    kos = next((k for k in kos_list if k["id"] == kos_id), kos_list[0])

    # ── Pre-compute nilai ─────────────────────────────────────
    ids        = [k["id"] for k in kos_list]
    rank       = ids.index(kos["id"]) + 1 if kos["id"] in ids else "—"
    harga_str  = format_harga(kos["harga"])
    jarak_str  = format_jarak(kos["jarak_km"])
    moora_val  = kos.get("skor_moora", 0.0)
    kesesuaian = kos.get("kesesuaian_pct", 0)
    nama       = kos.get("nama", "—")
    alamat     = kos.get("alamat", "—")
    deskripsi  = kos.get("deskripsi", "—")
    pemilik    = kos.get("pemilik", "Pemilik Kos")
    daerah     = kos.get("daerah", "")
    no_wa      = kos.get("no_wa", "0")
    cluster    = kos.get("cluster", "Standar")
    cluster_icon = {"Ekonomis": "🌿", "Standar": "⭐"}.get(cluster, "💎")
    badge_bg   = {"Ekonomis": "#D1FAE5", "Standar": "#FEF3C7"}.get(cluster, "#DBEAFE")
    badge_col  = {"Ekonomis": "#065F46", "Standar": "#92400E"}.get(cluster, "#1E3A5F")
    nama_enc   = nama.replace(" ", "%20")
    wa_url     = (
        f"https://wa.me/{no_wa}?text=Halo%20{pemilik.replace(' ','%20')}%2C%20"
        f"saya%20tertarik%20dengan%20{nama_enc}%20dari%20KosKu%20UNESA."
    )
    foto_path  = _foto_path(kos)
    fasilitas  = kos.get("fasilitas", [])

    # ── KONTEN HALAMAN ────────────────────────────────────────
    st.markdown(
        "<div style='max-width:1180px;margin:0 auto;padding:1.5rem 1rem'>",
        unsafe_allow_html=True,
    )

    # Tombol kembali + breadcrumb
    col_bk, col_bc = st.columns([2, 6])
    with col_bk:
        if st.button("Kembali ke Hasil", key="btn_back_results",
                     use_container_width=True):
            st.session_state.current_page = "results"
            st.rerun()

    st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)

    # ── LAYOUT 2 KOLOM ───────────────────────────────────────
    left_col, right_col = st.columns([6, 4], gap="large")

    # ════════════════════════════════════════════════════════
    #  KOLOM KIRI — Foto, Deskripsi, Fasilitas, Lokasi
    # ════════════════════════════════════════════════════════
    with left_col:
    
        # 1. FOTO UTAMA
        if foto_path:
            img = crop_image(foto_path, size=(800, 420))
            st.image(img, use_container_width=True)
        else:
            st.markdown(
                """
                <div style="
                    background:#E5E7EB;height:300px;border-radius:12px;
                    display:flex;flex-direction:column;align-items:center;
                    justify-content:center;color:#9CA3AF;gap:8px">
                    <span style="font-size:2.5rem">📷</span>
                    <span style="font-size:.9rem">No Image Available</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

        # 2. DESKRIPSI
        st.markdown(
            "<h3 style='font-family:Sora,sans-serif;font-size:1rem;"
            "font-weight:700;color:#111827;margin-bottom:.5rem'>"
            "<img src='https://cdn-icons-png.flaticon.com/512/1584/1584961.png' "
            "width='18' style='border-radius:50%;background:#E5E7EB;padding:2px;"
            "vertical-align:middle'> Tentang Kos Ini</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='font-size:.9rem;color:#4B5563;line-height:1.8;"
            f"background:#F0FDF4;border-radius:8px;padding:14px 16px;"
            f"border-left:3px solid #059669;margin-bottom:1.25rem'>"
            f" {deskripsi}</div>",
            unsafe_allow_html=True,
        )

        # 3. FASILITAS
        st.markdown(
            "<h3 style='font-family:Sora,sans-serif;font-size:1rem;"
            "font-weight:700;color:#111827;margin-bottom:.5rem'>"
            "<img src='https://cdn-icons-png.flaticon.com/512/4350/4350275.png' "
            "width='18' style='border-radius:50%;background:#E5E7EB;padding:2px;"
            "vertical-align:middle'> Fasilitas Lengkap</h3>",
            unsafe_allow_html=True,
        )
        if fasilitas:
            fas_html = "".join(
                f'<span style="background:#D1FAE5;color:#065F46;'
                f'padding:.25rem .8rem;border-radius:99px;font-size:.82rem;'
                f'font-weight:500;margin:.2rem .2rem .2rem 0;display:inline-block">'
                f' {f}</span>'
                for f in fasilitas
            )
            st.markdown(
                f'<div style="display:flex;flex-wrap:wrap;gap:2px;margin-bottom:1.25rem">'
                f'{fas_html}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<p style='color:#9CA3AF;font-size:.85rem'>—</p>",
                unsafe_allow_html=True,
            )

        # 4. LOKASI
        maps_url = (
            "https://www.google.com/maps/search/?api=1&query="
            + urllib.parse.quote(alamat + " Surabaya")
        )
        
        st.markdown(
            "<h3 style='font-family:Sora,sans-serif;font-size:1rem;"
            "font-weight:700;color:#111827;margin-bottom:.5rem'>"
            "<img src='https://cdn-icons-png.flaticon.com/512/535/535188.png' "
            "width='18' style='border-radius:50%;background:#E5E7EB;padding:2px;"
            "vertical-align:middle'> Lokasi</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style='background:#F9FAFB;border:1px solid #E5E7EB;
                        border-radius:12px;padding:1.25rem 1.5rem;
                        display:flex;align-items:center;
                        justify-content:space-between;gap:1rem;flex-wrap:wrap'>
                <div style='font-size:.9rem;color:#374151;font-weight:500'>
                     {alamat}
                </div>
                <a href='{maps_url}' target='_blank'
                style='display:inline-flex;align-items:center;gap:6px;
                        background:#059669;color:#fff;
                        padding:.4rem 1rem;border-radius:8px;
                        font-size:.8rem;font-weight:600;
                        text-decoration:none;white-space:nowrap;
                        box-shadow:0 2px 8px rgba(5,150,105,.3)'>
                    <img src='https://cdn-icons-png.flaticon.com/512/2875/2875433.png'
                        width='14' style='filter:brightness(10)'>
                    Buka Maps
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ════════════════════════════════════════════════════════
    #  KOLOM KANAN — Info Card (sticky via CSS tidak berlaku,
    #  tapi tetap muncul di atas karena urutan render)
    # ════════════════════════════════════════════════════════
    with right_col:

        # ── CLUSTER BADGE + RANK ──────────────────────────
        st.markdown(
            f"<div style='display:flex;align-items:center;"
            f"justify-content:space-between;margin-bottom:10px'>"
            f"<span style='background:{badge_bg};color:{badge_col};"
            f"font-size:.75rem;font-weight:700;padding:.25rem .85rem;"
            f"border-radius:99px;text-transform:uppercase;letter-spacing:.04em'>"
            f"{cluster_icon} Cluster {cluster}</span>"
            f"<span style='font-size:.78rem;font-weight:700;color:#9CA3AF'>"
            f"Rank #{rank}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        
        daerah_badge = (
            f"<span style='background:#F3F4F6;color:#374151;"
            f"font-size:.72rem;font-weight:600;"
            f"padding:.2rem .65rem;border-radius:99px;"
            f"border:1px solid #E5E7EB'>"
            f" {daerah}</span>"
        ) if daerah else ""
        
        # ── NAMA KOS ──────────────────────────────────────
        st.markdown(
            f"<div style='font-family:Sora,sans-serif;font-size:1.3rem;"
            f"font-weight:800;color:#111827;line-height:1.3;margin-bottom:15px'>"
            f"{nama}</div>"
            f"<div style='font-size:.82rem;color:#9CA3AF;margin-top:8px;margin-bottom:12px'>"
            f" {daerah_badge}</div>",
            unsafe_allow_html=True,
        )

        st.divider()

        # ── HARGA ─────────────────────────────────────────
        st.markdown(
            "<div style='font-size:.7rem;color:#9CA3AF;text-transform:uppercase;"
            "letter-spacing:.06em;font-weight:600'>Harga Per Bulan</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='font-family:Sora,sans-serif;font-size:1.55rem;"
            f"font-weight:800;color:#047857;margin-bottom:12px'>{harga_str}</div>",
            unsafe_allow_html=True,
        )

        # ── QUICK INFO GRID (4 kotak) ─────────────────────
        q1, q2 = st.columns(2)
        q3, q4 = st.columns(2)
        info_style = (
            "background:#F0FDF4;border-radius:8px;padding:5px;"
            "text-align:center;font-size:.8rem"
        )
        with q1:
            st.markdown(
                f"<div style='{info_style}'>"
                f"<img src='https://cdn-icons-png.flaticon.com/512/484/484141.png' "
                f"width='15' style='border-radius:50%;background:#E5E7EB;padding:3px'><br>"
                f"<span style='font-size:.65rem;color:#9CA3AF;text-transform:uppercase;"
                f"font-weight:600'>Jarak</span><br>"
                f"<b>{int(kos['jarak_km']*1000)} m</b></div>",
                unsafe_allow_html=True,
            )
        with q2:
            st.markdown(
                f"<div style='{info_style}'>"
                f"<img src='https://cdn-icons-png.flaticon.com/512/8112/8112972.png' "
                f"width='15' style='border-radius:50%;background:#E5E7EB;padding:3px'><br>"
                f"<span style='font-size:.65rem;color:#9CA3AF;text-transform:uppercase;"
                f"font-weight:600'>Ukuran</span><br>"
                f"<b>{kos.get('ukuran','—')}</b></div>",
                unsafe_allow_html=True,
            )
        with q3:
            st.markdown(
                f"<div style='{info_style}'>"
                f"<img src='https://cdn-icons-png.flaticon.com/512/33/33308.png' "
                f"width='15' style='border-radius:50%;background:#E5E7EB;padding:3px'><br>"
                f"<span style='font-size:.65rem;color:#9CA3AF;text-transform:uppercase;"
                f"font-weight:600'>Jenis</span><br>"
                f"<b>{kos.get('jenis','—')}</b></div>",
                unsafe_allow_html=True,
            )
        with q4:
            st.markdown(
                f"<div style='{info_style}'>"
                f"<img src='https://cdn-icons-png.flaticon.com/512/4350/4350275.png' "
                f"width='15' style='border-radius:50%;background:#E5E7EB;padding:3px'><br>"
                f"<span style='font-size:.65rem;color:#9CA3AF;text-transform:uppercase;"
                f"font-weight:600'>Fasilitas</span><br>"
                f"<b>{len(fasilitas)} item</b></div>",
                unsafe_allow_html=True,
            )

        st.divider()

        # ── SKOR AI (st.progress — native, pasti render) ──
        st.markdown(
            "<div style='font-size:.7rem;color:#9CA3AF;text-transform:uppercase;"
            "letter-spacing:.06em;font-weight:600;margin-bottom:8px'>"
            "Skor Analisis AI</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;"
            f"font-size:.8rem;color:#4B5563;margin-bottom:3px'>"
            f"<span><img src='https://cdn-icons-png.flaticon.com/512/3558/3558884.png' "
            f"width='16' style='vertical-align:middle;margin-right:4px'>Skor MOORA</span><b>{moora_val:.3f}</b></div>",
            unsafe_allow_html=True,
        )
        st.progress(float(moora_val))

        st.markdown(
            f"<div style='display:flex;justify-content:space-between;"
            f"font-size:.8rem;color:#4B5563;margin:8px 0 3px'>"
            f"<span><img src='https://cdn-icons-png.flaticon.com/512/845/845646.png' "
            f"width='16' style='vertical-align:middle;margin-right:4px'>Kesesuaian</span><b>{kesesuaian}%</b></div>",
            unsafe_allow_html=True,
        )
        st.progress(kesesuaian / 100)

        st.divider()

        # ── PEMILIK ───────────────────────────────────────
        st.markdown(
            f"<div style='font-size:.875rem;color:#4B5563;margin-bottom:12px'>"
            f"<img src='https://cdn-icons-png.flaticon.com/512/1077/1077012.png'"
            f"width='18' style='border-radius:50%;background:#E5E7EB;padding:2px;"
            f"vertical-align:middle'> <b>Pemilik:</b> {pemilik}</div>",
            unsafe_allow_html=True,
        )

        # ── TOMBOL WHATSAPP ───────────────────────────────
        st.link_button(
            "Hubungi Pemilik via WhatsApp",
            url=wa_url,
            use_container_width=True,
            type="primary",
        )
        st.markdown(
            f"<div style='font-size:.72rem;color:#9CA3AF;text-align:center;margin-top:4px'>"
            f"Diarahkan ke WhatsApp untuk survei &amp; booking</div>",
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)