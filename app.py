# import streamlit as st
# import os
# import requests
# import yt_dlp as youtube_dl
# import whisper
# import yt_dlp as youtube_dl
# from dotenv import load_dotenv
# from transcribe import transcribe_audio
# def load_api():
#     load_dotenv()
#     youtube_api=os.getenv("YOUTUBE_API")
#     google_api=os.getenv("GOOGLE_API_KEY")
#     return {'youtube_api':youtube_api,"google_api":google_api}

# def load_video():
#     query=transcribe_audio()
#     url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={load_api()['youtube_api']}"
#     response = requests.get(url)
#     data = response.json()
#     video_id = data["items"][0]["id"]["videoId"]
#     video_url =f"https://www.youtube.com/watch?v={video_id}"
#     return video_url

# def transcribe_video(video_url):
#     try:
#         st.write("Downloading audio...")
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#             'outtmpl': 'youtube_audio',
#         }

#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([video_url])

#         audio_path = "youtube_audio.mp3"

#         model = whisper.load_model("tiny") 
#         result = model.transcribe(audio_path)
#         transcription = result["text"]
#         os.remove(audio_path)
#         return transcription

#     except Exception as e:
#         st.error(f"An error occurred: {e}")



















import streamlit as st
import os
import requests
import yt_dlp as youtube_dl
import whisper
from dotenv import load_dotenv
from transcribe import transcribe_audio


def load_api_keys():
    """Load API keys from environment variables."""
    load_dotenv()
    return {
        "youtube_api": os.getenv("YOUTUBE_API"),
        "google_api": os.getenv("GOOGLE_API_KEY"),
    }


def fetch_video_url(query, youtube_api_key):
    """Fetch the first YouTube video URL based on a search query."""
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&q={query}&type=video&key={youtube_api_key}"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    video_id = data["items"][0]["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={video_id}"


def download_audio(video_url):
    """Download audio from a YouTube video and save it as an MP3 file."""
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": "youtube_audio",
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return "youtube_audio.mp3"


def transcribe_audio_file(audio_path):
    """Transcribe audio using the Whisper model."""
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_path)
    return result["text"]


def transcribe_video(video_url):
    """Transcribe audio from a YouTube video."""
    try:
        st.write("Downloading audio...")
        audio_path = download_audio(video_url)
        st.write("Transcribing audio...")
        transcription = transcribe_audio_file(audio_path)
        os.remove(audio_path)
        return transcription
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def main():
    """Main function to run the Streamlit app."""
    st.title("YouTube Video Transcriber")
    api_keys = load_api_keys()
    query = transcribe_audio()
    video_url = fetch_video_url(query, api_keys["youtube_api"])
    st.video(video_url)
    transcription = transcribe_video(video_url)
    return transcription


if __name__ == "__main__":
    main()