import streamlit as st
import yt_dlp
import whisper
import os
import glob

st.title("AI Highlight Finder")

# Fungsi Downloader yang lebih fleksibel
def download_audio(url):
    # Hapus file sisa (mp3, m4a, webm) agar tidak bingung
    for f in glob.glob("temp.*"):
        os.remove(f)
        
    ydl_opts = {
        # 'bestaudio' akan mengambil file audio terpisah. 
        # Jika YouTube memaksa, '/best' akan menjadi cadangannya.
        'format': 'bestaudio/best', 
        'outtmpl': 'temp.%(ext)s',
        'cookiefile': 'cookies.txt', 
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'quiet': False, # Ubah ke False agar jika ada error, log di Streamlit lebih detail
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Cari file apa pun yang berawalan 'temp.'
    files = glob.glob("temp.*")
    if not files:
        raise FileNotFoundError("Gagal mengunduh audio.")
    return files[0] # Mengembalikan file pertama yang ditemukan

# Interface
url = st.text_input("Paste Link VOD (YouTube):")

if st.button("Analisis"):
    if not url:
        st.warning("Tolong masukkan link terlebih dahulu!")
    else:
        try:
            with st.spinner("Mengunduh..."):
                audio_path = download_audio(url)
            
            with st.spinner("Mentranskrip..."):
                # Whisper bisa baca m4a, webm, mp3 tanpa masalah
                model = whisper.load_model("base")
                result = model.transcribe(audio_path)
                
            st.success("Analisis Selesai!")
            
            st.write("### Daftar Highlight:")
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
                st.info("Tidak ditemukan momen dengan keyword tersebut.")
                
        except Exception as e:
            st.error(f"Error: {e}")
