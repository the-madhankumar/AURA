import streamlit as st
import os
from dotenv import load_dotenv
import io
import base64
from PIL import Image

from agents.textEndPoint import ResearchAssistant
from agents.imageEndPoint import ImageOCR
from agents.duckduckGo import ResearchSearchAgent

# Load environment variables
load_dotenv()
api_key = os.getenv("HF_TOKEN")

# Set Streamlit Page Configuration
st.set_page_config(page_title="AI Research Assistant", layout="wide")

# Custom CSS for Enhanced UI
st.markdown(
    """
    <style>
        body { font-family: 'Arial', sans-serif; }
        .stButton>button { width: 100%; padding: 12px; border-radius: 8px; }
        .stTextInput>div>div>input { font-size: 16px; }
        .stFileUploader { border: 2px dashed #aaa; padding: 20px; }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
st.sidebar.title("🔍 Research Assistant")
option = st.sidebar.radio("Select a mode:", ["Chatbot", "Image-Based Research", "Web Search", "Local Search"])

# Chatbot Section
if option == "Chatbot":
    st.title("💬 AI Research Chatbot")
    st.markdown("**Enter a research topic and let AI generate structured content.**")
    
    user_input = st.text_area("Enter your research query:")

    col1, col2, col3 = st.columns(3)  # Creating three buttons in one row

    if col1.button("Generate Research Content", key="chatbot"):
        if user_input.strip():
            assistant = ResearchAssistant(api_key=api_key)
            response = assistant.generate_response(user_input)
            st.markdown("### 🔎 Generated Research Content:")
            st.write(response['text'])
        else:
            st.warning("⚠️ Please enter a valid research query.")

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
elif option == "Image-Based Research":
    st.title("🖼️ Image-Based Research")
    st.markdown("**Upload an image, and AI will extract text and search for relevant research.**")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        # Convert uploaded file to PIL Image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert image to base64 string
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Save the image locally
        img_path = f"temp_uploaded_image.png"
        image.save(img_path)

        col1, col2, col3, col4 = st.columns(4)  # Creating four buttons in one row

        if col1.button("Extract from PIL Image", key="image_pil"):
            ocr = ImageOCR()
            text = ocr.extract_text(image)  # Pass as PIL image
            assistant = ResearchAssistant(api_key=api_key)
            response = assistant.generate_response(text)
            st.markdown("### 🔎 Extracted Text:")
            st.write(text)
            st.markdown("### 🔎 Generated Research Content:")
            st.write(response)
            
        if col2.button("Extract from Base64", key="image_base64"):
            ocr = ImageOCR()
            text = ocr.extract_text(img_base64)  # Pass as base64 string
            st.markdown("### 🔎 Extracted Text:")
            st.write(text)

        if col3.button("Extract from Local Path", key="image_local"):
            ocr = ImageOCR()
            text = ocr.extract_text(img_path)  # Pass as local path
            st.markdown("### 🔎 Extracted Text:")
            st.write(text)

        if col4.button("Search Online", key="image_web_search"):
            st.markdown("### 🌐 Web Research Results:")
            st.write("**[Backend will return web search results for the extracted text]**")

# Web Search Section
elif option == "Web Search":
    st.title("🌐 Web Research")
    st.markdown("**Search for academic research papers on the web.**")
    
    query = st.text_input("Enter research topic:")
    
    if st.button("Search Online", key="web_search"):
        if query.strip():
            st.markdown("### 🔗 Research Papers Found:")
            agent = ResearchSearchAgent()
            # example user_query = "The impact of AI on climate change research"
            result = agent.search(query)
            st.write(result.content)
        else:
            st.warning("⚠️ Please enter a valid search topic.")

# Local Search Section
elif option == "Local Search":
    st.title("📂 Local Research Paper Search")
    st.markdown("**Search for research papers stored in your local repository.**")
    
    query = st.text_input("Enter keywords:")
    
    if st.button("Search Local Repository", key="local_search"):
        if query.strip():
            st.markdown("### 📄 Matching Research Papers:")
            st.write("**[Backend will return matching PDFs]**")
        else:
            st.warning("⚠️ Please enter a valid keyword.")

# Footer
st.sidebar.info("🔬 Powered by AI Research Modules")
