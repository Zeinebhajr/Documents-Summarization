from flask import Flask, request, render_template 
import os
from werkzeug.utils import secure_filename
from model import summarize_documents

app = Flask(__name__)

# Set up upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('uploads.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return "No file part"
    
    files = request.files.getlist('files')  # Get list of uploaded files
    
    if len(files) == 0:
        return "No selected files"
    
    # Get user inputs for summary settings
    max_length = request.form.get('max_length', type=int)
    min_length = request.form.get('min_length', type=int)

    cluster_documents = 'clusterDocuments' in request.form
    percentage = request.form.get('percentage', type=int) if cluster_documents else None
  # List to hold summaries for each document
    documents=[]
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the file
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            documents.append(text)
            
            # Pass the parameters to the summarize_documents function
    summary = summarize_documents(documents, max_length, min_length, percentage,cluster_documents)
    return render_template('results.html', summary=summary)
app.run(debug=True)
