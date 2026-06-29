# HIKVISION to LARK BOT Integration

Dự án này sử dụng Python để lấy ảnh (snapshot) từ camera IP Hikvision qua giao thức ISAPI và gửi lên nền tảng Lark (Feishu) thông qua Bot.

## Cài đặt

1. Cài đặt Python.
2. Mở Terminal tại thư mục này và chạy:
   ```bash
   pip install -r requirements.txt
   ```

## Cấu hình

Mở file `.env` và điền:
- `CAMERA_IP`, `CAMERA_USER`, `CAMERA_PASS`: Thông tin camera Hikvision.
- `LARK_APP_ID`, `LARK_APP_SECRET`: Lấy tại [Lark Developer](https://open.larksuite.com/).
- `LARK_CHAT_ID`: ID của chat group hoặc người nhận.

## Chạy dự án

```bash
python main.py
```
