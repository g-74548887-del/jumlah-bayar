import streamlit as st
import os

# --- Konfigurasi Laman ---
st.set_page_config(page_title="Inovasi Pendidikan OKU (Jual Beli)", page_icon="💰", layout="centered")

# --- Gaya CSS Tema Jual Beli ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1607082349566-187342375d8f?auto=format&fit=crop&w=1000&q=80");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
h1, h2, h3, h4, h5, h6, p, span {
    color: #2b2b2b !important;
    text-shadow: 0px 1px 2px rgba(255,255,255,0.8);
}
.block-container {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Tajuk & Kredit ---
st.markdown("""
# 🧩 Inovasi Pendidikan OKU (Jual Beli)
### Dibangunkan oleh **Narjihah binti Mohd Hashim**
---
""")

# --- Semak folder images ---
if not os.path.exists("images"):
    st.error("❌ Folder 'images' tiada. Pastikan semua gambar duit ada dalam folder images/.")
    st.stop()

# --- Senarai nilai duit dan nama fail ---
duit_images = {
    100: "rm100.jpg",
    50: "rm50.jpg",
    20: "rm20.jpg",
    10: "rm10.jpg",
    5: "rm5.jpg",
    2: "rm2.jpg",
    1: "rm1.jpg",
    0.5: "sen50.jpg",
    0.2: "sen20.jpg",
    0.1: "sen10.jpg",
    0.05: "sen5.jpg"
}

# --- Input utama ---
st.header("💵 Kalkulator Jual Beli")
st.write("Masukkan jumlah harga barang dan duit diberi oleh pelanggan.")

duit_diberi = st.number_input("💰 Duit Diberi (RM):", min_value=0.0, step=0.5)
harga_barang = st.number_input("🛍️ Jumlah Harga Barang (RM):", min_value=0.0, step=0.5)

if st.button("Kira Baki"):
    baki = round(duit_diberi - harga_barang, 2)

    if baki < 0:
        st.error("❌ Duit tidak mencukupi.")
    elif baki == 0:
        st.success("✅ Tiada baki perlu diberi.")
    else:
        st.success(f"💸 Jumlah baki: RM {baki:.2f}")

        # Fungsi kira baki (3 jenis gaya)
        def kira_kombinasi(baki, jenis=1):
            baki_sen = int(round(baki * 100))
            senarai = []
            nilai = [10000, 5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5]
            if jenis == 2:
                nilai = nilai[::-1]  # guna duit kecil dulu
            elif jenis == 3:
                nilai = [5000, 2000, 1000, 500, 200, 100, 50]  # campur besar + kecil

            for n in nilai:
                if baki_sen >= n:
                    bil = baki_sen // n
                    baki_sen %= n
                    senarai.append((n / 100, int(bil)))
            return senarai

        # Papar 3 kemungkinan
        for jenis in range(1, 4):
            st.markdown(f"### 💡 Kemungkinan {jenis}")
            kombinasi = kira_kombinasi(baki, jenis)
            cols = st.columns(5)
            i = 0
            for nilai, bil in kombinasi:
                if bil > 0 and nilai in duit_images:
                    img_path = os.path.join("images", duit_images[nilai])
                    if os.path.exists(img_path):
                        with cols[i % 5]:
                            st.image(img_path, width=100, caption=f"{bil} × RM{nilai:.2f}")
                    else:
                        st.write(f"🖼️ {bil} × RM{nilai:.2f} (gambar tiada)")
                    i += 1
