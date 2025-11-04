import streamlit as st
import os

# --- Konfigurasi Laman ---
st.set_page_config(page_title="Inovasi Pendidikan OKU (Jual Beli)", page_icon="💰", layout="centered")

# --- Gaya Tema ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1607082349566-187342375d8f?auto=format&fit=crop&w=1200&q=80");
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
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.kotak-baki {
    border: 3px solid #00897b;
    border-radius: 15px;
    background-color: #e0f2f1;
    padding: 15px;
    margin-bottom: 20px;
}
.petak-kuantiti {
    background-color: white;
    border: 3px solid #00897b;
    border-radius: 10px;
    width: 50px;
    height: 50px;
    text-align: center;
    font-weight: bold;
    font-size: 20px;
    line-height: 45px;
    margin: auto;
    color: #004d40;
}
.footer-left {
    text-align: left;
    font-style: italic;
    font-size: 14px;
    color: #444;
    margin-top: 30px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Tajuk Utama ---
st.markdown("# 🧩 Inovasi Pendidikan OKU (Jual Beli)")

# --- Semak folder gambar ---
if not os.path.exists("images"):
    st.error("❌ Folder 'images' tiada. Pastikan semua gambar duit ada dalam folder images/.")
    st.stop()

duit_images = {
    100: "rm100.jpg",
    50: "rm50.jpg",
    20: "rm20.jpg",
    10: "rm10.jpg",
    5: "rm5.jpg",
    1: "rm1.jpg",
    0.5: "sen50.jpg",
    0.2: "sen20.jpg",
    0.1: "sen10.jpg",
    0.05: "sen5.jpg"
}

# --- Pilihan peranan ---
peranan = st.radio("Pilih peranan:", ["👩‍💼 Peniaga", "🧍‍♀️ Pembeli"])
st.header(f"💵 Kalkulator {peranan.replace('👩‍💼 ', '').replace('🧍‍♀️ ', '')}")

# --- Ruangan harga barang dinamik ---
if "jumlah_barang" not in st.session_state:
    st.session_state.jumlah_barang = 1

if "harga_list" not in st.session_state:
    st.session_state.harga_list = [0.0]

def tambah_barang():
    if st.session_state.jumlah_barang < 50:
        st.session_state.jumlah_barang += 1
        st.session_state.harga_list.append(0.0)
    else:
        st.warning("⚠️ Had maksimum 50 barang telah dicapai!")

st.write("🛒 Masukkan harga setiap barang:")

# --- Input harga barang ---
for i in range(st.session_state.jumlah_barang):
    st.session_state.harga_list[i] = st.number_input(
        f"Harga Barang {i+1} (RM):", 
        min_value=0.0, 
        step=0.5, 
        key=f"harga_{i}"
    )

st.button("➕ Tambah Barang", on_click=tambah_barang)

jumlah_harga = round(sum(st.session_state.harga_list), 2)
st.info(f"💰 Jumlah Harga Keseluruhan: RM {jumlah_harga:.2f}")

# --- Input duit diberi ---
duit_diberi = st.number_input("💵 Duit Diberi (RM):", min_value=0.0, step=0.5)

# --- Butang Kira Baki ---
if st.button("Kira Baki"):
    baki = round(duit_diberi - jumlah_harga, 2)

    if baki < 0:
        st.error("❌ Duit tidak mencukupi.")
    elif baki == 0:
        st.success("✅ Tiada baki perlu diberi.")
    else:
        if peranan == "👩‍💼 Peniaga":
            st.success(f"💸 Baki perlu diberi kepada pembeli: RM {baki:.2f}")
        else:
            st.success(f"💸 Baki yang anda akan terima: RM {baki:.2f}")

        # Fungsi kira kombinasi
        def kira_kombinasi(baki, jenis=1):
            baki_sen = int(round(baki * 100))
            senarai = []
            nilai = [10000, 5000, 2000, 1000, 500, 100, 50, 20, 10, 5]  # RM2 dibuang
            if jenis == 2:
                nilai = nilai[::-1]
            elif jenis == 3:
                nilai = [5000, 1000, 500, 100, 50]
            for n in nilai:
                if baki_sen >= n:
                    bil = baki_sen // n
                    baki_sen %= n
                    senarai.append((n / 100, int(bil)))
            return senarai

        # --- Papar 3 kemungkinan ---
        for jenis in range(1, 4):
            st.markdown(f"<div class='kotak-baki'><h3>💡 Kemungkinan {jenis}</h3>", unsafe_allow_html=True)
            kombinasi = kira_kombinasi(baki, jenis)
            cols = st.columns(4)
            i = 0
            for nilai, bil in kombinasi:
                if bil > 0 and nilai in duit_images:
                    img_path = os.path.join("images", duit_images[nilai])
                    if os.path.exists(img_path):
                        with cols[i % 4]:
                            st.image(img_path, width=100, caption=f"RM{nilai:.2f}")
                            st.markdown(f"<div class='petak-kuantiti'>{bil}</div>", unsafe_allow_html=True)
                    else:
                        st.write(f"🖼️ RM{nilai:.2f} x {bil} (gambar tiada)")
                    i += 1
            st.markdown("</div>", unsafe_allow_html=True)

# --- Footer kiri ---
st.markdown("""
<div class="footer-left">
<b>Dibangunkan oleh:</b> Narjihah binti Mohd Hashim<br>
Untuk Inovasi Pendidikan Khas (Masalah Pembelajaran)
</div>
""", unsafe_allow_html=True)
