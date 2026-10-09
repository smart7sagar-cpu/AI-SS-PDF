import streamlit as st
import os
from google import genai
from google.genai import types

# 1. UI Setup
st.set_page_config(page_title="AI PDF Assistant", layout="wide")
st.title("🚀 AI PDF Assistant (made by SAGAR)")

# 🔒 Secrets se Dynamic API Key call
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("⚠️ API Key missing! Streamlit Advanced Settings -> Secrets me GEMINI_API_KEY daalein.")
    st.stop()

# File uploader
uploaded_files = st.file_uploader("Apni PDF files upload karein", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    # Multiple files processing using official Google File API
    # Yeh tareeqa bypass karta hai saare string constraints ko
    google_uploaded_files = []
    
    if not os.path.exists("temp_cloud"):
        os.makedirs("temp_cloud")
        
    with st.spinner("PDF files ko link ke liye optimize kiya ja raha hai..."):
        for uploaded_file in uploaded_files:
            # Temporary file write karein local memory cloud pipeline ke liye
            temp_path = os.path.join("temp_cloud", uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Direct file upload context to Google File API for stability
            uploaded_cloud_file = client.files.upload(file=temp_path)
            google_uploaded_files.append(uploaded_cloud_file)

    st.success("🎉 Sabhi PDFs process ho gayi hain! Ab aap pure access link ke sath chat kar sakte hain.")

    # 1. Official Cloud Summary Engine
    if st.button("📝 PDF ka detailed Summary points me chahiye?"):
        with st.spinner("AI summary generate kar raha hai..."):
            # Sabhi objects ko contents list me structure ke sath add karna
            contents = list(google_uploaded_files)
            contents.append("Niche diye gaye PDF documents ka ek clear aur detailed summary points me Hindi me likhein.")
            
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=contents,
            )
            st.write("### 📋 PDF Summary:")
            st.write(response.text)

    # 2. Page Wise Intelligent Chat Section
    st.write("---")
    st.subheader("💬 AI se Sawal Poochein (With Page Numbers)")
    user_query = st.text_input("PDF ke baare me koi bhi sawal likhein:")
    
    if user_query:
        with st.spinner("AI link context se jawab dhoond raha hai..."):
            system_instruction = (
                "Aap ek professional AI assistant hain. Bheji gayi PDF files ko read karein. "
                "User ke sawal ka bilkul sateek aur clear jawab Hindi me dein. Apne jawab me strictly "
                "batayein ki yeh jankari kis Page Number aur kis Document se li gayi hai."
            )
            
            contents = list(google_uploaded_files)
            contents.append(user_query)
            
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3
                )
            )
            st.write("### 🤖 AI ka Jawab:")
            st.write(response.text)
