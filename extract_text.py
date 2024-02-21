# Extract the text on the first page of the pdf

import fitz

def get_text(path):
  pdf_document = fitz.open(path)

  text = pdf_document[0].get_text()
  text = text.replace("\n", " ")

  return text