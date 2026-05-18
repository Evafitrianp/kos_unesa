import streamlit as st


def render():
        # ── HEADER ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:2rem">
        <span class="section-label">Hubungi Kami</span>
        <h1 class="section-title" style="margin-top:.5rem">
            Kontak & <span style="color:var(--primary)">Dukungan</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # ── KONTEN CONTACT ─────────────────────────────────────────────
    contact_cols = st.columns(2, gap="large")

    with contact_cols[0]:
        st.markdown("""
        <div class="card">
            <h2 style="font-family:'Sora',sans-serif;font-size:1.1rem;font-weight:700;color:var(--text-primary);margin-bottom:1.5rem">
                Informasi Kontak</h2>
            <div style="display: flex; flex-direction: column; gap: 1.5rem; font-size: 1.1rem;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/542/542689.png" width="35" height="35" style="object-fit: contain; border-radius: 50%; border: 2px solid #111827; padding: 6px;">
                    <span><strong>Email:</strong> admin@kosku-unesa.ac.id</span></div>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/455/455705.png" width="35" height="35" style="object-fit: contain; border-radius: 50%; border: 2px solid #111827; padding: 6px;">
                    <span><strong>WhatsApp:</strong> +62 813-3571-5350</span></div>
                <div style="display: flex; align-items: center; gap: 15px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/484/484167.png" width="35" height="35" style="object-fit: contain; border-radius: 50%; border: 2px solid #111827; padding: 6px;">
                    <span><strong>Lokasi:</strong> Kampus UNESA Ketintang, Surabaya</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with contact_cols[1]:
        st.markdown("""
        <div class="card">
            <h2 style="font-family:'Sora',sans-serif;font-size:1.1rem;font-weight:700;color:var(--text-primary);margin-bottom:1.5rem">
                FAQ & Dukungan</h2>
            <div style="margin-bottom:1rem">
                <details style="cursor:pointer">
                    <summary style="font-weight:600;color:var(--text-primary);
                                   padding:.5rem;background:var(--bg);border-radius:var(--radius-xs);
                                   margin-bottom:.5rem">
                        Bagaimana cara menggunakan platform?
                    </summary>
                    <p style="color:var(--text-secondary);font-size:.9rem;
                              margin-top:.75rem;line-height:1.6">
                        Pengguna cukup mengisi kriteria seperti budget, jarak, fasilitas, ukuran kamar, 
                        dan jenis kos. Setelah itu, sistem akan menampilkan rekomendasi kos yang paling sesuai.</p>
                </details></div>
            <div style="margin-bottom:1rem">
                <details style="cursor:pointer">
                    <summary style="font-weight:600;color:var(--text-primary);
                                   padding:.5rem;background:var(--bg);border-radius:var(--radius-xs);
                                   margin-bottom:.5rem">
                        Apakah hasil rekomendasi bisa disesuaikan?
                    </summary>
                    <p style="color:var(--text-secondary);font-size:.9rem;
                              margin-top:.75rem;line-height:1.6">
                        Ya, hasil rekomendasi akan menyesuaikan dengan kriteria yang Anda masukkan. 
                        Semakin spesifik preferensi yang diberikan, semakin relevan hasil yang ditampilkan.</p>
                </details></div>
            <div style="margin-bottom:1rem">
                <details style="cursor:pointer">
                    <summary style="font-weight:600;color:var(--text-primary);
                                   padding:.5rem;background:var(--bg);border-radius:var(--radius-xs);
                                   margin-bottom:.5rem">
                        Apakah platform ini membantu dalam proses pemesanan kos?
                    </summary>
                    <p style="color:var(--text-secondary);font-size:.9rem;
                              margin-top:.75rem;line-height:1.6">
                        Platform ini membantu dalam menemukan kos yang sesuai, 
                        sedangkan proses pemesanan dilakukan secara langsung dengan pemilik kos melalui kontak yang tersedia.</p>
                </details></div>
        </div>
        """, unsafe_allow_html=True)

