import os
import pdfplumber

def extract_text():
    txt = ""
    files = [f for f in os.listdir("uploads") if f.lower().endswith(".pdf")]
    for file in files:
        path = os.path.join("uploads", file)
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_txt = page.extract_text()
                if page_txt:
                    txt += page_txt
    with open("preprocessing/data.txt", "w",encoding='UTF-8') as f:
        f.write(txt)
    return txt