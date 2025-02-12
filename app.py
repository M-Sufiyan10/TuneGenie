# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import os
import requests
import yt_dlp as youtube_dl
from pytube import YouTube
import whisper
from pytube import YouTube
from pydub import AudioSegment
from dotenv import load_dotenv
# load_dotenv()
# # Client_id=os.getenv("CLIENT_ID")
# # client_secret=os.getenv("CLIENT_SECRET")
# # sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=Client_id, client_secret=client_secret))

# Youtube_api=os.getenv('YOUTUBE_API')
# print(Youtube_api)
# #results = sp.search(q="Jatt Mehkma", limit=1)
# #preview_url = results['tracks']['href']

# #print(preview_url)

# SEARCH_QUERY = "get me a song of Shape of You Ed Sheeran"

# url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={SEARCH_QUERY}&type=video&key={Youtube_api}"
# response = requests.get(url)
# data = response.json()
# video_id = data["items"][0]["id"]["videoId"]
video_url ="https://www.youtube.com/watch?v=RE-dLbNOkf4"
# print("YouTube Video URL:", video_url)
# st.title("Embed YouTube Video in Streamlit")
# st.video(video_url)



import streamlit as st
import yt_dlp as youtube_dl
import whisper
import os

# Title of the app
st.title("YouTube Video Transcription with Whisper AI")

# Input for YouTube URL
youtube_url = video_url

if youtube_url:
    try:
        # Step 1: Download the audio from the YouTube video using yt-dlp
        st.write("Downloading audio...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'youtube_audio',  # Output file name without extension
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # Path to the downloaded audio file
        audio_path = "youtube_audio.mp3"

        # Step 2: Transcribe the audio using Whisper AI
        st.write("Transcribing audio...")
        model = whisper.load_model("base")  # Use "small", "medium", or "large" for better accuracy
        result = model.transcribe(audio_path)
        transcription = result["text"]

        # Step 3: Display the transcription
        st.write("Transcription:")
        st.write(transcription)

        # Step 4: Embed the YouTube video
        st.write("Embedded YouTube Video:")
        st.video(youtube_url)

        # Step 5: Allow users to download the transcription
        if transcription:
            st.download_button(
                label="Download Transcription",
                data=transcription,
                file_name="transcription.txt",
                mime="text/plain"
            )

        # Clean up temporary files
        os.remove(audio_path)

    except Exception as e:
        st.error(f"An error occurred: {e}")