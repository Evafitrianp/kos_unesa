import streamlit as st
from utils.logo import LOGO_B64

# ── Konfigurasi halaman (HARUS di baris pertama Streamlit) ─────────
st.set_page_config(
    page_title  = "KosKu UNESA — Sistem Rekomendasi Kos",
    page_icon   = "logo.png",
    layout      = "wide",
    initial_sidebar_state = "collapsed",
    menu_items  = {
        "Get Help"    : "https://github.com/",
        "Report a bug": "mailto:email@unesa.ac.id",
        "About"       : "# KosKu UNESA\nSistem Rekomendasi Kos berbasis K-Means & MOORA",
    },
)

# ── Import setelah set_page_config ─────────────────────────────────
from utils.styles import inject_global_styles
import pages.home    as home_page
import pages.search  as search_page
import pages.results as results_page
import pages.detail  as detail_page
import pages.about   as about_page
import pages.contact as contact_page

# ── Inisialisasi session state ─────────────────────────────────────
_DEFAULTS = {
    "current_page"  : "home",      # halaman aktif: home|search|results|detail
    "search_results": None,         # list hasil pencarian (dari algoritma)
    "selected_kos"  : None,         # id kos yang dipilih untuk detail
    "search_params" : {},           # parameter terakhir yang digunakan
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── Suntikkan CSS global ────────────────────────────────────────────
inject_global_styles()


# ══════════════════════════════════════════════════════════════════
#  NAVBAR
# ══════════════════════════════════════════════════════════════════
def _nav_btn(label: str, target: str, key: str):
    """Render satu tombol navigasi dengan efek warna jika aktif."""
    # 1. Cek apakah halaman ini sedang dibuka oleh user
    is_active = st.session_state.current_page == target
    
    # 2. Jika aktif, beri warna primary (solid/gelap). Jika tidak, secondary (pucat/outline)
    btn_type = "primary" if is_active else "secondary"
    
    # 3. Gunakan use_container_width=True agar ukuran tombol kaku dan tidak bergeser
    if st.button(label, key=key, type=btn_type, use_container_width=True):
        st.session_state.current_page = target
        st.rerun()

def render_navbar():
    """Render navbar sejajar satu baris dengan logo Base64."""

    col1, col3, col4, col5, col6, col7= st.columns([3, 1.6, 1.6, 1.6, 1.6, 0.2])

    with col1:
        st.markdown(
            f"""
            <div style="font-size:1.5rem;font-weight:bold;padding-top:5px">
                <img src="{LOGO_B64}"
                     width="35"
                     style="vertical-align:middle;margin-right:8px;margin-bottom:6px">
                KosKu <span style="color:var(--accent)">UNESA</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        _nav_btn("Beranda",  "home",   "nav_home")
    with col4:
        _nav_btn("Cari Kos", "search", "nav_search")
    with col5:
        _nav_btn("About",    "about",  "nav_about")
    with col6:
        _nav_btn("Contact",  "contact","nav_contact")

    st.markdown("<hr style='margin-top:5px;margin-bottom:20px'/>", unsafe_allow_html=True,)
# ══════════════════════════════════════════════════════════════════
#  ROUTING
# ══════════════════════════════════════════════════════════════════

PAGE_MAP = {
    "home"   : home_page.render,
    "search" : search_page.render,
    "results": results_page.render,
    "detail" : detail_page.render,
    "about"  : about_page.render,
    "contact": contact_page.render,
}


def main():
    render_navbar()
    current = st.session_state.get("current_page", "home")
    PAGE_MAP.get(current, home_page.render)()


if __name__ == "__main__" or True:
    main()
