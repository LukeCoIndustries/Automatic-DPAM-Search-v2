from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, BooleanField, StringField, IntegerField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import os
import pandas as pd
from protein_search_V2_just_code import Protein_search
from threading import Thread
app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['UPLOAD_FOLDER'] = 'static/files'
class UploadFileForm(FlaskForm):
    file = FileField('File')
    uniprot = StringField('uniprot')
    submit = SubmitField('Submit')
    extra = StringField('Yes or No')
    extra_col = StringField('extra column location')
    extra_name = StringField('extra column name')
    run = StringField('all or top')
    Zscore = StringField("Z Score")
    protein_count = StringField("Number of Protein")
    output_name = StringField('name of output File')
@app.route('/', methods = ['GET',"POST"])
@app.route('/home', methods = ['GET',"POST"])
def home():
    form = UploadFileForm()
    is_form_valid = form.validate_on_submit()
    print(is_form_valid)
    print(form.errors)
    if is_form_valid:
        print('starting')
        Protein_search(form.file.data,form.uniprot.data,form.run.data,form.output_name.data,form.extra.data,form.extra_col.data,form.extra_name,form.Zscore.data,form.protein_count.data)
        return render_template('summary.html') 
    return render_template('index.html',form = form)
    
if __name__ == '__main__':
    app.run(debug=True)