import streamlit as st
import os
import io
import base64
from dotenv import load_dotenv
from PIL import Image
from agents.textEndPoint import ResearchAssistant
from agents.imageEndPoint import ImageOCR
from agents.duckduckGo import ResearchSearchAgent

# Load environment variables
load_dotenv()
api_key = os.getenv("HF_TOKEN")

# Streamlit Page Configuration
st.set_page_config(page_title="AI Research Hub", layout="wide")

# Custom CSS for Modern UI
def custom_css():
    st.markdown(
        """
        <style>
            body { font-family: 'Arial', sans-serif; }
            .stButton>button { width: 100%; padding: 12px; border-radius: 8px; background-color: #007bff; color: white; font-size: 16px; }
            .stTextInput>div>div>input, .stTextArea>div>textarea { font-size: 16px; }
            .stFileUploader { border: 2px dashed #aaa; padding: 20px; text-align: center; }
            .stTabs [data-baseweb="tab"] { font-size: 18px; padding: 8px; }
            .uploaded-file-container { border-radius: 10px; padding: 15px; background-color: #f5f5f5; margin-top: 10px; }
            .button-container { text-align: center; margin-top: 20px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
custom_css()

# Navigation Tabs
selected_tab = st.sidebar.radio("📚 Select a Mode:", ["Chatbot", "Image-Based Research", "Web Search", "Local Search", "Saved Research Papers"])

# Chatbot Section
if selected_tab == "Chatbot":
    st.title("💬 AI Research Chatbot")
    user_input = st.text_area("Enter a research topic:")
    col1, col2, col3 = st.columns(3)

    if col1.button("Generate Research Content", key="chatbot_btn"):
        if user_input.strip():
            assistant = ResearchAssistant(api_key=api_key)
            response = assistant.generate_response(user_input)
            st.markdown("### 🔎 Research Output:")
            st.write(response['text'])
        else:
            st.warning("⚠️ Please enter a valid query.")
    
    if col2.button("Search Online", key="web_search"):
        if user_input.strip():
            st.markdown("### 🌐 Web Research Results:")
            st.write("**[Backend will return web search results for the query]**")
        else:
            st.warning("⚠️ Please enter a valid search query.")
    
    if col3.button("Search Local Repository", key="local_search"):
        if user_input.strip():
            st.markdown("### 📂 Local Research Papers:")
            st.write("**[Backend will return matching local research papers]**")
        else:
            st.warning("⚠️ Please enter a valid search query.")

# Image-Based Research Section
elif selected_tab == "Image-Based Research":
    st.title("🖼️ Image-Based Research")
    uploaded_file = st.file_uploader("Upload an image (JPG, PNG)", type=["jpg", "png", "jpeg"], key="image_uploader")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        img_path = "temp_uploaded_image.png"
        image.save(img_path)
        
        col1, col2, col3, col4 = st.columns(4)

        if col1.button("Extract from PIL Image", key="image_pil"):
            ocr = ImageOCR()
            text = ocr.extract_text(image)
            assistant = ResearchAssistant(api_key=api_key)
            response = assistant.generate_response(text)
            st.markdown("### 🔎 Extracted Text:")
            st.write(text)
            st.markdown("### 🔎 Generated Research Content:")
            st.write(response)
        
        if col2.button("Extract from Base64", key="image_base64"):
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            ocr = ImageOCR()
            text = ocr.extract_text(img_base64)
            st.markdown("### 🔎 Extracted Text:")
            st.write(text)
        
        if col3.button("Extract from Local Path", key="image_local"):
            ocr = ImageOCR()
            text = ocr.extract_text(img_path)
            st.markdown("### 🔎 Extracted Text:")
            st.write(text)
        
        if col4.button("Search Online", key="image_web_search"):
            st.markdown("### 🌐 Web Research Results:")
            st.write("**[Backend will return web search results for the extracted text]**")

# Web Search Section
elif selected_tab == "Web Search":
    st.title("🌐 Web Research")
    query = st.text_input("Enter your research topic:", key="web_search_input")
    if st.button("Search Online", key="web_search_btn"):
        if query.strip():
            agent = ResearchSearchAgent()
            result = agent.search(query)
            st.markdown("### 🔗 Research Papers:")
            st.write(result.content)
        else:
            st.warning("⚠️ Enter a valid search query.")

# Local Search Section
elif selected_tab == "Local Search":
    st.title("📂 Local Research Paper Search")
    query = st.text_input("Enter keywords:", key="local_search_input")
    if st.button("Search Local Papers", key="local_search_btn"):
        if query.strip():
            st.markdown("### 📄 Matching Local Papers:")
            st.write("**[Local research paper results will be displayed here]**")
        else:
            st.warning("⚠️ Please enter keywords.")

# Saved Research Papers Section
elif selected_tab == "Saved Research Papers":
    st.title("📜 Saved Research Papers")
    st.write("**[Feature to list and manage saved research papers]**")
