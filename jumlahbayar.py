# streamlit_app.py
import streamlit as st
from math import floor

st.set_page_config(page_title="Pengira Duit (Gambar dari Internet)", layout="centered")

st.title("Pengiraan Duit — Papar Gambar Duit dari Internet")
st.write("Masukkan jumlah harga (contoh: 9.50) dan tekan 'Kira Jumlah'.")

# input jumlah (float)
jumlah_input = st.text_input("Jumlah (RM)", value="9.50")
if st.button("Kira Jumlah"):
    # --- step-by-step arithmetic: convert to sen (cents) as integer ---
    try:
        jumlah_rm = float(jumlah_input)
    except:
        st.error("Sila masukkan nombor yang sah (contoh: 9.50).")
        st.stop()

    # convert to sen (integer) to avoid floating point issues
    total_sen = int(round(jumlah_rm * 100))

    st.success(f"Jumlah Harga: RM {jumlah_rm:.2f}")

    # Denominations in sen (1 RM = 100 sen)
    # Notes and coins commonly used: RM100,50,20,10,5,1; coins: 50,20,10,5 sen
    denom_list = [
        (10000, "RM100"),
        (5000,  "RM50"),
        (2000,  "RM20"),
        (1000,  "RM10"),
        (500,   "RM5"),
        (100,   "RM1"),
        (50,    "50 sen"),
        (20,    "20 sen"),
        (10,    "10 sen"),
        (5,     "5 sen"),
    ]

    # Map denomination label -> image URL (internet). 
    # NOTE: If any URL fails to load, replace it with another working URL.
    image_urls = {
        "RM100": "https://upload.wikimedia.org/wikipedia/commons/8/8b/MYR100_banknote.jpg",
        "RM50":  "https://upload.wikimedia.org/wikipedia/commons/7/7a/MYR50_banknote.jpg",
        "RM20":  "https://upload.wikimedia.org/wikipedia/commons/1/12/MYR20_banknote.jpg",
        "RM10":  "https://upload.wikimedia.org/wikipedia/commons/3/37/MYR10_banknote.jpg",
        "RM5":   "https://upload.wikimedia.org/wikipedia/commons/4/4a/MYR5_banknote.jpg",
        "RM1":   "https://upload.wikimedia.org/wikipedia/commons/6/65/MYR1_banknote.jpg",
        "50 sen":"https://upload.wikimedia.org/wikipedia/commons/2/26/MYR50sen_coin.jpg",
        "20 sen":"https://upload.wikimedia.org/wikipedia/commons/5/5b/MYR20sen_coin.jpg",
        "10 sen":"https://upload.wikimedia.org/wikipedia/commons/6/60/MYR10sen_coin.jpg",
        "5 sen": "https://upload.wikimedia.org/wikipedia/commons/9/95/MYR5sen_coin.jpg",
    }

    # compute greedy decomposition
    result = []
    remaining = total_sen
    for value, label in denom_list:
        count = remaining // value
        if count > 0:
            result.append((label, count))
            remaining -= count * value

    # If there is leftover less than 5 sen (e.g., 1-4 sen) handle as info (Malaysia rarely uses 1 sen)
    if remaining > 0:
        # show rounding note
        st.info(f"Terdapat baki {remaining} sen yang kurang daripada denominasi terkecil dalam senarai (5 sen). "
                "Anda boleh bulatkan atau beri eWallet. (Baki ditunjukkan di bawah).")

    st.subheader("Duit yang perlu diberi:")

    # display each with image and caption in columns
    for label, count in result:
        # create a small card-like layout: image + caption + text
        cols = st.columns([1, 3])
        img_url = image_urls.get(label)
        with cols[0]:
            if img_url:
                # width disesuaikan untuk paparan telefon vs desktop
                try:
                    st.image(img_url, width=100)
                except Exception as e:
                    # fallback: kalau image load gagal, tunjuk teks
                    st.write(f"(Gambar {label} tak boleh dimuat)")
            else:
                st.write(f"(Tiada URL gambar untuk {label})")
        with cols[1]:
            st.write(f"**{count} x {label}**")
            # tunjuk nilai jumlah untuk pendidikan murid
            # convert label to sen to compute displayed RM value
            # remove non-digits to compute numeric value
            # But simpler: show total value of that denom:
            # find denom value from denom_list dict
            denom_value = None
            for v,l in denom_list:
                if l == label:
                    denom_value = v
                    break
            if denom_value is not None:
                total_value_rm = (denom_value * count) / 100.0
                st.write(f"Nilai: RM {total_value_rm:.2f}")

    # show leftover (if any)
    if remaining > 0:
        st.write(f"Baki (sen): {remaining} sen")

    # final check: recompute total from decomposition
    recomputed_sen = sum(( (next(v for v,l in denom_list if l==label) * count) for label, count in result ))
    recomputed_rm = recomputed_sen / 100.0
    st.write("---")
    st.write(f"Jumlah daripada pecahan: RM {recomputed_rm:.2f}")

    # helpful note for teacher
    st.caption("Jika mana-mana gambar tidak keluar, gantikan URL di `image_urls` dengan link gambar yang sah (contoh: Wikimedia Commons).")
