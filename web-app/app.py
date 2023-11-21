from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import sys, os, json


cwd = os.getcwd()
sys.path.append(os.path.abspath(os.path.dirname(cwd)))
sys.path.insert(0, cwd)

import config
import utils_time
from api.api import api_add_family
# import sensor
from sensor.api import mocua, dongcua

# minio
from s3_minio.minio_ import Minio_Client
# Khởi tạo Minio Clinet
minio = Minio_Client()

# Thư mục để lưu trữ ảnh
UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
# Thư mục để lưu trữ ảnh
UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Phần mở rộng tệp cho phép
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
app.secret_key = 'your_secret_key'  # Đặt secret key là một chuỗi bí mật và duy nhất

# Config Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Mock User Database
class User(UserMixin):
    def __init__(self, user_id, username, password, is_admin=False):
        self.id = user_id
        self.username = username
        self.password = password
        self.is_admin = is_admin

users = {
    '1': User('1', 'admin', 'admin', is_admin=True),
    '2': User('2', 'user', 'user'),
}

# Flask-Login callback to load a user
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = next((u for u in users.values() if u.username == username and u.password == password), None)

        if user:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Invalid username or password.', 'error')

    return render_template('login.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@login_required
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
@login_required
def add_family():
    if not current_user.is_admin:
        flash('Permission denied. Only admins can access this page.', 'error')
        return redirect(url_for('index'))
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
        # error = "debug"
        # Trả về kết quả thành công
        if error == "File uploaded successfully" :
            flash(error, 'success')
        else :
            flash(error, 'error')
        return redirect(url_for('add_family'))
        
    # Trả về kết quả thất bại với thông báo lỗi
    flash('Invalid file format', 'error')
    return redirect(url_for('add_family.html'))

@app.route('/remove_family')
@login_required
def remove_family():
    return render_template('remove_family.html')

@app.route('/process_action', methods=['GET'])
def process_action():
    action = request.args.get('action')

    # Xử lý action tùy thuộc vào action được gửi từ frontend
    if action == 'open':
        # Thực hiện các thao tác cần thiết khi ấn nút Open
        result_message = mocua()
    elif action == 'close':
        # Thực hiện các thao tác cần thiết khi ấn nút Close
        result_message = dongcua()
    else:
        # Trường hợp không xác định action
        result_message = 'Invalid action.'

    # Trả về kết quả dưới dạng JSON
    return jsonify({'message': result_message})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
