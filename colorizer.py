#!/bin/env python

import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

import render

UPLOAD_FOLDER = '/root/uploads'
ALLOWED_EXTENSIONS = set(['ct', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
	content = ""
        for i in file.stream.readlines():
	    content += i
	(resp_code, resp) = render.render_msg(file.filename, content)
        return app.make_response((resp, resp_code))
        #if file and allowed_file(file.filename):
        #    filename = secure_filename(file.filename)
        #    filename = file.filename
        #    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #    return redirect(url_for('uploaded_file',
        #                            filename=filename))
	#    return 
    return '''
    <!doctype html>
    <title>Upload a File to Colorize</title>
    <h1>Upload a File to Colorize</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><br/>
         <input type=submit value=Colorize!!>
    </form>
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    port = 5050
    host = '0.0.0.0'
    app.config['DEBUG'] = True

    app.run(host=host, port=port)
