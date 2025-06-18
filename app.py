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
    return df.iloc[rekomendasi_idx]

# ==========================================
# Tampilan Streamlit
# ==========================================
st.set_page_config(page_title="Rekomendasi Wisata Labuan Bajo", layout="wide")

st.title("🏝️ Sistem Rekomendasi Wisata Labuan Bajo")
st.write("Pilih destinasi favoritmu, lalu sistem akan merekomendasikan tempat wisata lain yang mirip! ✨")

# Dropdown tempat wisata
nama_pilihan = st.selectbox("📍 Pilih Tempat Wisata", df['nama_tempat'].sort_values().unique())

# Tampilkan rekomendasi saat tombol ditekan
if st.button("🎯 Tampilkan Rekomendasi"):
    hasil = rekomendasi_tempat(nama_pilihan)
    
    if isinstance(hasil, str):
        st.error(hasil)
    else:
        st.success(f"Berikut rekomendasi tempat wisata mirip dengan: **{nama_pilihan}**")

        for _, row in hasil.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(row['gambar_tempat'], width=200, caption=row['nama_tempat'])
                with col2:
                    st.markdown(f"### {row['nama_tempat']}")
                    st.markdown(f"**Kategori:** {row['kategori_tempat']}")
                    st.markdown(f"**Rating Pengguna:** ⭐ {row['rating_pengguna']}")
                    if pd.notnull(row['link_google_maps']):
                        st.markdown(f"[🗺️ Lihat di Google Maps]({row['link_google_maps']})", unsafe_allow_html=True)
                st.markdown("---")
