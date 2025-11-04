import streamlit as st
import os

st.set_page_config(page_title="Kalkulator Duit Malaysia", layout="centered")

st.title("💰 Kalkulator Duit Malaysia (Versi Pendidikan Khas)")
st.write("Masukkan harga barang satu per satu dan lihat jumlah serta gambar duit sebenar yang perlu dibayar.")

# Folder gambar
image_folder = "images"

# Pastikan folder wujud
if not os.path.exists(image_folder):
    st.error("❌ Folder 'images' tidak dijumpai. Pastikan semua gambar duit ada dalam folder 'images'.")
    st.stop()

# Peta nama duit ke fail gambar
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

# Denominasi duit dalam sen
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

# Guna session_state untuk simpan bilangan barang
if "bil_barang" not in st.session_state:
    st.session_state.bil_barang = 1

st.subheader("🛒 Senarai Harga Barang")

# Butang tambah barang
col_tambah, col_reset = st.columns([1,1])
with col_tambah:
    if st.button("➕ Tambah Barang"):
        if st.session_state.bil_barang < 100:
            st.session_state.bil_barang += 1
        else:
            st.warning("Maksimum 100 barang sahaja.")
with col_reset:
    if st.button("♻️ Padam Semua"):
        st.session_state.bil_barang = 1

# Input harga barang mengikut bilangan
harga_barang = []
for i in range(1, st.session_state.bil_barang + 1):
    val = st.text_input(f"Harga barang {i}", value="", key=f"barang_{i}")
    if val.strip() != "":
        try:
            harga_barang.append(float(val))
        except ValueError:
            st.warning(f"Harga barang {i} tidak sah. Sila masukkan nombor.")

# Butang kira jumlah
if st.button("💵 Kira Jumlah"):
    if not harga_barang:
        st.error("⚠️ Sila masukkan sekurang-kurangnya satu harga.")
        st.stop()

    jumlah = sum(harga_barang)
    st.success(f"Jumlah Keseluruhan: RM {jumlah:.2f}")

    total_sen = int(round(jumlah * 100))

    # Kira pecahan duit
    baki = total_sen
    hasil = []
    for nilai, label in denominations:
        keping = baki // nilai
        if keping > 0:
            hasil.append((label, keping))
            baki -= nilai * keping

    # Papar gambar duit
    st.header("🪙 Duit yang perlu diberi:")

    for label, keping in hasil:
        col1, col2 = st.columns([1, 2])
        with col1:
            img_path = image_files.get(label)
            if img_path and os.path.exists(img_path):
                # Pastikan Streamlit baca gambar dari folder betul
                st.image(img_path, width=120)
            else:
                st.warning(f"(Gambar untuk {label} tiada)")
        with col2:
            st.markdown(f"**{keping} x {label}**")
            total_label = keping * (next(v for v, l in denominations if l == label)) / 100
            st.write(f"Nilai: RM {total_label:.2f}")

    st.markdown("---")
    jumlah_kira = sum([(next(v for v, l in denominations if l == label) * keping)
                       for label, keping in hasil]) / 100
    st.write(f"**Jumlah daripada pecahan:** RM {jumlah_kira:.2f}")

    if baki > 0:
        st.info(f"Baki kecil: {baki} sen (bulatkan jumlah).")

st.caption("💡 Tekan 'Tambah Barang' untuk tambah ruang harga baru (maksimum 100). Semua gambar duit diambil dari folder tempatan 'images/'.")
