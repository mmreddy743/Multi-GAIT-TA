# pdf_handler.py
import PyPDF2
import os

class PDFHandler:
    def __init__(self, local_pdf_path: str, processed_dir: str):
        self.pdf_dir = local_pdf_path
        self.text_dir = os.path.join(processed_dir, 'texts')
        os.makedirs(self.text_dir, exist_ok=True)

    def get_pdfs(self):
        """List all PDFs in directory"""
        return [f for f in os.listdir(self.pdf_dir) if f.endswith('.pdf')]

    def process_pdf(self, pdf_name):
        """Process a single PDF file"""
        pdf_path = os.path.join(self.pdf_dir, pdf_name)
        text_path = os.path.join(self.text_dir, f"{os.path.splitext(pdf_name)[0]}.txt")

        try:
            # Return existing text if already processed
            if os.path.exists(text_path):
                with open(text_path, 'r', encoding='utf-8') as f:
                    return f.read()

            # Process PDF
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"

            # Save processed text
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text)

            return text

        except Exception as e:
            print(f"Error processing {pdf_name}: {e}")
            return None