import streamlit as st


OBAT = {
    "Demam": {"Paracetamol": 5000, "Ibuprofen": 8000, "Panadol": 6000},
    "Batuk": {"Hufagrip": 15000, "Woods": 14000, "Komix": 5000},
    "Maag": {"Promag": 10000, "Polysilane": 12000, "Mylanta": 15000},
}

# Inisialisasi state
if "pesanan" not in st.session_state:
    st.session_state.pesanan = {}

# Layout utama dengan sidebar
st.set_page_config(page_title="E-Apotik", layout="wide")
st.sidebar.title("Pengguna")
menu = st.sidebar.radio("Pilih Halaman:", ["Beranda", "Pemesanan", "Pembayaran"])

# 1. Halaman Beranda
if menu == "Beranda":
    st.title("Selamat Datang di E-Apotik!")
    st.markdown("""
        Aplikasi E-Apotik mempermudah Anda dalam mencari dan memesan obat. 
        Navigasikan melalui menu di sebelah kiri untuk memilih kategori:
        - Pemesanan: Memilih obat berdasarkan kategori.
        - Pembayaran: Menyelesaikan pembayaran.
    """)

# 2. Halaman Pemesanan
elif menu == "Pemesanan":
    st.title("Pilih Obat Sesuai Kebutuhan Anda")
    
    # Memilih kategori obat
    kategori = st.selectbox("Pilih Kategori Penyakit:", ["", "Demam", "Batuk", "Maag"])

    if kategori:
        obat = st.selectbox("Pilih Obat:", [""] + list(OBAT[kategori].keys()))
        
        if obat:
            jumlah = st.number_input(f"Jumlah untuk {obat}:", min_value=1, step=1)
            alamat = st.text_area("Masukkan Alamat Pengiriman:", placeholder="Alamat lengkap Anda...")
            
            if st.button("Tambahkan ke Keranjang"):
                if alamat == "":
                    st.error("Alamat pengiriman harus diisi!")
                else:
                    if obat in st.session_state.pesanan:
                        st.session_state.pesanan[obat]["jumlah"] += jumlah
                    else:
                        st.session_state.pesanan[obat] = {"jumlah": jumlah, "alamat": alamat}
                    st.success(f"{obat} sebanyak {jumlah} telah ditambahkan ke pesanan. Alamat pengiriman: {alamat}")

# 3. Halaman Pembayaran
elif menu == "Pembayaran":
    st.title("Proses Pembayaran")
    if not st.session_state.pesanan:
        st.warning("Tidak ada item di pesanan. Silakan lakukan pemesanan terlebih dahulu.")
    else:
        total_harga = 0
        total_item = 0
        for obat, details in st.session_state.pesanan.items():
            jumlah = details["jumlah"]
            harga = [v for penyakit in OBAT.values() for k, v in penyakit.items() if k == obat][0]
            subtotal = jumlah * harga
            total_harga += subtotal
            total_item += jumlah
            st.write(f"- {obat} (x{jumlah}): Rp{subtotal:,}")
            st.write(f"Alamat pengiriman: {details['alamat']}")
        
        st.write(f"Total Harga: Rp{total_harga:,}")
        
        # Menambahkan pajak 22% jika pembelian lebih dari 10 item
        pajak_persen = 12  # Pajak 22% untuk operator
        pajak = 0
        if total_item > 0:  # Jika membeli lebih dari 10 item
            pajak = (pajak_persen / 100) * total_harga
            st.write(f"Pajak (12%): Rp{pajak:,}")
        
        total_setelah_pajak = total_harga + pajak

        st.write(f"Total setelah Pajak: Rp{total_setelah_pajak:,}")
        
        e_money = st.selectbox("Pilih Jenis E-Money:", ["", "OVO", "GoPay", "DANA"])
        nomor = st.number_input("Masukkan nomor {e_money} anda: ")
        
        # Input untuk memasukkan PIN
        pin = st.text_input("Masukkan PIN Anda:", type="password")
        
        # Setelah PIN dimasukkan, baru tampilkan input untuk pembayaran
        if pin and len(pin) >= 6:

            # Input untuk memasukkan nominal pembayaran
            jumlah_bayar = st.number_input("Masukkan jumlah pembayaran:", min_value=0)
            
            if st.button("Bayar"):
                if jumlah_bayar == total_setelah_pajak:
                    if not e_money:
                        st.error("Pilih jenis e-money terlebih dahulu.")
                    else:
                        alamat_pengiriman = ", ".join([details["alamat"] for details in st.session_state.pesanan.values()])
                        st.success(f"Pembayaran berhasil menggunakan {e_money}! Terima kasih telah menggunakan E-Apotik, semoga lekas sembuh. Pemesanan Anda akan segera dikirim ke alamat: {alamat_pengiriman}.")
                        st.session_state.pesanan.clear()
                elif jumlah_bayar < total_setelah_pajak:
                    st.error("Jumlah pembayaran kurang.")
                else:
                    st.warning("Nominal pembayaran melebihi total harga.")
        else:
            st.warning("Masukkan PIN terlebih dahulu (minimal 6 digit).")