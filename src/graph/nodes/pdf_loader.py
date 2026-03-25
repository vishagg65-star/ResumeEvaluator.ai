# graph/nodes/pdf_loader.py

from langchain_community.document_loaders import PyPDFLoader
from typing import Dict

from src.graph.state.graph_state import ResumeState


def pdf_loader(state: ResumeState) -> ResumeState:
    """
    Node A: Loads resume PDF and extracts raw text.
    """
    pdf_path = state.get("pdf_path")

    if not pdf_path:
        raise ValueError("pdf_path missing in state")

    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        text = "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"[WARN] PyPDFLoader failed: {e}")
        # fallback
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"

    extracted_text = text.strip()
    print("[pdf_loader] Extracted text length:", len(extracted_text))
    return {
        "resume_text": extracted_text
    }
