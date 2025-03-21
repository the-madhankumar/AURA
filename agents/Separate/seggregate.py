import os
import shutil
import PyPDF2
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from collections import Counter

# Load API Key
load_dotenv()
api_key = os.getenv("HF_TOKEN")

# Define base folder for categorized PDFs
BASE_FOLDER = "categorized_pdfs"
NORMAL_PDF_FOLDER = os.path.join(BASE_FOLDER, "Normal_PDFs")
os.makedirs(NORMAL_PDF_FOLDER, exist_ok=True)

# Initialize LLM Model
repo_id = "Qwen/QwQ-32B"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_length=256,
    temperature=0.3,
    huggingfacehub_api_token=api_key
)

# Define Research Paper Classification Prompt
research_prompt_text = """
You are an AI assistant specializing in research classification. Analyze the given text and determine if it is a research paper.

Text: {text}

**Step 1: Identify the core topic**  
Clearly state the field of research (e.g., Deep Learning, Medicine, AI, Biology).

**Step 2: Extract Keywords**  
List the most relevant research-related keywords (e.g., neural networks, convolutional layers, classification, dataset).

**Step 3: Determine Research Paper Status**  
Does this text belong to a research paper? (Answer strictly with 'Yes' or 'No')

Response:
"""
research_prompt = PromptTemplate.from_template(research_prompt_text)
llm_chain = research_prompt | llm


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = "\n".join(filter(None, (page.extract_text() for page in reader.pages[:5])))  # Extract first 5 pages
    return text


def extract_keywords(text):
    """Uses LLM to extract keywords and determine if it's a research paper."""
    response = llm_chain.invoke({"text": text})
    print(f"LLM Response:\n{response}\n")  # Debugging print

    lines = response.split("\n")
    topic, keywords, is_research = "", [], "No"
    for line in lines:
        if "Core Topic:" in line:
            topic = line.split(":")[-1].strip()
        elif "Extracted Keywords:" in line:
            keywords = [word.strip() for word in line.split(":")[-1].split(",")]
        elif "Research Classification:" in line:
            is_research = line.split(":")[-1].strip()

    return topic, keywords, is_research.lower() == "yes"


DEEP_LEARNING_TERMS = {"deep learning", "neural network", "convolutional", "transformer", "backpropagation"}


def find_best_matching_folder(keywords):
    """Finds the best matching folder based on keyword similarity."""
    existing_folders = [folder.name for folder in os.scandir(BASE_FOLDER) if folder.is_dir() and folder.name != "Normal_PDFs"]
    
    if not existing_folders:
        return None

    folder_scores = Counter()
    for folder in existing_folders:
        folder_words = set(folder.lower().split("_"))
        for keyword in keywords:
            if keyword.lower() in folder_words:
                folder_scores[folder] += 1

    best_match = folder_scores.most_common(1)
    return best_match[0][0] if best_match else None


def save_pdf_to_category(uploaded_file):
    """Processes an uploaded PDF, extracts keywords, and categorizes it."""
    if uploaded_file:
        os.makedirs("temp", exist_ok=True)
        filename = os.path.basename(uploaded_file.name)
        temp_pdf_path = os.path.join("temp", filename)
        
        with open(temp_pdf_path, "wb") as file:
            file.write(uploaded_file.read())
        
        text = extract_text_from_pdf(temp_pdf_path)
        topic, keywords, is_research = extract_keywords(text)
        
        if any(term in text.lower() for term in DEEP_LEARNING_TERMS):
            is_research = True
        
        if is_research:
            best_folder = find_best_matching_folder(keywords) or topic or "Uncategorized"
            best_folder = best_folder.replace(" ", "_")
            new_folder_path = os.path.join(BASE_FOLDER, best_folder)
            os.makedirs(new_folder_path, exist_ok=True)
            dest_path = os.path.join(new_folder_path, filename)
        else:
            dest_path = os.path.join(NORMAL_PDF_FOLDER, filename)
        
        shutil.move(temp_pdf_path, dest_path)
        return f"Document categorized as **{best_folder if is_research else 'Normal_PDFs'}** and moved to `{dest_path}`"
    
    return "No file uploaded"


if __name__ == "__main__":
    pdf_path = r"D:\pdf_ppt\SANKAR SIR\Overview of Deep Learning in Dermatology\GAN\s41598-023-39648-8.pdf"
    with open(pdf_path, "rb") as file:
        class_result = save_pdf_to_category(file)
        print(class_result)