from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY. Set it in your .env file.")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=api_key,  # Pass API key here
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)
text_to_summarize = """
LLaMA (Large Language Model Meta AI) is a state-of-the-art language model developed by Meta. 
It is designed to be efficient and effective for various natural language processing tasks, 
including summarization, translation, and code generation. LLaMA models are available in 
different sizes, making them suitable for both small-scale and large-scale applications.
"""
summary_prompt = f"Summarize the following text:\n\n{text_to_summarize}"
response = llm.invoke(summary_prompt)
print("Summary:", response.content)
