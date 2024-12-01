import os
import streamlit as st
from llama_index.readers.file import PDFReader
from llama_index.llms.gemini import Gemini # type: ignore
from llama_index.embeddings.gemini import GeminiEmbedding # type: ignore
import streamlit.components.v1 as components
from pypdf import PdfReader

from llama_index.core import VectorStoreIndex, Document
from llama_index.core.node_parser.text import TokenTextSplitter



# Set Google API key
GOOGLE_API_KEY = "AIzaSyCwJoD3zC5VOzRSawA574nr5J_N4V-7Ph8" # os.getenv("GOOGLE_API_KEY")

llm = Gemini(model="models/gemini-1.5-flash-8b", temperature=0, embedding=GeminiEmbedding,api_key=GOOGLE_API_KEY)

    
# def extract_content(contract_pdf):
#     pdf_text = ""
#     pdf_reader = PdfReader(contract_pdf)
#     number_of_pages = len(pdf_reader.pages)
#     for index in range(number_of_pages):
#         pdf_text = pdf_text + pdf_reader.pages[index].extract_text()
#     return pdf_text

def extract_content(contract_pdfs):
    pdf_text = ""
    for i in range(len(contract_pdfs)):
        pdf_reader = PdfReader(contract_pdfs[i])
        number_of_pages = len(pdf_reader.pages)
        for index in range(number_of_pages):
            pdf_text = pdf_text + pdf_reader.pages[index].extract_text()
    return pdf_text

                                                                  
    

if 'contract_text' not in st.session_state:
    st.session_state['contract_text'] = ''

















