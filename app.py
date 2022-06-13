import os

from werkzeug.utils import secure_filename
from flask import Flask, render_template, \
    flash, request, redirect, url_for

from processing.object_detection import detect


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
    elif request.method == 'GET':
        if 'filename' in request.values:
            image_path = f'{UPLOAD_FOLDER}/{request.values["filename"]}'
            detect(image_path)
            return render_template('index.html',
                image_path=image_path)
        return render_template('index.html')
    else:
        return 'Some error!'


if __name__ == '__main__':
    app.run()
