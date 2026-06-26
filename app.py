import streamlit as st
import whisper
import os

# Konfigurasi halaman
st.set_page_config(page_title="AI Audio Detector", layout="centered")
st.title("🎙️ AI Audio Highlight Detector")
st.write("Upload file audio Anda untuk mendeteksi momen highlight secara instan.")

# Sidebar untuk pengaturan
st.sidebar.header("Pengaturan AI")
model_size = st.sidebar.selectbox("Pilih Model AI", ["tiny", "base"])
st.sidebar.info("Model 'tiny' lebih cepat, model 'base' lebih akurat.")

# Fungsi Utama Pemrosesan
def process_audio(audio_path, model_name):
    # Memuat model
    model = whisper.load_model(model_name)
    
    with st.spinner(f"AI ({model_name}) sedang bekerja..."):
        result = model.transcribe(audio_path)
    
    return result

# Antarmuka Utama
uploaded_file = st.file_uploader("Upload file audio (.mp3, .wav, .m4a)", type=['mp3', 'wav', 'm4a'])

if uploaded_file is not None:
    if st.button("Mulai Deteksi"):
        # Simpan file sementara
        temp_path = "temp_audio.mp3"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Jalankan deteksi
        result = process_audio(temp_path, model_size)
        
        # Tampilkan Hasil
        st.success("Analisis Selesai!")
        keywords = ["gila", "mantap", "kena", "win", "kill", "gg", "epic", "hebat"]
        found = False
        
        for segment in result['segments']:
            text = segment['text'].lower()
            if any(word in text for word in keywords):
                found = True
                start = int(segment['start'])
                st.write(f"⏱️ **Menit {start//60}:{start%60:02d}**: {segment['text']}")
        
        if not found:
            st.info("Tidak ada keyword highlight yang terdeteksi.")
        
        # Hapus file sementara
        if os.path.exists(temp_path):
            os.remove(temp_path)
