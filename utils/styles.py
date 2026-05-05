import streamlit as st

# ─────────────────────────────────────────────
#  GLOBAL CSS — disuntikkan sekali di app.py
# ─────────────────────────────────────────────

def inject_global_styles():
    st.markdown("""
    <style>
    /* ============================================================
       1. FONTS & VARIABLES
    ============================================================ */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap');

    [data-testid="stSidebar"] {display: none !important;}
    
    :root {
        --primary:        #059669;
        --primary-dark:   #047857;
        --primary-light:  #D1FAE5;
        --secondary:      #0284C7;
        --accent:         #F59E0B;
        --danger:         #EF4444;
        --bg:             #F0FDF4;
        --bg-card:        #FFFFFF;
        --bg-dark:        #064E3B;
        --text-primary:   #111827;
        --text-secondary: #4B5563;
        --text-muted:     #9CA3AF;
        --border:         #E5E7EB;
        --shadow-xs:      0 1px 3px rgba(0,0,0,.07);
        --shadow-sm:      0 2px 8px rgba(0,0,0,.09);
        --shadow-md:      0 6px 20px rgba(0,0,0,.11);
        --shadow-lg:      0 12px 40px rgba(0,0,0,.14);
        --shadow-primary: 0 6px 24px rgba(5,150,105,.35);
        --radius-xs:  6px;
        --radius-sm:  10px;
        --radius-md:  14px;
        --radius-lg:  20px;
        --radius-xl:  28px;
        --transition: all .22s cubic-bezier(.4,0,.2,1);
    }

    /* ============================================================
       2. RESET STREAMLIT CHROME
    ============================================================ */
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { display: none !important; }
    .stDeployButton { display: none !important; }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-primary);
    }

    /* Remove default padding from main container */
    .main > div { padding-top: 0 !important; }
    section.main > div.block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: #a7f3d0; border-radius: 99px; }

    /* ============================================================
       3. NAVBAR
    ============================================================ */
    .navbar {
        position: fixed;
        top: 0;
        z-index: 999;
        background: rgba(255,255,255,.95);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--border);
        padding: 0 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 64px;
        box-shadow: var(--shadow-xs);
    }
    .navbar-brand {
        font-family: 'Sora', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--primary);
        display: flex;
        align-items: center;
        gap: .5rem;
        text-decoration: none;
    }
    .navbar-brand .brand-dot {
        display: inline-block;
        width: 8px; height: 8px;
        background: var(--accent);
        border-radius: 50%;
        margin-left: 2px;
        vertical-align: super;
    }
    .nav-links {
        display: flex;
        gap: .25rem;
        align-items: center;
    }
    .nav-pill {
        padding: .4rem 1rem;
        border-radius: 99px;
        font-size: .875rem;
        font-weight: 500;
        color: var(--text-secondary);
        cursor: pointer;
        transition: var(--transition);
        border: none;
        background: transparent;
        text-decoration: none;
    }
    .nav-pill:hover { background: var(--primary-light); color: var(--primary-dark); }
    .nav-pill.active {
        background: var(--primary-light);
        color: var(--primary-dark);
        font-weight: 600;
    }
    .nav-cta {
        padding: .45rem 1.15rem;
        border-radius: 99px;
        background: var(--primary);
        color: #fff !important;
        font-size: .875rem;
        font-weight: 600;
        cursor: pointer;
        transition: var(--transition);
        border: none;
        margin-left: .5rem;
        box-shadow: var(--shadow-primary);
    }
    .nav-cta:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
        box-shadow: 0 8px 28px rgba(5,150,105,.4);
    }

    /* ============================================================
       4. STREAMLIT BUTTON OVERRIDES (navbar row)
    ============================================================ */
    /* Remove all default Streamlit button styling inside nav container */
    div.nav-container div[data-testid="stButton"] > button {
        background: transparent !important;
        border: none !important;
        color: var(--text-secondary) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: .9rem !important;
        font-weight: 500 !important;
        padding: .45rem 1.1rem !important;
        border-radius: 99px !important;
        transition: var(--transition) !important;
        box-shadow: none !important;
        width: 100%;
    }
    div.nav-container div[data-testid="stButton"] > button:hover {
        background: var(--primary-light) !important;
        color: var(--primary-dark) !important;
        transform: none !important;
    }
    div.nav-container div[data-testid="stButton"] > button:focus,
    div.nav-container div[data-testid="stButton"] > button:active {
        box-shadow: none !important;
        border: none !important;
        outline: none !important;
    }

    /* ============================================================
       5. GENERAL BUTTONS
    ============================================================ */
    div[data-testid="stButton"].btn-primary > button {
        background: var(--primary) !important;
        color: #fff !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        font-size: .95rem !important;
        padding: .75rem 2rem !important;
        box-shadow: var(--shadow-primary) !important;
        transition: var(--transition) !important;
    }
    div[data-testid="stButton"].btn-primary > button:hover {
        background: var(--primary-dark) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(5,150,105,.45) !important;
    }

    div[data-testid="stButton"].btn-outline > button {
        background: transparent !important;
        color: var(--primary) !important;
        border: 2px solid var(--primary) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 600 !important;
        padding: .65rem 1.5rem !important;
        transition: var(--transition) !important;
    }
    div[data-testid="stButton"].btn-outline > button:hover {
        background: var(--primary-light) !important;
        transform: translateY(-1px) !important;
    }

    div[data-testid="stButton"].btn-whatsapp > button {
        background: #25D366 !important;
        color: #fff !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: .8rem 2rem !important;
        box-shadow: 0 6px 20px rgba(37,211,102,.4) !important;
        transition: var(--transition) !important;
    }
    div[data-testid="stButton"].btn-whatsapp > button:hover {
        background: #22c55e !important;
        transform: translateY(-2px) !important;
    }

    div[data-testid="stButton"].btn-card > button {
        background: var(--primary-light) !important;
        color: var(--primary-dark) !important;
        border: 1.5px solid var(--primary) !important;
        border-radius: var(--radius-xs) !important;
        font-weight: 600 !important;
        font-size: .82rem !important;
        padding: .4rem 1rem !important;
        transition: var(--transition) !important;
        width: 100%;
    }
    div[data-testid="stButton"].btn-card > button:hover {
        background: var(--primary) !important;
        color: #fff !important;
        transform: none !important;
    }

    /* ============================================================
       6. CARDS & CONTAINERS
    ============================================================ */
    .card {
        background: var(--bg-card);
        border-radius: var(--radius-lg);
        padding: 2rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border);
        transition: var(--transition);
    }
    .card:hover { box-shadow: var(--shadow-md); }

    .kos-card {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border);
        transition: var(--transition);
        height: 100%;
    }
    .kos-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-4px);
        border-color: var(--primary-light);
    }
    .kos-card-img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        display: block;
    }
    .kos-card-body { padding: 1.25rem; }
    .kos-card-title {
        font-family: 'Sora', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: .25rem;
    }
    .kos-card-subtitle {
        font-size: .82rem;
        color: var(--text-muted);
        margin-bottom: .75rem;
    }

    /* ============================================================
       7. BADGES / LABELS
    ============================================================ */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: .3rem;
        padding: .22rem .7rem;
        border-radius: 99px;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .03em;
        text-transform: uppercase;
    }
    .badge-ekonomis  { background: #D1FAE5; color: #065F46; }
    .badge-standar   { background: #FEF3C7; color: #92400E; }
    .badge-premium   { background: #DBEAFE; color: #1E3A5F; }

    /* ============================================================
       8. FORM ELEMENTS OVERRIDE
    ============================================================ */
    div[data-testid="stSlider"] > div > div > div > div {
        background: var(--primary) !important;
    }
    div[data-testid="stSlider"] > div > div > div {
        background: var(--primary-light) !important;
    }

    /* Multiselect tags */
    span[data-baseweb="tag"] {
        background-color: var(--primary-light) !important;
        border: none !important;
    }
    span[data-baseweb="tag"] span { color: var(--primary-dark) !important; }

    /* Select box & multiselect border */
    div[data-baseweb="select"] > div:first-child,
    div[data-baseweb="input"] > div:first-child {
        border-color: var(--border) !important;
        border-radius: var(--radius-sm) !important;
        transition: var(--transition) !important;
    }
    div[data-baseweb="select"] > div:first-child:focus-within,
    div[data-baseweb="input"] > div:first-child:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(5,150,105,.15) !important;
    }

    /* Radio group */
    div[data-testid="stRadio"] > label {
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
    }

    /* ============================================================
       9. HERO SECTION
    ============================================================ */
    .hero-section {
        background: linear-gradient(135deg, #064E3B 0%, #047857 40%, #059669 70%, #0EA5E9 100%);
        padding: 5rem 2rem 6rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        inset: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -1px; left: 0; right: 0;
        height: 60px;
        background: var(--bg);
        clip-path: ellipse(55% 100% at 50% 100%);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: .4rem;
        background: rgba(255,255,255,.15);
        border: 1px solid rgba(255,255,255,.3);
        backdrop-filter: blur(8px);
        color: #fff;
        padding: .35rem 1rem;
        border-radius: 99px;
        font-size: .8rem;
        font-weight: 600;
        letter-spacing: .04em;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-family: 'Sora', sans-serif;
        font-size: clamp(2rem, 5vw, 3.2rem);
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.2;
        margin-bottom: 1rem;
        text-shadow: 0 2px 20px rgba(0,0,0,.2);
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,.85);
        margin: 0 auto 2.5rem;
        line-height: 1.7;
    }

    /* ============================================================
       10. FEATURE CARDS (Home Page)
    ============================================================ */
    .feature-card {
        background: var(--bg-card);
        border-radius: var(--radius-md);
        padding: 1.75rem;
        text-align: center;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border);
        transition: var(--transition);
        height: 100%;
    }
    .feature-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-4px);
        border-color: var(--primary-light);
    }
    .feature-icon {
        width: 56px; height: 56px;
        border-radius: var(--radius-md);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem;
        margin: 0 auto 1rem;
    }
    .feature-icon-green  { background: var(--primary-light); }
    .feature-icon-blue   { background: #DBEAFE; }
    .feature-icon-amber  { background: #FEF3C7; }
    .feature-title {
        font-family: 'Sora', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: .5rem;
    }
    .feature-desc {
        font-size: .875rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* ============================================================
       11. SECTION TITLES
    ============================================================ */
    .section-label {
        display: inline-block;
        font-size: .75rem;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: var(--primary);
        background: var(--primary-light);
        padding: .25rem .75rem;
        border-radius: 99px;
        margin-bottom: .75rem;
    }
    .section-title {
        font-family: 'Sora', sans-serif;
        font-size: clamp(1.4rem, 3vw, 2rem);
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.25;
        margin-bottom: .5rem;
    }
    .section-subtitle {
        font-size: .95rem;
        color: var(--text-secondary);
        max-width: 520px;
        line-height: 1.65;
    }

    /* ============================================================
       12. STAT PILLS (hero stats row)
    ============================================================ */
    .stat-row {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 1rem;
        margin-top: 2.5rem;
    }
    .stat-pill {
        background: rgba(255,255,255,.15);
        border: 1px solid rgba(255,255,255,.25);
        backdrop-filter: blur(8px);
        border-radius: var(--radius-lg);
        padding: .6rem 1.4rem;
        text-align: center;
        color: #fff;
    }
    .stat-pill-num {
        font-family: 'Sora', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        line-height: 1;
    }
    .stat-pill-label {
        font-size: .75rem;
        color: rgba(255,255,255,.75);
        margin-top: .2rem;
    }

    /* ============================================================
       13. SCORE / PROGRESS BARS
    ============================================================ */
    .score-bar-wrap { margin-bottom: .6rem; }
    .score-bar-label {
        display: flex;
        justify-content: space-between;
        font-size: .8rem;
        color: var(--text-secondary);
        margin-bottom: .2rem;
    }
    .score-bar-track {
        height: 7px;
        background: var(--border);
        border-radius: 99px;
        overflow: hidden;
    }
    .score-bar-fill {
        height: 100%;
        border-radius: 99px;
        background: linear-gradient(90deg, var(--primary), #34D399);
        transition: width .6s ease;
    }

    /* ============================================================
       14. LOADING SPINNER (custom)
    ============================================================ */
    .loading-overlay {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        gap: 1.25rem;
    }
    .spinner {
        width: 52px; height: 52px;
        border: 4px solid var(--primary-light);
        border-top-color: var(--primary);
        border-radius: 50%;
        animation: spin .8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .loading-text {
        font-family: 'Sora', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--primary-dark);
        text-align: center;
    }
    .loading-sub {
        font-size: .85rem;
        color: var(--text-muted);
        text-align: center;
    }

    /* ============================================================
       15. PAGE WRAPPER & CONTENT
    ============================================================ */
    .page-wrapper {
        background: var(--bg);
        min-height: 100vh;
    }
    .content-container {
        max-width: 1180px;
        margin: 0 auto;
        padding: 3rem 2rem;
    }

    /* ============================================================
       16. FACILITY TAGS (Detail page)
    ============================================================ */
    .facility-tag {
        display: inline-flex;
        align-items: center;
        gap: .3rem;
        background: var(--primary-light);
        color: var(--primary-dark);
        padding: .3rem .85rem;
        border-radius: 99px;
        font-size: .82rem;
        font-weight: 500;
        margin: .2rem;
    }

    /* ============================================================
       17. INFO ROW (price / distance)
    ============================================================ */
    .info-row {
        display: flex;
        align-items: center;
        gap: .5rem;
        font-size: .875rem;
        color: var(--text-secondary);
        margin-bottom: .35rem;
    }
    .info-row-icon { font-size: 1rem; }
    .price-tag {
        font-family: 'Sora', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--primary-dark);
    }

    /* ============================================================
       18. BACK BUTTON ROW
    ============================================================ */
    .back-row {
        display: flex;
        align-items: center;
        gap: .5rem;
        color: var(--text-secondary);
        font-size: .875rem;
        cursor: pointer;
        transition: var(--transition);
        margin-bottom: 1.5rem;
        width: fit-content;
    }
    .back-row:hover { color: var(--primary); }

    /* ============================================================
       19. UTILITY
    ============================================================ */
    .divider {
        height: 1px;
        background: var(--border);
        margin: 1rem 0;
    }
    .text-primary-green { color: var(--primary); }
    .text-muted   { color: var(--text-muted); font-size: .85rem; }
    .fw-bold      { font-weight: 700; }
    .mt-1 { margin-top: .5rem; }
    .mb-1 { margin-bottom: .5rem; }
    .mb-2 { margin-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)
