import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# 2. UI Layout
st.set_page_config(page_title="AI Chat Assistant", page_icon="💬")
st.title("📸 Universal Chat Assistant")
st.write("Upload a screenshot or paste text to get the perfect reply.")

# Sidebar for settings
with st.sidebar:
    tone = st.selectbox("Choose Tone", ["Friendly", "Professional", "Funny", "Short & Sweet", "Sarcastic"])
    detail_level = st.slider("Detail Level", 1, 5, 3)

# 3. Input Section (Tabs)
tab1, tab2 = st.tabs(["🖼️ Screenshot", "✍️ Paste Text"])

with tab1:
    uploaded_file = st.file_uploader("Upload a screenshot of the chat", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Screenshot", use_column_width=True)

with tab2:
    chat_text = st.text_area("Paste the chat history here...", height=200)

# 4. Logic Section
if st.button("Generate Suggestions ✨", type="primary"):
    with st.spinner("Analyzing..."):
        try:
            prompt = f"Analyze this chat and suggest 3 different replies in a {tone} tone. The goal is a level {detail_level} out of 5 for detail."
            
            if uploaded_file:
                # If image is provided, send both image and prompt
                response = model.generate_content([prompt, image])
            elif chat_text:
                # If only text is provided
                response = model.generate_content(f"{prompt}\n\nChat history:\n{chat_text}")
            else:
                st.warning("Please provide either a screenshot or some text!")
                st.stop()

            # Display Result
            st.subheader("Suggested Replies:")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")

# 5. Instructions
st.info("Pro-tip: You can use 'Windows + Shift + S' to take a screenshot and save it, then drag it here.")