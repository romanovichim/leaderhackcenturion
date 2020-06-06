import os
from flask import Flask, request, redirect, url_for, send_from_directory,after_this_request,render_template
from werkzeug.utils import secure_filename
#from util import removefile
import uuid



#TryTheme - тестовый алгоритм на 5 тем
from trythemeit import generatetopics
from wordcgen import generatewordcloud 

ALLOWED_EXTENSIONS = set(['pdf', 'docx'])
# куда и какие расширения для ограничений


app = Flask(__name__, instance_path=os.path.dirname(os.path.realpath(__file__)))
UPLOAD_FOLDER = os.path.join(app.instance_path, 'files')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# включаем и настраиваем папку

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# проверка расширения файла

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        #сгенерируем уникальный идентификатор
        unique= uuid.uuid4().hex
        os.mkdir(app.config['UPLOAD_FOLDER']+'/'+unique+'/')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+'/'+unique, filename))

        #return render_template('success.html')

        return redirect(url_for('uploaded_file',filenames=unique))



    return render_template('index.html')
   



@app.route('/<filenames>')
def uploaded_file(filenames):
    table= generatetopics(filenames)
    generatewordcloud(filenames)
    return render_template('trytable.html', tbl=table,bgimgname=filenames+".png")

    #return render_template('success.html')
    #return render_template('trytable.html', tbl=table)
    #return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
    




if __name__ == '__main__':
    app.run()
