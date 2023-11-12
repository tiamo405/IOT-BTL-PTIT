
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Thư mục để lưu trữ ảnh
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Phần mở rộng tệp cho phép
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')
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
    # kiểm tra có phải refesh không. nếu == True là không, xử lí yêu cầu
    is_refresh = request.form.get('is_refresh', 'false')
    print(is_refresh)
    
    if file and allowed_file(file.filename) and is_refresh == 'true':
        # Lưu trữ tệp ảnh
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Nhận dữ liệu khác từ form
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']

        # Thực hiện xử lý với dữ liệu và ảnh ở đây
        # Ví dụ: in thông tin ra console
        print(f"Name: {name}, Age: {age}, Gender: {gender}")
        print(f"Image saved as: {filename}")

        # Trả về kết quả thành công
        return render_template('add_family.html', result={'result': 'success', 'message': 'File uploaded successfully'})

    # Trả về kết quả thất bại với thông báo lỗi
    return render_template('add_family.html', result={'result': 'failed', 'error': 'Invalid file format'})

if __name__ == '__main__':
    app.run(debug=True)
