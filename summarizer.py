from langchain_google_genai import ChatGoogleGenerativeAI
from app import transcribe_video, fetch_video_url, load_api_keys
from transcribe import transcribe_audio
import streamlit as st


def setup_LLM_configurations():
    with st.sidebar:
        temperature=st.slider("TUNE THE GENIE TEMPERATURE !!!!",min_value=0.0, max_value=1.0,value=0.5,step=0.1)
        max_tokens=st.slider("TUNE THE GENIE MAX TOKENS !!!!",min_value=100, max_value=1000,value=500,step=100)
        max_tries=st.slider("TUNE THE GENIE MAX TRIES",min_value=3,max_value=6,value=3,step=1)
    return {'temperature':temperature,
            "tokens":max_tokens,
            "tries":max_tries
            }


def initialize_llm(api_key):
    """Initialize the Google Generative AI model."""
    if not api_key:
        raise ValueError("Missing GOOGLE_API_KEY. Set it in your .env file.")
    llm_config=setup_LLM_configurations()
    return ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=api_key,
    temperature=llm_config['temperature'],
    max_tokens=llm_config['tokens'],
    max_retries=llm_config['tries']
        )


def summarize_text(text, llm):
    """Summarize text using the LLM model."""
    summary_prompt = f"Summarize the following text in bullet points :\n\n{text}"
    response = llm.invoke(summary_prompt)
    return response.content


def main():
    """Main function to summarize transcribed video content."""
    st.subheader("TUNEGENIE")
    api_keys = load_api_keys()
    llm = initialize_llm(api_keys["google_api"])
    if not st.button("Input your voice"):
        return False
    query=transcribe_audio()
    video_url = fetch_video_url(query, api_keys["youtube_api"])
    st.video(video_url)
    text_to_summarize = transcribe_video(video_url)
    summary = summarize_text(text_to_summarize, llm)
    st.subheader("SUMMARY: ")
    st.write(summary)

if __name__ == "__main__":
    main()