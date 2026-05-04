"""
utils/dummy_data.py
───────────────────
Data dummy untuk 3 kos contoh.
Pada implementasi nyata, data ini berasal dari database/CSV hasil K-Means & MOORA.
"""

KOS_LIST = [
    {
        "id": 1,
        "nama": "Kos Griya Hijau Asri",
        "alamat": "Jl. Ketintang Madya No. 12, Surabaya",
        "harga": 650_000,
        "jarak_km": 0.35,
        "jenis": "Putri",
        "ukuran": "3x4 m",
        "cluster": "Ekonomis",
        "cluster_badge": "badge-ekonomis",
        "skor_moora": 0.912,
        "kesesuaian_pct": 94,
        "fasilitas": ["WiFi", "Kamar Mandi Dalam", "Lemari", "Meja Belajar", "Listrik Token"],
        "deskripsi": (
            "Kos Griya Hijau Asri menawarkan hunian nyaman dan terjangkau "
            "hanya 350 meter dari Kampus UNESA Ketintang. Suasana asri dengan "
            "taman kecil di depan, lingkungan aman, dan dikelola oleh ibu kos "
            "yang ramah. Cocok untuk mahasiswi yang mengutamakan kenyamanan "
            "dengan budget hemat."
        ),
        "no_wa": "6281234567890",
        "foto_thumb": "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=600&q=80",
        "foto_list": [
            "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800&q=80",
            "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80",
            "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80",
        ],
        "pemilik": "Bu Sari",
    },
    {
        "id": 2,
        "nama": "Kos Mahajaya Residence",
        "alamat": "Jl. Ketintang Baru No. 27, Surabaya",
        "harga": 1_100_000,
        "jarak_km": 0.55,
        "jenis": "Campur",
        "ukuran": "4x4 m",
        "cluster": "Standar",
        "cluster_badge": "badge-standar",
        "skor_moora": 0.847,
        "kesesuaian_pct": 88,
        "fasilitas": ["WiFi", "AC", "Kamar Mandi Dalam", "Lemari", "Meja Belajar", "Dapur Bersama", "Parkir Motor"],
        "deskripsi": (
            "Kos Mahajaya Residence adalah pilihan ideal bagi mahasiswa yang "
            "menginginkan fasilitas lengkap dengan harga terjangkau. Tersedia "
            "kamar ber-AC, kamar mandi dalam, serta dapur bersama yang bersih. "
            "Lokasi strategis 550 meter dari UNESA, dekat minimarket dan "
            "warung makan mahasiswa."
        ),
        "no_wa": "6289876543210",
        "foto_thumb": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=600&q=80",
        "foto_list": [
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=80",
            "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&q=80",
            "https://images.unsplash.com/photo-1540518614846-7eded433c457?w=800&q=80",
        ],
        "pemilik": "Pak Budi",
    },
    {
        "id": 3,
        "nama": "Kos Elegan Premium Suite",
        "alamat": "Jl. Ketintang Timur No. 5A, Surabaya",
        "harga": 1_750_000,
        "jarak_km": 0.72,
        "jenis": "Putra",
        "ukuran": "4x5 m",
        "cluster": "Premium",
        "cluster_badge": "badge-premium",
        "skor_moora": 0.791,
        "kesesuaian_pct": 81,
        "fasilitas": [
            "WiFi Dedicated", "AC Inverter", "Kamar Mandi Dalam",
            "Kasur Spring Bed", "Lemari 2 Pintu", "Meja Kerja Besar",
            "TV 32\"", "Kulkas Mini", "CCTV 24 Jam", "Parkir Mobil/Motor",
        ],
        "deskripsi": (
            "Kos Elegan Premium Suite menghadirkan pengalaman hunian premium "
            "setara apartemen. Kamar luas 4x5 meter dilengkapi spring bed, "
            "kulkas mini, dan TV pribadi. Sistem keamanan CCTV 24 jam "
            "menjamin ketenangan. Ideal untuk mahasiswa pascasarjana atau "
            "yang mengutamakan kenyamanan maksimal."
        ),
        "no_wa": "6281122334455",
        "foto_thumb": "https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=600&q=80",
        "foto_list": [
            "https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=800&q=80",
            "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=800&q=80",
            "https://images.unsplash.com/photo-1631049552057-403cdb8f0658?w=800&q=80",
        ],
        "pemilik": "Pak Eko",
    },
]


def get_dummy_kos_list() -> list[dict]:
    """Kembalikan seluruh daftar kos dummy."""
    return KOS_LIST


def get_kos_by_id(kos_id: int) -> dict | None:
    """Kembalikan satu kos berdasarkan ID-nya."""
    for k in KOS_LIST:
        if k["id"] == kos_id:
            return k
    return None


def format_harga(harga: int) -> str:
    """Format angka harga menjadi string Rupiah yang rapi."""
    return f"Rp {harga:,.0f}".replace(",", ".")


def format_jarak(jarak_km: float) -> str:
    """Format jarak dalam meter atau km."""
    if jarak_km < 1:
        return f"{int(jarak_km * 1000)} m dari kampus"
    return f"{jarak_km:.1f} km dari kampus"
