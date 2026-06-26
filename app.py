import streamlit as st
import yt_dlp
import whisper
import librosa
import numpy as np

st.title("AI Highlight Finder")

# 1. Download & Audio Extraction
def download_audio(url):
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'temp.mp3', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
    return "temp.mp3"

# 2. Main UI Logic
url = st.text_input("Paste Link VOD:")
if st.button("Analisis"):
    with st.spinner("Proses VOD..."):
        audio_path = download_audio(url)
        
        # Transkripsi
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        
        # Analisis Volume (Simple Feature)
        y, sr = librosa.load(audio_path)
        
        # Tampilkan hasil
        st.write("### Daftar Highlight:")
        for segment in result['segments']:
            # Logika: Jika durasi cukup dan teks tidak kosong
            if len(segment['text'].split()) > 5:
                st.video(url, start_time=int(segment['start']))
                st.write(f"Momen: {segment['text']}")