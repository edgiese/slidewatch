import csv

import flask
from flask import render_template, request

import state

# from werkzeug import secure_filename

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    with open('index.html', 'r') as file:
        data = file.read()
    return data


@app.route('/upload')
def upload_file_form():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return 'file uploaded successfully'


@app.route('/slide/<int:slide_num>', methods=['GET'])
def set_slide(slide_num):
    print(slide_num)
    state.set_slide(slide_num)
    return "<p>processed %d</p>" % slide_num


def init():
    with open('Worship Instructions 2021-02-07.csv') as f:
        f.read(3)
        reader = csv.DictReader(f)
        lines = []
        for row in reader:
            lines.append(row)
    state.init(lines)


init()
app.config['UPLOAD_FOLDER'] = "C:\\worship_instructions"
app.config['MAX_CONTENT_PATH'] = 200000
app.run(host='0.0.0.0')
