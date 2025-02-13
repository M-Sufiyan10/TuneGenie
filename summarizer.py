# from dotenv import load_dotenv
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from app import transcribe_video, load_video, load_api

# api_key=load_api()['google_api']

# if not api_key:
#     raise ValueError("Missing GOOGLE_API_KEY. Set it in your .env file.")

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro",
#     google_api_key=api_key,  
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2
# )
# video_url=load_video()
# text_to_summarize = transcribe_video(video_url)
# summary_prompt = f"Summarize the following text:\n\n{text_to_summarize}"
# response = llm.invoke(summary_prompt)
# print("Summary:", response.content)














from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app import transcribe_video, fetch_video_url, load_api_keys
from transcribe import transcribe_audio
import streamlit as st

def initialize_llm(api_key):
    """Initialize the Google Generative AI model."""
    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY. Set it in your .env file.")
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=api_key,
        temperature=0.5
    )


def summarize_text(text, llm):
    """Summarize text using the LLM model."""
    summary_prompt = f"Summarize the following text:\n\n{text}"
    response = llm.invoke(summary_prompt)
    return response.content


def main():
    """Main function to summarize transcribed video content."""
    api_keys = load_api_keys()
    llm = initialize_llm(api_keys["google_api"])
    
    query = transcribe_audio()
    video_url = fetch_video_url(query, api_keys["youtube_api"])
    st.video(video_url)
    text_to_summarize = transcribe_video(video_url)
    summary = summarize_text(text_to_summarize, llm)
    st.write(summary)


if __name__ == "__main__":
    main()