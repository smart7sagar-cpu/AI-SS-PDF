import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader

# 1. UI Configuration Setup
st.set_page_config(page_title="AI PDF Assistant", layout="wide")
st.title("🚀 AI PDF Assistant (made by SAGAR)")

# 🔒 Secrets Pipeline Validation
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("⚠️ API Key issue! Streamlit Advanced Settings -> Secrets me GEMINI_API_KEY confirm karein.")
    st.stop()

# Multi File Uploader System
uploaded_files = st.file_uploader("Apni PDF files upload karein", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    full_context = ""
    
    with st.spinner("PDF layers se text content parse kiya ja raha hai..."):
        for uploaded_file in uploaded_files:
            reader = PdfReader(uploaded_file)
            for page_num, page in enumerate(reader.pages):
                text_content = page.extract_text()
                if text_content:
                    full_context += f"\n--- [Document: {uploaded_file.name} | Page Number: {page_num + 1}] ---\n"
                    full_context += text_content

    st.success("🎉 All documents loaded inside memory cache successfully!")

    # 1. Safe Production Summary Engine Execution
    if st.button("📝 PDF ka detailed Summary points me chahiye?"):
        if not full_context.strip():
            st.warning("Document me text content nahi mila.")
        else:
            with st.spinner("AI engine summary generate kar raha hai..."):
                prompt = f"Niche diye gaye PDF data ka ek clear aur detailed summary points me Hindi me likhein:\n\n{full_context[:45000]}"
                
                # Dynamic identifier mapping to official active stable instance
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=prompt,
                )
                st.write("### 📋 PDF Summary Content:")
                st.write(response.text)

    # 2. Page Wise Structured Search Chat System
    st.write("---")
    st.subheader("💬 AI se Sawal Poochein (With Document Page Numbers)")
    user_query = st.text_input("PDF ke context ke baare me koi bhi sawal likhein:")
    
    if user_query:
        if not full_context.strip():
            st.warning("Data load nahi ho paaya.")
        else:
            with st.spinner("AI response structural parameters fetch kar raha hai..."):
                system_instruction = (
                    "Aap ek highly efficient AI assistant hain. Diye gaye text context ko strictly use karein. "
                    "User ke sawal ka bilkul clear aur sateek jawab Hindi me do. Apne answer me metadata verification "
                    "ke liye check karein aur target Document Name aur Page Number zaroor highlight karein."
                )
                
                prompt_payload = f"Context Data:\n{full_context[:55000]}\n\nSawal: {user_query}"
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash', 
                    contents=prompt_payload,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2
                    )
                )
                st.write("### 🤖 AI Response:")
                st.write(response.text)
