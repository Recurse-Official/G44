import requests  
import pdfplumber  
url = "https://arxiv.org/pdf/1706.03762.pdf"  
response = requests.get(url)

with open("my_pdf_file.pdf", "wb") as file:  
    file.write(response.content)

print("PDF downloaded!")

with pdfplumber.open("my_pdf_file.pdf") as pdf:
    text = ""
    for page in pdf.pages: 
        text += page.extract_text()  
with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
    text_file.write(text)

import sys
sys.stdout.reconfigure(encoding='utf-8')  
print("Extracted Text Preview:\n", text[:500])  