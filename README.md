# Hệ thống AI Check-In với Lark Bot 🚀📷

Dự án này là một hệ thống Web-based cho phép nhân viên thực hiện Check-in bằng khuôn mặt thông qua Webcam của máy tính. Sau khi nhận diện, hệ thống tự động tải ảnh chụp và gửi thông báo trạng thái vào tài khoản hoặc nhóm chat trên nền tảng **Lark (Feishu)** thông qua một ứng dụng Bot.

Được thiết kế hiện đại, tinh tế với giao diện Glassmorphism và cực kì dễ cài đặt!

---

## 🛠 1. Tính năng nổi bật
- **Giao diện Web Hiện Đại**: Dark mode sang trọng, kính mờ (Glassmorphism), có hiệu ứng quét khuôn mặt radar và đồng hồ Real-time.
- **Tự động nhận diện khuôn mặt**: Sử dụng công nghệ AI qua OpenCV để tự động tìm và xác định khuôn mặt trong ảnh.
- **Tích hợp Lark Chatbot**: Gửi tin nhắn văn bản (Text) thông báo check-in kèm theo hình ảnh chụp (Snapshot) trực tiếp vào group chat/cá nhân qua Lark.

---

## 🤖 2. Cấu hình Bot trên Lark (Quan trọng)
Để gửi tin nhắn được vào Lark, bạn cần tạo một ứng dụng Bot và cấp quyền cho nó.

1. Truy cập trang web [Lark Developer](https://open.larksuite.com/app) và đăng nhập.
2. Nhấn **Create Custom App** để tạo một ứng dụng mới (Ví dụ đặt tên là: *AI Checkin Bot*).
3. Trong mục **Credentials & Basic Info**, copy **App ID** và **App Secret**.
4. Chọn **Features** > **Add Features** > Bật tính năng **Bot** (Add).
5. Trong mục **Permissions & Scopes**, thêm các quyền sau để Bot hoạt động:
   - `im:resource` hoặc `im:resource:upload`: Quyền upload hình ảnh lên máy chủ.
   - `im:message:send_as_bot`: Quyền cho phép Bot gửi tin nhắn.
6. **BẮT BUỘC:** Chọn **Version Management & Release** -> Nhấn **Create a Version** -> Nhấn **Save** và **Publish**. Bất kì lúc nào bạn đổi quyền, bạn đều phải tạo version mới và Publish thì hệ thống mới nhận!

---

## 💻 3. Cài đặt mã nguồn

1. Tải toàn bộ mã nguồn của kho lưu trữ này về máy.
2. Mở **Terminal** (hoặc Command Prompt / PowerShell) tại đúng thư mục mã nguồn vừa tải về.
3. Cài đặt các thư viện cần thiết bằng lệnh:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ 4. Thiết lập file cấu hình (.env)

Trong thư mục gốc, tạo một file tên là `.env`. Điền các thông tin của bạn vào file này:

```env
# CẤU HÌNH LARK BOT (Lấy từ bước 2)
LARK_APP_ID=cli_xxxxxxxxxxxxxx
LARK_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Nhập Email cá nhân của bạn, hoặc ID của Group Chat
LARK_USER_EMAIL=email_tai_khoan_lark_cua_ban@gmail.com
# LARK_CHAT_ID=oc_xxxxxxxxxxxxxxxxxxxx 
```

---

## 🏃 5. Khởi động và Sử dụng

1. Chạy lệnh sau để khởi động Backend Server (Flask):
   ```bash
   python app.py
   ```
2. Mở trình duyệt web (Chrome, Edge, Safari...) và truy cập vào đường dẫn:
   **http://127.0.0.1:5000**
3. Cấp quyền truy cập Camera cho trình duyệt (Nếu được hỏi).
4. Đứng trước camera và nhấn nút **Thực hiện Check-in**.
5. Hệ thống sẽ nhận diện khuôn mặt, chụp ảnh và gửi thông báo về Lark ngay lập tức! Chúc bạn thành công!
