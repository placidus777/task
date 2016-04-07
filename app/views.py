import os
from flask import request, redirect, url_for, render_template
from app import app
from werkzeug.utils import secure_filename
from flask import send_from_directory
import uuid
import shelve
import sqlite3

exts1=['png', 'jpg', 'jpeg', 'gif']
exts2=[x.upper() for x in exts1]

ALLOWED_EXTENSIONS = set(exts1+exts2)
UPLOAD_FOLDER = './app/static/pictures'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def saveData(flname,comment):
    db = sqlite3.connect('./app/dbase.db')
    cur = db.cursor()
    cur.execute('insert into main (filename,comment) values(?,?);',(flname,comment))
    cur.close()
    db.commit()
    db.close()

def getData():
    db = sqlite3.connect('./app/dbase.db')
    cur = db.cursor()
    cur.execute('select filename,comment from main;')
    rezz = cur.fetchall()
    cur.close()
    db.close()
    return rezz

@app.route('/')
@app.route('/index')
def index():
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
            saveData(filename,comment)
            return redirect(url_for('index'))
    return render_template('form.html',title="Форма ввода")
