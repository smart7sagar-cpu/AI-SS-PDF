import streamlit as st
import os
from google import genai
from google.genai import types
from pypdf import PdfReader

# 1. UI Setup
st.set_page_config(page_title="AI PDF Assistant", layout="wide")
st.title("📄 Super-Fast AI PDF Assistant (made by SAGAR)")

# 🔒 Secrets se Safe Tarike se API Key loading
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("⚠️ API Key nahi mili! Kripya Streamlit Secrets me GEMINI_API_KEY set karein.")
    st.stop()

# File uploader (Multiple PDFs support)
uploaded_files = st.file_uploader("Apni PDF files upload karein", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    full_context = ""
    
    with st.spinner("PDF files ko read kiya ja raha hai..."):
        for uploaded_file in uploaded_files:
            reader = PdfReader(uploaded_file)
            for page_num, page in enumerate(reader.pages):
                full_context += f"\n--- [Document: {uploaded_file.name} | Page Number: {page_num + 1}] ---\n"
                full_context += page.extract_text()

    st.success("🎉 Sabhi PDFs padh li gayi hain! Ab aap bina kisi error ke chat kar sakte hain.")

    # 1. Automatic Summary Section
    if st.button("📝 PDF ka detailed Summary points me chahiye?"):
        with st.spinner("AI summary bana raha hai..."):
            prompt = f"Niche diye gaye PDF data ka ek clear aur detailed summary points me Hindi me likhein:\n\n{full_context[:50000]}"
            
            # Long-Term Production Standard Model Call
            response = client.models.generate_content(
                model='gemini-1.5-flash', 
                contents=prompt,
            )
            st.write("### 📋 PDF Summary:")
            st.write(response.text)

    # 2. Chat Section with Page Citation
    st.write("---")
    st.subheader("💬 AI se Sawal Poochein (With Page Numbers)")
    user_query = st.text_input("PDF ke baare me koi bhi sawal likhein:")
    
    if user_query:
        with st.spinner("AI jawab dhoond raha hai..."):
            system_instruction = (
                "Aap ek professional AI assistant hain. Diye gaye context (PDF text) ko achhe se padhein. "
                "User ke sawal ka bilkul sateek aur clear jawab Hindi me dein. Apne jawab me strictly "
                "batayein ki yeh jankari kis Page Number aur kis Document se li gayi hai. "
                "Agar jawab data me nahi hai, to keh dein ki 'Mujhe iska jawab document me nahi mila'."
            )
            
            prompt = f"Context:\n{full_context[:60000]}\n\nSawal: {user_query}"
            
            # Long-Term Production Standard Model Call
            response = client.models.generate_content(
                model='gemini-1.5-flash', 
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3
                )
            )
            st.write("### 🤖 AI ka Jawab:")
            st.write(response.text)
