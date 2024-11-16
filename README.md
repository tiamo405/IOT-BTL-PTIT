# Đề tài : Sử dụng khuôn mặt để đóng mở cửa tự động. Có thể theo dõi qua telegram và Web app

## Face
- Feature :
    + Nhận dạng người quen
        + Done
    + Đóng mở cửa
        + Chưa tích hợp sensor
    + Đẩy dữ liệu lên s3
        + Done
- Run
```sh
pythom main.py
```
Mới chạy video, chưa thử camera
## Telegram 
+ Run
```sh
cd bot_tele
python bot_noti.py
```
- Chạy nếu cần sử dụng lệnh trên tele để điều khiển cửa
## Web-app
- Feature :
    + add_family 
        + Done
    + View history 
        + Done
+ Run 
```sh
python web-app/app.py
```
## Phần cứng IOT
- Sử dụng esp8266 và 1 động cơ sevor ( motor qua 180 độ) để quay vòng
- gửi dữ liệu từ backend lên firebase để esp8266 nhận dữ liệu rồi truyền 0-1 cho servo
- nạp code vào esp8266: 
    + [code arduino](sensor/code_arduino.ino)
    + Cài 1 số thư viện theo video này: https://youtu.be/0LYmD8jv7xo?si=aa06ErAPrg90SBUX
        + [link add để tải esp8266](https://arduino.esp8266.com/stable/package_esp8266com_index.json)
```
# lỗi ttyUSB0( chưa xác nhận)
sudo su
//type your password
cd /
cd dev
chown username ttyUSB0
```
## Tài liệu
+ [docs](https://www.google.com/)
+ [slide](https://www.google.com/)
## test github dev