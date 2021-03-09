import csv

import flask
from flask import render_template, request
import openpyxl
import state

# from werkzeug import secure_filename

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    with open('index.html', 'r') as file:
        data = file.read()
    return data


@app.route('/setup')
def upload_file_form():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        wb = openpyxl.load_workbook(f.filename)
        sheet = wb['Sheet1']
        header = [cell.value for cell in sheet[1]]

        lines = []
        skip_first = True
        for row in sheet:
            if skip_first:
                skip_first = False
                continue
            line = {}
            for key, cell in zip(header, row):
                line[key] = cell.value
            lines.append(line)
        state.init(lines)

        """    
        header = []
        lines = []
        for i in range(0, sheet.ncols):
            header[i] = sheet.cell_value(0, i)
        for i in range(1, sheet.nrows):
            row = {}
            for j in range(0, len(header)):
                row[header[j]] = sheet.cell_value(i, j)
        """
        return 'file uploaded successfully'


@app.route('/slide/<int:slide_num>', methods=['GET'])
def set_slide(slide_num):
    print(slide_num)
    state.set_slide(slide_num)
    return "<p>processed %d</p>" % slide_num


def init():
    with open('Worship Instructions 2021-03-03.csv') as f:
        reader = csv.DictReader(f)
        lines = []
        for row in reader:
            lines.append(row)
    state.init(lines)


# init()
app.config['UPLOAD_FOLDER'] = "C:\\worship_instructions"
app.config['MAX_CONTENT_PATH'] = 200000
app.run(host='0.0.0.0')
