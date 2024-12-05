from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
from pdf_handler import PDFHandler
from rag_service import RAGService

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

LOCAL_PDF_PATH = os.getenv('LOCAL_PDF_PATH')
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), 'processed')

# Initialize handlers
pdf_handler = PDFHandler(LOCAL_PDF_PATH, PROCESSED_DIR)
rag_service = RAGService(os.getenv('OPENAI_API_KEY'))
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Process PDFs and create embeddings when app starts
print("Starting PDF processing...")
pdfs = pdf_handler.get_pdfs()
for pdf in pdfs:
    print(f"Processing: {pdf}")
    pdf_handler.process_pdf(pdf)
print("PDF processing complete!")

print("Creating embeddings...")
num_processed = rag_service.process_embeddings()
print(f"Created embeddings for {num_processed} documents")

@app.route('/')
def hello():
    return {'message': 'Hello from Flask!'}

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Get relevant context from RAG service
        relevant_docs = rag_service.similar_search(user_message, k=2)
        context = "\n".join(relevant_docs)
        
        # Prepare prompt with context
        prompt = f"""Use the following context to answer the question. If the question cannot be answered using the context, provide a general response based on your knowledge:

Context:
{context}

Question: {user_message}"""

        # Call OpenAI API with context-enhanced prompt
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context from PDF documents."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        # Extract the response text
        bot_response = response.choices[0].message.content

        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'response': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)