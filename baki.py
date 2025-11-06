import streamlit as st
import os
import base64

# ---------------------------------------------------------
# ✅ KONFIG LAMAN + BACKGROUND FRAME KALKULATOR
# ---------------------------------------------------------

st.set_page_config(page_title="Inovasi Pendidikan OKU (Jual Beli)", page_icon="💰", layout="centered")

page_bg = """
<style>

[data-testid="stAppViewContainer"] {
    background: #e9f2ff;
}

/* ✅ FRAME KALKULATOR BESAR */
.block-container {
    background: #ffffff;
    border-radius: 25px;
    padding: 30px;
    border: 5px solid #0b6bcb66;
    box-shadow: 0 0 25px rgba(0,80,160,0.25);
    position: relative;
}

/* ✅ CORAK BUTANG KALKULATOR ATAS FRAME */
.block-container:before {
    content: "";
    position: absolute;
    inset: -15px -15px auto -15px;
    height: 55px;
    background:
        radial-gradient(#d4e5ff 3px, transparent 2px) 0 0 / 22px 22px,
        radial-gradient(#d4e5ff 3px, transparent 2px) 11px 11px / 22px 22px;
    opacity: .45;
    border-top-left-radius: 30px;
    border-top-right-radius: 30px;
}

/* ✅ STYLE PAPARAN DUIT */
.row-duit {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 12px;
}

.petak-kuantiti {
    background-color: white;
    border: 3px solid #00897b;
    border-radius: 12px;
    width: 65px;
    height: 65px;
    text-align: center;
    font-weight: bold;
    font-size: 26px;
    line-height: 58px;
    color: #004d40;
}

.kotak-baki {
    border: 3.5px solid #00897b;
    border-radius: 18px;
    background-color: #e0f2f1;
    padding: 18px;
    margin-bottom: 25px;
}

.resit {
    background-color: #fff3e0;
    border: 3px solid #ffb74d;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 25px;
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
    st.error("❌ Folder 'images' tiada.")
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


# ---------------------------------------------------------
# ✅ PILIH PERANAN (GUNA LOGO BESAR)
# ---------------------------------------------------------

st.write("### 🎭 Pilih Peranan")

peranan = st.radio("", ["🧍‍♀️ Pembeli", "👨‍🍳 Penjual"], horizontal=True)

if peranan == "🧍‍♀️ Pembeli":
    st.image("images/pembeli.png", width=180)
else:
    st.image("images/penjual.png", width=180)

st.header(peranan.replace("🧍‍♀️", "").replace("👨‍🍳", "").strip())


# ---------------------------------------------------------
# ✅ INPUT HARGA BARANG
# ---------------------------------------------------------

if "jumlah_barang" not in st.session_state:
    st.session_state.jumlah_barang = 1

if "harga_list" not in st.session_state:
    st.session_state.harga_list = [0.0]

def tambah_barang():
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
# ✅ 3 KEMUNGKINAN PECAHAN DUIT—TERMASUK KEMUNGKINAN 3 BARU
# ---------------------------------------------------------

def kira_kombinasi(baki, jenis):
    baki_sen = int(round(baki * 100))

    nilai_RM_besar = [10000, 5000, 2000]   # RM100 RM50 RM20
    nilai_RM_kecil = [1000, 500, 100]      # RM10 RM5 RM1
    syiling = [50, 20, 10]                 # sen50 sen20 sen10
    syiling_dgn_5 = [50, 20, 10, 5]

    kombinasi = []

    # ✅ KEMUNGKINAN 1 — Greedy normal (termasuk 5 sen)
    if jenis == 1:
        nilai = nilai_RM_besar + nilai_RM_kecil + syiling_dgn_5

    # ✅ KEMUNGKINAN 2 — RM besar 1 keping + syiling tanpa 5 sen
    elif jenis == 2:
        for n in nilai_RM_besar:
            if baki_sen >= n:
                kombinasi.append((n/100, 1))
                baki_sen -= n
        nilai = syiling

    # ✅ KEMUNGKINAN 3 — RM10 banyak + RM kecil + syiling
    elif jenis == 3:

        # RM10 banyak
        while baki_sen >= 1000:
            kombinasi.append((10, 1))
            baki_sen -= 1000

        # RM5
        if baki_sen >= 500:
            kombinasi.append((5, 1))
            baki_sen -= 500

        # RM1
        if baki_sen >= 100:
            bil = baki_sen // 100
            baki_sen %= 100
            kombinasi.append((1, bil))

        # Syiling (tanpa 5 sen)
        for n in syiling:
            if baki_sen >= n:
                bil = baki_sen // n
                baki_sen %= n
                kombinasi.append((n/100, bil))

        # sen5 hanya jika wajib
        if baki_sen >= 5:
            kombinasi.append((0.05, 1))
            baki_sen -= 5

        return kombinasi

    # (Untuk Kemungkinan 1 & 2)
    for n in nilai:
        if baki_sen >= n:
            bil = baki_sen // n
            baki_sen %= n
            kombinasi.append((n/100, int(bil)))

    return kombinasi


# ---------------------------------------------------------
# ✅ PAPARKAN 3 KEMUNGKINAN
# ---------------------------------------------------------

if st.button("Kira Baki"):
    baki = round(duit_diberi - jumlah_harga, 2)

    if baki < 0:
        st.error("❌ Duit tidak mencukupi.")
        st.stop()
    elif baki == 0:
        st.success("✅ Tiada baki diperlukan.")
        st.stop()

    # Resit ringkas
    st.markdown("""
    <div class='resit'>
    <h3>🧾 Resit Mini</h3>
    </div>
    """, unsafe_allow_html=True)
    st.write(f"Jumlah Harga: RM {jumlah_harga:.2f}")
    st.write(f"Duit Diberi: RM {duit_diberi:.2f}")
    st.write(f"Baki: RM {baki:.2f}")

    # 3 kombinasi
    for jenis in [1, 2, 3]:
        st.markdown(
            f"<div class='kotak-baki'><h3>💡 Kemungkinan {jenis}</h3>",
            unsafe_allow_html=True
        )

        kombinasi = kira_kombinasi(baki, jenis)

        for nilai, bil in kombinasi:
            img_name = duit_images.get(nilai)

            if img_name and bil > 0:
                path = f"images/{img_name}"

                if os.path.exists(path):
                    with open(path, "rb") as f:
                        encoded = base64.b64encode(f.read()).decode()

                    st.markdown(
                        f"""
                        <div class='row-duit'>
                            <img src='data:image/jpeg;base64,{encoded}' width='110'>
                            <div class='petak-kuantiti'>{bil}</div>
                            <span style='font-size:20px;font-weight:bold;'>RM{nilai:.2f}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# ✅ FOOTER
# ---------------------------------------------------------

st.markdown("""
<br><br>
<i>Dibangunkan oleh: Narjihah binti Mohd Hashim</i><br>
<i>Inovasi Pendidikan Khas (Masalah Pembelajaran)</i>
""", unsafe_allow_html=True)
