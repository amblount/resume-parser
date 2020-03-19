import os
import msvdd_bloc.resumes
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader, PdfFileWriter
import json


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'pdf'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print(UPLOAD_FOLDER)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processFile(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            redirect("/", code=302)

    return render_template('index.html')

    
@app.route('/uploads/', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
    redirect('/')

def processFile(path, filename):
    # output = PdfFileWriter()
    resume_text = msvdd_bloc.resumes.extract_text_from_pdf(path)
    resume_data = msvdd_bloc.resumes.parse_text(resume_text)
    with open(filename + '.json', 'w') as json_file:
        json.dump(resume_data, json_file)
        output_stream = app.config['DOWNLOAD_FOLDER'] + filename 
        json_file.write(output_stream)
    return jsonify(resume_data)
    # redirect('/uploads')

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
