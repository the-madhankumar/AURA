import streamlit as st
import os
import io
import base64
from dotenv import load_dotenv
from PIL import Image
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
from agents.EmbedEndpoints import ResearchPaperManager
from agents.searchEndpoint import SearchManager

from agents.textEndPoint import ResearchAssistant
from agents.imageEndPoint import ImageOCR
from agents.duckduckGo import ResearchSearchAgent

# Load environment variables
load_dotenv()
api_key = os.getenv("HF_TOKEN")
research_manager = ResearchPaperManager()
search_manager = SearchManager()
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="research_paper")

def process_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])
    return text

def add_to_chromadb(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    chunk_embeddings = embedding_model.encode(chunks, show_progress_bar=True)
    
    for i, (chunk, embedding) in enumerate(zip(chunks, chunk_embeddings)):
        collection.add(documents=[chunk], embeddings=[embedding.tolist()], ids=[str(i)])

def search_research_paper(query, top_k=5):
    query_embedding = embedding_model.encode([query])
    results = collection.query(query_embeddings=query_embedding.tolist(), n_results=top_k)
    return results["documents"]

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
selected_tab = st.sidebar.radio("📚 Select a Mode:", ["Chatbot", "Image-Based Research", "Web Search", "Upload & Search", "Local Search", "Saved Research Papers"])

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
            agent = ResearchSearchAgent()
            result = agent.search(user_input)
            st.write(result.content)
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
    main_text = ""
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        img_path = "temp_uploaded_image.png"
        image.save(img_path)
        
        col1, col2, col3, col4 = st.columns(4)

        if col1.button("Extract from PIL Image", key="image_pil"):
            ocr = ImageOCR()
            text = ocr.extract_text(image)
            main_text = text
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
            main_text = text
            st.markdown("### 🔎 Extracted Text:")
            st.write(text)
        
        if col3.button("Extract from Local Path", key="image_local"):
            ocr = ImageOCR()
            text = ocr.extract_text(img_path)
            st.markdown("### 🔎 Extracted Text:")
            st.write(text)
        
        if col4.button("Search Online", key="image_web_search"):
            st.markdown("### 🌐 Web Research Results:")
            agent = ResearchSearchAgent()
            result = agent.search(main_text)
            st.markdown("### 🔗 Research Papers:")
            st.write(result.content)

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
elif selected_tab == "Upload & Search":
    st.title("📤 Upload & Search Research Papers")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], key="pdf_uploader")
    
    if uploaded_file:
        with st.spinner("Processing PDF..."):
            text = process_pdf(uploaded_file)
            add_to_chromadb(text)
        st.success("✅ Research paper uploaded and stored successfully!")
    
    query = st.text_input("🔍 Search your uploaded papers:", key="upload_search_input")
    if st.button("Search Uploaded Papers", key="upload_search_btn"):
        if query.strip():
            results = search_research_paper(query, top_k=5)
            assistant = ResearchAssistant(api_key=api_key)
            response = assistant.generate_response(query,results)
            st.markdown("### 📄 Matching Uploaded Papers:")
            # if results:
            #     for idx, doc in enumerate(results, 1):
            #         st.write(f"{idx}. {doc}")
            # else:
            #     st.write("No matching research papers found.")
            st.markdown("### 🔎 Generated Research Content:")
            st.write(response.content)
        else:
            st.warning("⚠️ Please enter keywords.")

elif selected_tab == "Local Search":
    st.title("📂 Local Research Paper Search")
    query = st.text_input("Enter keywords:", key="local_search_input")
    
    if st.button("Search Local Papers", key="local_search_btn"):
        if query.strip():
            results = search_research_paper(query, top_k=5)
            assistant = ResearchAssistant(api_key=api_key)

            # Convert results to text format for response generation
            retrieved_text = "\n\n".join([doc for sublist in results for doc in sublist]) if results else "No relevant papers found."

            # Generate response using retrieved text
            response = assistant.generate_response(f"{query}\n\n{retrieved_text}")

            st.markdown("### 📄 Matching Local Papers:")
            if results:
                for idx, doc in enumerate(results, 1):
                    st.write(f"{idx}. {doc}")
            else:
                st.write("No matching research papers found.")

            st.markdown("### 🔎 Generated Research Content:")
            st.write(response)
        else:
            st.warning("⚠️ Please enter keywords.")

# Saved Research Papers Section
elif selected_tab == "Saved Research Papers":
    st.title("📜 Saved Research Papers")
    st.write("**[Feature to list and manage saved research papers]**")
