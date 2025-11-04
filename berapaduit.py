import streamlit as st
import os

st.set_page_config(page_title="Kalkulator Duit Malaysia", layout="centered")

st.title("💰 Kalkulator Duit Malaysia (Versi Pendidikan Khas)")
st.write("Masukkan harga barang dan lihat jumlah serta gambar duit sebenar yang perlu dibayar.")

# --- Folder gambar duit ---
image_folder = "images"

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

# --- Denominasi duit dalam sen (100 sen = RM1) ---
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

# --- Bahagian input harga barang ---
st.subheader("🛒 Senarai Harga Barang")
st.caption("Masukkan harga untuk setiap barang (contoh: 5.50). Boleh isi sehingga 100 barang.")

# Buat 100 ruang input harga
harga_barang = []
for i in range(1, 101):
    value = st.text_input(f"Harga barang {i}", value="", key=f"barang_{i}")
    if value.strip() != "":
        try:
            harga_barang.append(float(value))
        except ValueError:
            st.warning(f"Harga barang {i} tidak sah. Sila masukkan nombor sahaja.")

# --- Kira jumlah keseluruhan ---
if st.button("💵 Kira Jumlah"):
    if not harga_barang:
        st.error("⚠️ Sila masukkan sekurang-kurangnya satu harga barang.")
        st.stop()

    jumlah = sum(harga_barang)
    st.success(f"Jumlah Keseluruhan: RM {jumlah:.2f}")

    # --- Tukar ke sen ---
    total_sen = int(round(jumlah * 100))

    # --- Kira pecahan duit (algoritma greedy) ---
    baki = total_sen
    hasil = []
    for nilai, label in denominations:
        keping = baki // nilai
        if keping > 0:
            hasil.append((label, keping))
            baki -= nilai * keping

    # --- Papar duit ---
    st.header("🪙 Duit yang perlu diberi:")

    for label, keping in hasil:
        col1, col2 = st.columns([1, 2])
        with col1:
            img_path = image_files.get(label)
            if img_path and os.path.exists(img_path):
                st.image(img_path, width=120)
            else:
                st.write("(Tiada gambar)")
        with col2:
            st.markdown(f"**{keping} x {label}**")
            total_label = keping * (next(v for v, l in denominations if l == label)) / 100
            st.write(f"Nilai: RM {total_label:.2f}")

    st.markdown("---")
    jumlah_kira = sum([(next(v for v, l in denominations if l == label) * keping) for label, keping in hasil]) / 100
    st.write(f"**Jumlah daripada pecahan:** RM {jumlah_kira:.2f}")

    if baki > 0:
        st.info(f"Baki kecil: {baki} sen (bulatkan jumlah).")

st.caption("💡 Aplikasi ini membantu murid Pendidikan Khas belajar nilai mata wang Malaysia.")
