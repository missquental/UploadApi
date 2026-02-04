import streamlit as st
import requests
from io import BytesIO
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="Video Upload via API",
    page_icon="🎥",
    layout="centered"
)

# Judul aplikasi
st.title("📤 Upload Video via API")
st.markdown("---")

# Informasi API endpoint
API_URL = "https://live.streamlit.app/api/upload"  # Ganti dengan URL API yang sesuai

# File uploader untuk video
uploaded_file = st.file_uploader(
    "Pilih file video untuk diupload",
    type=["mp4", "avi", "mov", "mkv", "webm"],
    accept_multiple_files=False
)

if uploaded_file is not None:
    # Menampilkan informasi file
    file_details = {
        "Nama File": uploaded_file.name,
        "Tipe File": uploaded_file.type,
        "Ukuran File": f"{uploaded_file.size / (1024*1024):.2f} MB"
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Informasi File")
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")
    
    with col2:
        st.subheader("Preview")
        st.video(uploaded_file)
        
    # Tombol upload
    if st.button("📤 Upload ke API", type="primary"):
        try:
            with st.spinner("Mengupload video... Mohon tunggu"):
                # Membaca konten file
                file_content = uploaded_file.read()
                
                # Mempersiapkan file untuk dikirim
                files = {
                    'file': (
                        uploaded_file.name,
                        BytesIO(file_content),
                        uploaded_file.type
                    )
                }
                
                # Mengirim request ke API
                response = requests.post(
                    API_URL,
                    files=files,
                    timeout=300  # Timeout 5 menit
                )
                
                # Memeriksa respons
                if response.status_code == 200:
                    st.success("✅ Video berhasil diupload!")
                    st.json(response.json())
                else:
                    st.error(f"❌ Upload gagal! Status code: {response.status_code}")
                    st.text(response.text)
                    
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error koneksi: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error tidak terduga: {str(e)}")

# Tabs untuk dokumentasi dan pengaturan
tab1, tab2 = st.tabs(["📝 Dokumentasi", "⚙️ Pengaturan"])

with tab1:
    st.subheader("Cara Penggunaan")
    st.markdown("""
    1. **Upload File**: Klik tombol 'Browse files' untuk memilih video
    2. **Preview**: Preview video akan ditampilkan setelah file dipilih
    3. **Upload**: Klik tombol 'Upload ke API' untuk mengirim video
    4. **Hasil**: Lihat hasil upload dan respons dari API
    
    **Format yang didukung:** MP4, AVI, MOV, MKV, WEBM
    """)

with tab2:
    st.subheader("Konfigurasi API")
    custom_api_url = st.text_input(
        "Custom API URL",
        value=API_URL,
        help="Masukkan URL API kustom jika diperlukan"
    )
    
    if custom_api_url != API_URL:
        st.info("URL API telah diubah. Gunakan tombol reset untuk kembali ke default.")
        if st.button("🔄 Reset ke Default"):
            st.experimental_rerun()

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
