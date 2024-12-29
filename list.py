import streamlit as st

# Inisialisasi data awal stok obat
if 'stok_obat' not in st.session_state:
    st.session_state.stok_obat = {
        "Maag": [
            {"nama": "Promag", "stok": 10000, "harga": 150000},
            {"nama": "Polysilane", "stok": 12000, "harga": 200000},
            {"nama": "Mylanta", "stok": 15000, "harga": 180000},
        ],
        "Demam": [
            {"nama": "Paracetamol", "stok": 5000, "harga": 120000},
            {"nama": "Ibuprofen", "stok": 8000, "harga": 150000},
            {"nama": "Panadol", "stok": 6000, "harga": 170000},
        ],
        "Batuk": [
            {"nama": "Hufagrip", "stok": 15000, "harga": 100000},
            {"nama": "Woods", "stok": 14000, "harga": 120000},
            {"nama": "Komix", "stok": 5000, "harga": 140000},
        ],
    }

st.title("Aplikasi Kasir Stok Obat")

# Input penyakit untuk menampilkan obat yang relevan
penyakit = st.selectbox("Pilih penyakit:", ["Maag", "Demam", "Batuk"])

# Tampilkan informasi obat berdasarkan penyakit yang dipilih
if penyakit:
    st.write(f"*Daftar Obat untuk {penyakit}:*")
    for index, obat in enumerate(st.session_state.stok_obat[penyakit]):
        st.write(f"### {index + 1}. {obat['nama']}")
        st.write(f"- Harga: Rp {obat['harga']}")
        st.write(f"- Stok tersedia: {obat['stok']}")

        # Tampilkan status ketersediaan
        if obat['stok'] > 0:
            st.success("Obat tersedia.")
            # Input jumlah pembelian
            jumlah = st.number_input(f"Masukkan jumlah yang telah dibeli untuk {obat['nama']}:", min_value=0, max_value=obat['stok'], step=1, key=f"{penyakit}_{index}")

            if st.button(f"Kurangi Stok {obat['nama']}", key=f"btn_{penyakit}_{index}"):
                if jumlah > 0:
                    obat['stok'] -= jumlah
                    st.success(f"Stok {obat['nama']} berhasil dikurangi sebanyak {jumlah}. Sisa stok: {obat['stok']}.")
                else:
                    st.warning("Masukkan jumlah yang valid untuk pembelian.")
        else:
            st.error("Obat tidak tersedia.")

# Tampilkan daftar stok secara keseluruhan
st.write("\n### Daftar Stok Obat Keseluruhan")
st.table([
    {"Penyakit": penyakit, "Nama Obat": obat["nama"], "Stok": obat["stok"], "Harga (Rp)": obat["harga"]}
    for penyakit, daftar_obat in st.session_state.stok_obat.items()
    for obat in daftar_obat
])
