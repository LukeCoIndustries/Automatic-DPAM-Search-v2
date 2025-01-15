from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, BooleanField, StringField, IntegerField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import os
import pandas as pd
from protein_search_V2_just_code import Protein_search

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['UPLOAD_FOLDER'] = 'static/files'
class UploadFileForm(FlaskForm):
    file = FileField('File')
    uniprot = IntegerField('uniprot')
    submit = SubmitField('Submit')
    extra = StringField('Yes or No')
    extra_col = IntegerField('extra column location')
    extra_name = StringField('extra column name')
    run = StringField('all or top')
    Zscore = IntegerField("Z Score")
    protein_count = IntegerField("Number of Protein")
    output_name = StringField('name of output File')
@app.route('/', methods = ['GET',"POST"])
@app.route('/home', methods = ['GET',"POST"])
def home():
    form = UploadFileForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        Protein_search(form.file.data,form.uniprot.data,form.run.data,form.output_name.data,form.extra.data,form.extra_col.data,form.extra_name,form.Zscore.data,form.protein_count.data)
        return 'working on it'
    return render_template('index.html',form = form)

if __name__ == '__main__':
    app.run(debug=True)