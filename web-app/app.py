from flask import Flask, render_template, request, redirect, url_for, flash
from flask_paginate import Pagination, get_page_parameter
from werkzeug.utils import secure_filename
import sys, os, json


cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.dirname(cwd)))
sys.path.insert(0, cwd)
# import file code
from api.api import api_add_family
import config
import utils_time

# minio
from s3_minio.minio_ import Minio_Client
from s3_minio import utils_minio
# Khởi tạo Minio Clinet
minio = Minio_Client()


app = Flask(__name__)

# app.secret_key = 'your_secret_key'
# Thư mục để lưu trữ ảnh
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Phần mở rộng tệp cho phép
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if os.path.exists(os.path.join(config.DIR_ROOT, "tmp/data/data.json")) :
        f = open(os.path.join(config.DIR_ROOT, "tmp/data/data.json"))
        data_json = json.load(f)
    else:
        data_json = minio.get_file_json(name_file= "data/data.json", bucket='iot')

    data = []
    for key in data_json:
        item = data_json[str(key)]
        one_data = {
            "date" : utils_time.timestamp_to_date(item["timeVisit"]),
            "name" : item["name"],
            "image" : minio.get_url(bucket='iot', name_file= os.path.join('data', str(item["timeVisit"])+'.jpg'))
        }
        data.append(one_data)
    data.reverse()
    return render_template('index.html', data=data)
    # return 'Hello'

@app.route('/add_family')
def add_family():
    return render_template('add_family.html')

@app.route('/upload_family', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)
   
    
    if file and allowed_file(file.filename):
        # Lưu trữ tệp ảnh
        filename = secure_filename(file.filename)
        file.save(os.path.join(DIR_ROOT, app.config['UPLOAD_FOLDER'], filename))

        # Nhận dữ liệu khác từ form
        name = request.form['name']
        dob = request.form['dob']
        gender = request.form['gender']

        # Thực hiện xử lý với dữ liệu và ảnh ở đây

        # Ví dụ: in thông tin ra console
        print(f"Name: {name}, DoB: {dob}, Gender: {gender}")
        print(f"Image saved as: {filename}")

        # bat dau them vao data base
        error = api_add_family(image= os.path.join(DIR_ROOT,app.config['UPLOAD_FOLDER'], filename), name= name, gender= gender, dob= dob)
        # Trả về kết quả thành công
        if error == "File uploaded successfully" :
            flash(error, 'success')
        else :
            flash(error, 'error')
        return redirect(url_for('add_family'))
        
    # Trả về kết quả thất bại với thông báo lỗi
    flash('Invalid file format', 'error')
    return redirect(url_for('add_family.html'))

if __name__ == '__main__':
    app.run(debug=True)
