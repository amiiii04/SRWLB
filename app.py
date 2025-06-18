import streamlit as st
import pandas as pd
import joblib

# ==========================================
# Load data dan model
# ==========================================
df = joblib.load("data_wisata.pkl")
similarity_matrix = joblib.load("similarity_matrix.pkl")
indices = joblib.load("indices.pkl")

# ==========================================
# Fungsi Rekomendasi
# ==========================================
def rekomendasi_tempat(nama, top_n=5):
    if nama not in indices:
        return f"Tempat '{nama}' tidak ditemukan dalam data."
    
    idx = indices[nama]
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    rekomendasi_idx = [i[0] for i in similarity_scores[1:top_n+1]]
    
    return df[['nama_tempat', 'kategori_tempat', 'rating_pengguna']].iloc[rekomendasi_idx]

# ==========================================
# Tampilan Streamlit
# ==========================================
st.set_page_config(page_title="Rekomendasi Wisata Labuan Bajo", layout="centered")

st.title("✨ Sistem Rekomendasi Wisata Labuan Bajo")
st.write("Pilih tempat wisata yang kamu sukai, lalu dapatkan rekomendasi tempat wisata lainnya yang mirip!")

# Dropdown tempat wisata
nama_pilihan = st.selectbox("Pilih Tempat Wisata", df['nama_tempat'].sort_values().unique())

# Tampilkan rekomendasi saat tombol ditekan
if st.button("Tampilkan Rekomendasi"):
    hasil = rekomendasi_tempat(nama_pilihan)

    if isinstance(hasil, str):
        st.error(hasil)
    else:
        st.success(f"Rekomendasi mirip dengan: {nama_pilihan}")
        st.table(hasil)
