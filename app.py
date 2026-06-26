import streamlit as st
import yt_dlp
import whisper
import os
import glob

st.title("🎬 AI Highlight Finder")

# Fungsi Downloader
def download_audio(url):
    for f in glob.glob("temp_audio.*"):
        os.remove(f)
        
    ydl_opts = {
        'outtmpl': 'temp_audio.%(ext)s',
        'cookiefile': 'cookies.txt',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    files = glob.glob("temp_audio.*")
    if not files:
        raise FileNotFoundError("Gagal mengunduh audio.")
    return files[0]

# Fungsi Pemroses AI
def process_audio(audio_path, video_url=None):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    
    st.success("Analisis AI Selesai!")
    st.write("### Daftar Highlight:")
    keywords = ["gila", "mantap", "kena", "win", "kill", "gg", "epic"]
    found = False
    
    for segment in result['segments']:
        text = segment['text'].lower()
        if any(word in text for word in keywords):
            found = True
            start_time = int(segment['start'])
            st.write(f"**Menit {start_time//60}:{start_time%60:02d}**: {segment['text']}")
            
            # Hanya tampilkan pemutar video jika sumbernya dari link YouTube
            if video_url:
                st.video(video_url, start_time=start_time)
    
    if not found:
        st.info("Tidak ditemukan momen highlight berdasarkan keyword pada klip ini.")

# --- TAMPILAN ANTARMUKA ---
tab1, tab2 = st.tabs(["📁 Upload File (Paling Aman)", "🔗 Link YouTube"])

with tab1:
    st.write("Bypass blokir YouTube dengan mengunggah file video/audio potongan secara langsung.")
    uploaded_file = st.file_uploader("Upload file (.mp3, .mp4, .wav, .m4a)", type=['mp3', 'mp4', 'wav', 'm4a'])
    
    if st.button("Analisis File"):
        if uploaded_file is not None:
            try:
                with st.spinner("Menyimpan file dan mentranskrip dengan AI..."):
                    # Simpan file yang diupload
                    temp_path = "temp_upload." + uploaded_file.name.split('.')[-1]
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Jalankan AI
                    process_audio(temp_path)
            except Exception as e:
                st.error(f"Error saat memproses: {e}")
        else:
            st.warning("Tolong upload file terlebih dahulu!")

with tab2:
    st.write("Catatan: Opsi ini mungkin tidak stabil karena proteksi anti-bot dari server penyedia video.")
    url = st.text_input("Paste Link VOD:")
    
    if st.button("Analisis Link"):
        if not url:
            st.warning("Masukkan link terlebih dahulu!")
        else:
            try:
                with st.spinner("Mengunduh..."):
                    audio_path = download_audio(url)
                with st.spinner("Mentranskrip dengan AI..."):
                    process_audio(audio_path, video_url=url)
            except Exception as e:
                st.error(f"Error: {e}")
