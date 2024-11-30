import requests
from bs4 import BeautifulSoup
import os
import pdfplumber
import re
import json

# Create a folder to store downloaded PDFs if it doesn't exist
if not os.path.exists("pdf_files"):
    os.makedirs("pdf_files")

# Function to scrape and download PDFs
def download_pdfs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all links to PDFs
    pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
    
    # Download each PDF
    for link in pdf_links:
        pdf_url = link if link.startswith("http") else url + link
        pdf_response = requests.get(pdf_url)
        pdf_name = os.path.join("pdf_files", link.split('/')[-1])
        with open(pdf_name, 'wb') as file:
            file.write(pdf_response.content)
        print(f"{pdf_name} downloaded.")

# Example website to scrape (replace with actual URL)
url = "https://www.dgft.gov.in/CP/?opt=ft-policy"
download_pdfs(url)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text()  # Extract text from each page
    return full_text

# Function to extract text from all downloaded PDFs
def extract_text_from_all_pdfs(pdf_folder="pdf_files"):
    all_text = {}
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Extracting text from {filename}...")
            text = extract_text_from_pdf(pdf_path)
            all_text[filename] = text
    return all_text

# Extract text from all PDFs in the "pdf_files" folder
pdf_texts = extract_text_from_all_pdfs()
print(pdf_texts[list(pdf_texts.keys())[0]][:500])  # Print the first 500 characters of the first PDF's text

# Function to clean and preprocess extracted text
def clean_text(text):
    # Remove unwanted characters (example: page numbers, special symbols)
    cleaned_text = re.sub(r'\n+', ' ', text)  # Remove multiple newlines
    cleaned_text = re.sub(r'Page \d+', '', cleaned_text)  # Remove "Page 1", "Page 2" etc.
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Remove extra whitespaces
    cleaned_text = cleaned_text.strip()  # Remove leading/trailing spaces

    return cleaned_text

# Process the extracted text from each PDF
pdf_texts_cleaned = {}

for pdf_file, text in pdf_texts.items():
    cleaned = clean_text(text)
    pdf_texts_cleaned[pdf_file] = cleaned

# Preview the cleaned text
print("Cleaned Text Preview:")
for pdf_file, text in pdf_texts_cleaned.items():
    print(f"\n{pdf_file}:")
    print(text[:500])  # Preview first 500 characters of cleaned text

# Function to split text into sections (paragraphs)
def split_text(text):
    # Split the text by paragraphs or sentences (you can modify this based on your needs)
    sections = text.split("\n\n")  # Split by paragraphs
    return sections

# Function to save processed text into a JSON file
def save_processed_text(sections, filename="processed_data.json"):
    # Save the processed text into a JSON file
    with open(filename, "w") as f:
        json.dump(sections, f)

# Process the extracted and cleaned text
for pdf_file, text in pdf_texts_cleaned.items():
    sections = split_text(text)
    save_processed_text(sections, filename=f"processed_{pdf_file}.json")  # Save processed text to a file
    print(f"Processed text for {pdf_file} saved.")

# Optional: Preview the processed text
print("Processed Text Preview:")
for pdf_file, sections in pdf_texts_cleaned.items():
    print(f"\n{pdf_file}:")
    print(sections[:500])  # Preview first 500 characters of processed text
