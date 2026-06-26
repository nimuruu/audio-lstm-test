import streamlit as st
import yt_dlp
import whisper
import librosa
import os

st.title("AI Highlight Finder")

# Fungsi Downloader dengan User-Agent yang lebih stabil
def download_audio(url):
    # Bersihkan file temp lama jika ada
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")
        
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': 'temp.mp3',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'no_warnings': True,
        'ignoreerrors': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "temp.mp3"

# Interface
url = st.text_input("Paste Link VOD (YouTube):")

if st.button("Analisis"):
    if not url:
        st.warning("Tolong masukkan link terlebih dahulu!")
    else:
        try:
            with st.spinner("Sedang mengunduh audio..."):
                audio_path = download_audio(url)
            
            with st.spinner("Sedang mentranskrip (menunggu AI bekerja)..."):
                # Load model
                model = whisper.load_model("base")
                result = model.transcribe(audio_path)
                
            st.success("Analisis Selesai!")
            
            # Tampilkan hasil
            st.write("### Highlight yang ditemukan:")
            keywords = ["gila", "mantap", "kena", "win", "kill", "gg", "epic"]
            
            found = False
            for segment in result['segments']:
                text = segment['text'].lower()
                if any(word in text for word in keywords):
                    found = True
                    start_time = int(segment['start'])
                    st.write(f"**Menit {start_time//60}:{start_time%60:02d}**: {segment['text']}")
                    st.video(url, start_time=start_time)
            
            if not found:
                st.info("Tidak ditemukan momen highlight berdasarkan keyword. Coba video lain!")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses video: {e}")
            st.write("Tips: Pastikan link tidak privat dan server memiliki akses ke video tersebut.")
