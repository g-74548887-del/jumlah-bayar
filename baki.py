import streamlit as st
from gtts import gTTS
import base64
from io import BytesIO

# Tajuk & logo
st.image("https://upload.wikimedia.org/wikipedia/commons/7/77/Logo_Pendidikan_Khas.png", width=120)
st.title("💰 Latihan Kira Jumlah & Duit - Pendidikan Khas")
st.write("Masukkan harga setiap barang yang pelanggan nak beli:")

# Input harga barang
barang1 = st.number_input("Harga Barang 1 (RM)", min_value=0.0, step=0.1)
barang2 = st.number_input("Harga Barang 2 (RM)", min_value=0.0, step=0.1)
barang3 = st.number_input("Harga Barang 3 (RM)", min_value=0.0, step=0.1)

# Kira jumlah
total = barang1 + barang2 + barang3

if st.button("Kira Jumlah"):
    st.success(f"Jumlah Harga: RM {total:.2f}")

    # Suara automatik jumlah harga
    tts = gTTS(f"Jumlah harga ialah {total:.2f} ringgit", lang="ms")
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    audio_bytes = audio_fp.read()
    b64 = base64.b64encode(audio_bytes).decode()
    st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

    # Tunjuk duit dan kotak kuantiti
    st.write("### Duit yang perlu diberi:")
    nilai = [100, 50, 20, 10, 5, 1]
    baki = int(total)

    for n in nilai:
        bil = baki // n
        baki = baki % n
        if bil > 0:
            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(f"https://raw.githubusercontent.com/hantian123/malaysia-currency-images/main/{n}.jpg", 
                         caption=f"RM{n}", width=100)
            with col2:
                st.number_input(f"Berapa keping RM{n}?", min_value=0, max_value=10, step=1, key=f"duit{n}", value=bil)

    sen = round((total - int(total)) * 100)
    if sen > 0:
        st.write(f"**Sen:** {sen} sen")

st.write("💡 Masukkan harga dan tekan 'Kira Jumlah' untuk lihat jumlah dan duit sebenar.")
