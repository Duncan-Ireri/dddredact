import os, glob      # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template, jsonify, send_file, abort
from werkzeug.utils import secure_filename
from readpdf import create_api, save_data
from makepdf import genTxt, txt2pdf

app = Flask(__name__)


app.secret_key = "secret key" # for encrypting the session
#It will allow below 16MB contents only, you can change it
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'bills')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf'])

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/dirtree', defaults={'req_path': ''})
@app.route('/dirtree/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = 'final'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('dirtree.html', files=files)


@app.route('/api/v1')
def api():
      
      print('..saving data')
      res = create_api()

      res_saving = save_data()

      print('..redacting data')

      res_2txt = genTxt()

      res_redact = txt2pdf()

      return jsonify(res)

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')

            return redirect('api/v1')
        else:
            flash('Allowed file types are txt, pdf')
            return redirect(request.url)


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 
 