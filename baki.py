import streamlit as st
import os

st.set_page_config(page_title="Kalkulator Duit Malaysia", layout="centered")

st.title("💰 Kalkulator Duit Malaysia (Pendidikan Khas)")
st.write("Pilih sama ada anda sebagai **peniaga** atau **pembeli**.")

# Folder gambar
image_folder = "images"
if not os.path.exists(image_folder):
    st.error("❌ Folder 'images' tiada. Pastikan semua gambar duit ada dalam folder images/")
    st.stop()

# Senarai gambar duit
image_files = {
    "RM100": os.path.join(image_folder, "rm100.jpg"),
    "RM50": os.path.join(image_folder, "rm50.jpg"),
    "RM20": os.path.join(image_folder, "rm20.jpg"),
    "RM10": os.path.join(image_folder, "rm10.jpg"),
    "RM5": os.path.join(image_folder, "rm5.jpg"),
    "RM1": os.path.join(image_folder, "rm1.jpg"),
    "50 sen": os.path.join(image_folder, "sen50.jpg"),
    "20 sen": os.path.join(image_folder, "sen20.jpg"),
    "10 sen": os.path.join(image_folder, "sen10.jpg"),
    "5 sen": os.path.join(image_folder, "sen5.jpg"),
}

# Denominasi dalam sen
denominations = [
    (10000, "RM100"),
    (5000, "RM50"),
    (2000, "RM20"),
    (1000, "RM10"),
    (500, "RM5"),
    (100, "RM1"),
    (50, "50 sen"),
    (20, "20 sen"),
    (10, "10 sen"),
    (5, "5 sen"),
]

# Fungsi kira baki dan paparkan gambar
def papar_gambar_duit(jumlah_sen):
    hasil = []
    baki = jumlah_sen
    for nilai, label in denominations:
        keping = baki // nilai
        if keping > 0:
            hasil.append((label, keping))
            baki -= nilai * keping

    # Paparkan gambar
    for label, keping in hasil:
        img_path = image_files.get(label)
        if os.path.exists(img_path):
            cols = st.columns(min(keping, 5))  # max 5 gambar satu baris
            idx = 0
            for i in range(keping):
                with cols[idx]:
                    st.image(img_path, width=100)
                idx += 1
                if idx >= 5:
                    cols = st.columns(min(keping - i, 5))
                    idx = 0
        st.write(f"**{keping} x {label}**")
    if baki > 0:
        st.info(f"Ada baki kecil: {baki} sen")

# Pilihan utama
mode = st.radio("Pilih peranan:", ["🧑‍🍳 Peniaga", "🧍‍♀️ Pembeli"])

st.markdown("---")

# Bilangan barang dinamik
if "bil_barang" not in st.session_state:
    st.session_state.bil_barang = 1

col1, col2 = st.columns([1,1])
with col1:
    if st.button("➕ Tambah Barang"):
        if st.session_state.bil_barang < 100:
            st.session_state.bil_barang += 1
        else:
            st.warning("Maksimum 100 barang sahaja.")
with col2:
    if st.button("♻️ Padam Semua"):
        st.session_state.bil_barang = 1

harga_barang = []
for i in range(1, st.session_state.bil_barang + 1):
    harga = st.text_input(f"Harga barang {i} (RM)", key=f"barang_{i}")
    if harga.strip() != "":
        try:
            harga_barang.append(float(harga))
        except ValueError:
            st.warning(f"Harga barang {i} tidak sah.")

# Jumlah harga barang
jumlah_barang = sum(harga_barang) if harga_barang else 0.0

st.write(f"**Jumlah harga semua barang:** RM {jumlah_barang:.2f}")

# Input jumlah duit diberi
duit_diberi = st.number_input("Masukkan jumlah duit diberi (RM)", min_value=0.0, step=0.1)

# ==========================
#   MODE PENIAGA
# ==========================
if mode == "🧑‍🍳 Peniaga":
    st.subheader("🧑‍🍳 Mod Peniaga: Kira baki yang perlu diberi kepada pelanggan")
    if st.button("💵 Kira Baki (Peniaga)"):
        baki = duit_diberi - jumlah_barang
        if baki < 0:
            st.error("❌ Duit pelanggan tak cukup!")
        else:
            st.success(f"Baki yang perlu diberi: RM {baki:.2f}")
            st.write("🪙 Duit baki yang perlu diberi:")
            papar_gambar_duit(int(round(baki * 100)))

# ==========================
#   MODE PEMBELI
# ==========================
if mode == "🧍‍♀️ Pembeli":
    st.subheader("🧍‍♀️ Mod Pembeli: Kira baki yang akan diterima daripada peniaga")
    if st.button("💰 Kira Baki (Pembeli)"):
        baki = duit_diberi - jumlah_barang
        if baki < 0:
            st.error("❌ Duit anda tak cukup!")
        else:
            st.success(f"Baki yang akan diterima: RM {baki:.2f}")
            st.write("🪙 Duit baki yang anda akan dapat:")
            papar_gambar_duit(int(round(baki * 100)))

st.markdown("---")
st.caption("💡 Tekan 'Tambah Barang' untuk tambah harga barang baru. Maksimum 100 barang. Semua gambar duit diambil dari folder 'images/'.")
