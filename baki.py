import streamlit as st
import os
import base64

# ---------------------------------------------------------
# ✅ KONFIGURASI LAMAN (TERMASUK BACKGROUND FRAME KALKULATOR)
# ---------------------------------------------------------

st.set_page_config(page_title="Inovasi Pendidikan OKU (Jual Beli)", page_icon="💰", layout="centered")

page_bg = """
<style>

[data-testid="stAppViewContainer"] {
    background: #e9f3ff;
    background-size: cover;
}

/* FRAME KALKULATOR */
.block-container {
    background: #ffffff;
    border-radius: 20px;
    padding: 25px;
    border: 4px solid #0b6bcb33;
    box-shadow: 0 10px 28px rgba(11,107,203,0.15);
}

/* Corak butang kalkulator */
.block-container:before {
    content: "";
    position: absolute;
    inset: -12px -12px auto -12px;
    height: 45px;
    background:
        radial-gradient(#d7e9ff 2px, transparent 2px) 0 0 / 18px 18px,
        radial-gradient(#d7e9ff 2px, transparent 2px) 9px 9px / 18px 18px;
    opacity: .35;
    border-top-left-radius: 26px;
    border-top-right-radius: 26px;
}

.row-duit {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}

.petak-kuantiti {
    background-color: white;
    border: 3px solid #00897b;
    border-radius: 10px;
    width: 55px;
    height: 55px;
    text-align: center;
    font-weight: bold;
    font-size: 22px;
    line-height: 49px;
    color: #004d40;
}

.kotak-baki {
    border: 3px solid #00897b;
    border-radius: 15px;
    background-color: #e0f2f1;
    padding: 15px;
    margin-bottom: 20px;
}

.resit {
    background-color: #fff3e0;
    border: 2px solid #ffb74d;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------------------------------------------------------
# ✅ TAJUK
# ---------------------------------------------------------
st.markdown("# 🧩 Inovasi Pendidikan OKU (Jual Beli)")

# ---------------------------------------------------------
# ✅ SEMAK FOLDER GAMBAR
# ---------------------------------------------------------
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
    0.05:"sen5.jpg"
}

# ---------------------------------------------------------
# ✅ PILIH PERANAN (GUNA LOGO BARU)
# ---------------------------------------------------------

st.write("### 🎭 Pilih Peranan Anda")

peranan = st.radio(
    "",
    ["🧍‍♀️ Pembeli", "👨‍🍳 Penjual"],
    horizontal=True
)

if peranan == "🧍‍♀️ Pembeli":
    st.image("images/pembeli.png", width=120)
else:
    st.image("images/penjual.png", width=120)

st.header(peranan.replace("🧍‍♀️", "").replace("👨‍🍳", "").strip())

# ---------------------------------------------------------
# ✅ INPUT HARGA BARANG
# ---------------------------------------------------------

if "jumlah_barang" not in st.session_state:
    st.session_state.jumlah_barang = 1

if "harga_list" not in st.session_state:
    st.session_state.harga_list = [0.0]

def tambah_barang():
    if st.session_state.jumlah_barang < 50:
        st.session_state.jumlah_barang += 1
        st.session_state.harga_list.append(0.0)

st.write("🛒 Masukkan harga setiap barang:")
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

# ---------------------------------------------------------
# ✅ INPUT DUIT DIBERI
# ---------------------------------------------------------

duit_diberi = st.number_input("💵 Duit Diberi (RM):", min_value=0.0, step=0.5)

# ---------------------------------------------------------
# ✅ KIRA BAKI & PAPAR 3 KEMUNGKINAN (TANPA sen5 UTAMA)
# ---------------------------------------------------------

if st.button("Kira Baki"):
    baki = round(duit_diberi - jumlah_harga, 2)

    if baki < 0:
        st.error("❌ Duit tidak mencukupi.")
        st.stop()

    elif baki == 0:
        st.success("✅ Tiada baki perlu diberi.")
        st.stop()

    # =====================================================
    # ✅ FUNGSY BARU: KEMUNGKINAN 2 & 3 TIDAK GUNA 5 SEN
    # =====================================================

    def kira_kombinasi(baki, jenis=1):
        baki_sen = int(round(baki * 100))

        # Senarai nilai RM ke sen — RM100 → RM1 → syiling
        nilai_penuh = [10000, 5000, 2000, 1000, 500, 100, 50, 20, 10]  
        nilai_dengan_5sen = nilai_penuh + [5]

        # ✅ Kemungkinan 1: sama seperti asal (termasuk 5 sen)
        if jenis == 1:
            nilai = nilai_dengan_5sen

        # ✅ Kemungkinan 2: campuran RM & syiling — TANPA 5 sen
        elif jenis == 2:
            nilai = nilai_penuh   

        # ✅ Kemungkinan 3: juga campuran, ikut ranking
        elif jenis == 3:
            nilai = nilai_penuh    

        senarai = []
        for n in nilai:
            if baki_sen >= n:
                bil = baki_sen // n
                baki_sen %= n
                senarai.append((n/100, int(bil)))

        return senarai

    # -----------------------------------------------------
    # ✅ PAPAR 3 KEMUNGKINAN
    # -----------------------------------------------------

    for jenis in range(1, 4):
        st.markdown(f"<div class='kotak-baki'><h3>💡 Kemungkinan {jenis}</h3>", unsafe_allow_html=True)
        kombinasi = kira_kombinasi(baki, jenis)

        for nilai, bil in kombinasi:
            if nilai in duit_images and bil > 0:

                img_path = os.path.join("images", duit_images[nilai])
                if os.path.exists(img_path):
                    with open(img_path, "rb") as img_file:
                        encoded = base64.b64encode(img_file.read()).decode()

                    st.markdown(
                        f"""
                        <div class='row-duit'>
                            <img src='data:image/jpeg;base64,{encoded}' width='100'>
                            <div class='petak-kuantiti'>{bil}</div>
                            <span style='font-size:18px;font-weight:bold;'>RM{nilai:.2f}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# ✅ FOOTER
# ---------------------------------------------------------

st.markdown("""
<br>
<i>Dibangunkan oleh: Narjihah binti Mohd Hashim</i><br>
<i>Inovasi Pendidikan Khas (Masalah Pembelajaran)</i>
""", unsafe_allow_html=True)
