import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score

# 1. Baca dataset
df = pd.read_csv("data_kos.csv")
# 2. Ambil fitur yang digunakan untuk clustering (Sesuai Bab 3)
fitur = ["Harga (Bulan)", "Jarak (km)", "Total Fasilitas", "Ukuran Kamar (M2)"]
X = df[fitur].fillna(0)
# 3. Normalisasi Min-Max
scaler = MinMaxScaler()
X_norm = scaler.fit_transform(X)
# 4. Jalankan K-Means dengan k=3 (Ekonomis, Standar, Premium)
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X_norm)
# 5. Hitung Silhouette Score
score = silhouette_score(X_norm, labels, metric='euclidean')

print(f"Hasil Silhouette Score untuk k=3 adalah: {score:.4f}")