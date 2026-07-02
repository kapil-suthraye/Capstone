from Backend.app.services.pdf_parser import PDFParser

parser = PDFParser()

doc = parser.parse("medical_records/sample.pdf")

print(doc.filename)

print(len(doc.pages))

print(doc.pages[0].lines[:5])