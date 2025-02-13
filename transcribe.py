import whisper
import speech_recognition as sr
import os

def transcribe_audio():
    print("Loading Whisper model...")
    model = whisper.load_model("tiny")  
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=5)
        print("You can start speaking now...")
        
        try:
            audio_data = recognizer.listen(source, timeout=10)
            print("Recording complete. Processing audio...")
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data.get_wav_data())
            print("Transcribing audio using Whisper...")
            transcription = model.transcribe("temp_audio.wav")
            
            print("Transcription:")
            transcribed_voice=transcription["text"]
            return transcribed_voice
        
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if os.path.exists("temp_audio.wav"):
                os.remove("temp_audio.wav")
