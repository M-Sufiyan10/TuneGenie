import whisper
import speech_recognition as sr
import os
import streamlit as st
def transcribe_audio():
    st.write("Loading Whisper model...")
    model = whisper.load_model("tiny")  
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.write("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=5)
        st.write("You can start speaking now...")
        
        try:
            audio_data = recognizer.listen(source, timeout=10)
            st.write("GOT IT!!!!!!")
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data.get_wav_data())
            transcription = model.transcribe("temp_audio.wav")
            
            transcribed_voice=transcription["text"]
            return transcribed_voice
        
        except sr.WaitTimeoutError:
            st.write("No speech detected within the timeout period.")
        except Exception as e:
            st.write(f"An error occurred: {e}")
        finally:
            if os.path.exists("temp_audio.wav"):
                os.remove("temp_audio.wav")
