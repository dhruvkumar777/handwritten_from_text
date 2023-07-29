from flask import Flask, render_template,request,redirect, url_for
import os
from werkzeug.utils import secure_filename
from pywhatkit import text_to_handwriting
import docx
import PyPDF2
from PIL import Image
from textconverter import texthandwritten as th


def readfile(filename):
    ext = os.path.splitext(filename)[-1].lower()
    if ext=='.txt':
        f = open('C:/Users/disci777/Desktop/flask/static/uploads/'+filename, 'r')
        readcontent = f.read()
        text = th.text_to_handwriting(
            readcontent, save_to='C:/Users/disci777/Desktop/flask/static/readcontent/test1.PNG')
    elif ext=='.docx':
        doc = docx.Document(
            'C:/Users/disci777/Desktop/flask/static/uploads/'+filename)
        doctext = []
        for singleline in doc.paragraphs:
            doctext.append(singleline.text)
        readcontent='\n'.join(doctext)
        text = th.text_to_handwriting(
            readcontent, save_to='C:/Users/disci777/Desktop/flask/static/readcontent/test1.PNG', rgb=[20, 20, 20])
    elif ext=='.pdf':
        pdf = 'C:/Users/disci777/Desktop/flask/static/uploads/'+filename
        pdfread = PyPDF2.PdfReader(pdf)
        page = pdfread.pages[0]
        pagecontent = page.extract_text()
        readcontent = ' '.join(pagecontent.split())
        text = th.text_to_handwriting(
            readcontent, save_to='C:/Users/disci777/Desktop/flask/static/readcontent/test1.PNG', rgb=[20, 20, 20])
    
    image = Image.open(
        'C:/Users/disci777/Desktop/flask/static/readcontent/test1.PNG')
    im=image.convert('RGB')
    im.save(r'C:/Users/disci777/Desktop/flask/static/readcontent/test1.pdf')

    return 'test23.PNG'


app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = 'C:/Users/disci777/Desktop/flask/static/uploads/'


@app.route("/", methods=['POST', 'GET'])
def upload_image():
    if request.method=='POST':
        image=request.files['file']
        if image.filename=='':
            print('Invalid')
            return redirect(request.url)

        filename=secure_filename(image.filename)

        basedir=os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(basedir,app.config['IMAGE_UPLOADS'],filename))

        filen=readfile(filename)


        return render_template('index.html',filename=filen)

    return render_template('index.html')


@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='/readcontent/test1.png'), code=301)


port=int(os.environ.get('PORT',5000))

app.run(debug=True,host='192.168.68.104',port=port)
