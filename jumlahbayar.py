import streamlit as st

st.set_page_config(page_title="Kalkulator Duit Malaysia", layout="centered")

st.title("💰 Kalkulator Duit Malaysia (Versi Pendidikan Khas)")
st.write("Masukkan jumlah harga dan tekan **Kira Jumlah** untuk lihat duit sebenar yang perlu diberi.")

# --- Input jumlah harga ---
jumlah_input = st.text_input("Masukkan Jumlah (contoh: 9.50)", value="")

# --- Butang kira ---
if st.button("Kira Jumlah"):
    try:
        jumlah_rm = float(jumlah_input)
    except:
        st.error("⚠️ Sila masukkan nombor yang sah, contoh: 12.30")
        st.stop()

    total_sen = int(round(jumlah_rm * 100))
    st.success(f"Jumlah Harga: RM {jumlah_rm:.2f}")

    # --- Senarai nilai duit ---
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

    # --- Gambar dari internet (Wikipedia Commons) ---
    image_urls = {
        "RM100": "https://upload.wikimedia.org/wikipedia/commons/8/8b/MYR100_obverse_and_reverse_2012.jpg",
        "RM50": "https://upload.wikimedia.org/wikipedia/commons/7/73/MYR50_obverse_and_reverse_2012.jpg",
        "RM20": "https://upload.wikimedia.org/wikipedia/commons/3/32/MYR20_obverse_and_reverse_2012.jpg",
        "RM10": "https://upload.wikimedia.org/wikipedia/commons/4/48/MYR10_obverse_and_reverse_2012.jpg",
        "RM5": "https://upload.wikimedia.org/wikipedia/commons/5/57/MYR5_obverse_and_reverse_2012.jpg",
        "RM1": "https://upload.wikimedia.org/wikipedia/commons/8/85/MYR1_obverse_and_reverse_2012.jpg",
        "50 sen": "https://upload.wikimedia.org/wikipedia/commons/a/ae/Malaysian_50_sen_coin_2012.jpg",
        "20 sen": "https://upload.wikimedia.org/wikipedia/commons/3/37/Malaysian_20_sen_coin_2012.jpg",
        "10 sen": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Malaysian_10_sen_coin_2012.jpg",
        "5 sen": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Malaysian_5_sen_coin_2012.jpg",
    }

    # --- Kira pecahan duit (greedy algorithm) ---
    baki = total_sen
    hasil = []
    for nilai, label in denominations:
        keping = baki // nilai
        if keping > 0:
            hasil.append((label, keping))
            baki -= nilai * keping

    # --- Papar keputusan ---
    st.header("Duit yang perlu diberi 💵")

    for label, keping in hasil:
        col1, col2 = st.columns([1, 2])
        with col1:
            url = image_urls.get(label, None)
            if url:
                st.image(url, use_column_width=True)
            else:
                st.write("(Tiada gambar)")
        with col2:
            st.markdown(f"**{keping} x {label}**")
            nilai = 0
            for v, l in denominations:
                if l == label:
                    nilai = v
                    break
            total_label = nilai * keping / 100
            st.write(f"Nilai: RM {total_label:.2f}")

    st.markdown("---")
    jumlah_kira = sum([(v * c) for v, l in denominations for x, c in hasil if l == x]) / 100
    st.write(f"**Jumlah daripada pecahan:** RM {jumlah_kira:.2f}")

    if baki > 0:
        st.info(f"Baki kecil: {baki} sen (bulatkan jumlah atau abaikan)")

st.caption("💡 Kod ini sesuai untuk latihan mata wang Malaysia bagi murid Pendidikan Khas. Gambar digunakan dari sumber Wikipedia Commons.")


import streamlit as st
import os

# Folder gambar
image_folder = "images"

# Gambar duit Malaysia
image_urls = {
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

