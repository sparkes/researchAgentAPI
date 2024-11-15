from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import requests
from researchAgent.research_agent import ResearchAgent
import tempfile

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize ResearchAgent
research_agent = ResearchAgent()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@app.route('/analyze/upload', methods=['POST'])
def analyze_uploaded_pdf():
    """Endpoint to analyze an uploaded PDF file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Analyze the PDF
            result = research_agent.analyze_paper(filepath)
            
            # Clean up the uploaded file
            os.remove(filepath)
            
            return jsonify(result)
        except Exception as e:
            # Clean up the uploaded file in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

@app.route('/analyze/url', methods=['POST'])
def analyze_pdf_url():
    """Endpoint to analyze a PDF from a URL"""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    url = data['url']
    if not url.lower().endswith('.pdf'):
        return jsonify({'error': 'URL must point to a PDF file'}), 400
    
    try:
        # Download the PDF
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download PDF'}), 400
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        # Analyze the PDF
        result = research_agent.analyze_paper(temp_path)
        
        # Clean up the temporary file
        os.remove(temp_path)
        
        return jsonify(result)
    except Exception as e:
        # Clean up the temporary file in case of error
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
