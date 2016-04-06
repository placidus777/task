import os
from flask import request, redirect, url_for, render_template
from app import app
from werkzeug.utils import secure_filename
from flask import send_from_directory
import uuid
import shelve

exts1=['png', 'jpg', 'jpeg', 'gif']
exts2=[x.upper() for x in exts1]

ALLOWED_EXTENSIONS = set(exts1+exts2)
UPLOAD_FOLDER = './app/static/pictures'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def saveData(flid,flname,comm):
    with shelve.open('./app/dbfile') as db:
        data = db.get('data')
        data[flid]=flname,comm
        db['data']=data

def getData():
    with shelve.open('./app/dbfile') as db:
        data = db.get('data')
        if data:
            return data
        else:
            return {}

@app.route('/')
@app.route('/index')
def index():
    #data = os.listdir(os.getcwd()+'/app/static/pictures')
    data = getData()
    return render_template('index.html',title="Отображение файлов",data=data)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':
        file = request.files['file']
        comment = request.form['message']
        if file and allowed_file(file.filename):
            flid = uuid.uuid4().hex
            filename = flid +'.'+file.filename.split('.')[-1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            saveData(flid,filename,comment)
            return redirect(url_for('index'))
    return render_template('form.html',title="Форма ввода")
