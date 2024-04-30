# import fitz  

# def extract_text_from_pdf(file_path):
#     with fitz.open(file_path) as doc:
#         text = ""
#         for page in doc:
#             text += page.get_text()
#     return text

# pdf_text = extract_text_from_pdf('ChernovaAllaResume.pdf')
# print(pdf_text)

import PyPDF2

def convert_pdf_to_text(pdf_path):
    pdf = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    text = ''
    for page in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page).extractText()
    pdf.close()
    return text