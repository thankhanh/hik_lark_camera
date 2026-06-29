# Tích hợp Camera Hikvision với Lark Bot 📷🚀

Dự án này là một công cụ bằng Python giúp tự động lấy ảnh chụp (snapshot) từ camera an ninh IP Hikvision thông qua giao thức ISAPI, sau đó tải bức ảnh lên và gửi tin nhắn tự động vào tài khoản hoặc nhóm chat trên nền tảng **Lark (Feishu)** thông qua một ứng dụng Bot.

Được thiết kế đơn giản, bất cứ ai (ngay cả người mới không rành về code) cũng có thể làm theo các bước dưới đây để thiết lập và chạy thành công!

---

## 🛠 1. Chuẩn bị trước khi bắt đầu
1. **Python**: Đảm bảo máy tính của bạn đã cài đặt Python (phiên bản 3.x). Bạn có thể tải tại [python.org](https://www.python.org/).
2. **Tài khoản Lark**: Một tài khoản Lark đang hoạt động để nhận tin nhắn.
3. **Camera Hikvision**: Nếu bạn muốn chạy thực tế, bạn cần biết Địa chỉ IP, Tên đăng nhập và Mật khẩu của camera (Camera và máy tính chạy code phải nằm cùng một mạng nội bộ).

---

## 🤖 2. Cấu hình Bot trên Lark (Quan trọng nhất)
Để gửi tin nhắn được vào Lark, bạn cần tạo một ứng dụng Bot và cấp quyền cho nó.

1. Truy cập trang web [Lark Developer](https://open.larksuite.com/app) và đăng nhập.
2. Nhấn **Create Custom App** để tạo một ứng dụng mới (Ví dụ đặt tên là: *Camera Bot*).
3. Sau khi tạo xong, ứng dụng của bạn sẽ có **App ID** và **App Secret** ở mục **Credentials & Basic Info**. Hãy copy 2 dòng này để lát nữa dùng.
4. Ở menu bên trái, tìm đến mục **Features** > **Add Features**. Chọn tính năng **Bot** và nhấn **Add** để bật Bot lên.
5. Ở menu bên trái, vào mục **Permissions & Scopes**, tìm và thêm các quyền (scopes) sau để Bot hoạt động được:
   - `im:resource` hoặc `im:resource:upload`: Quyền upload hình ảnh lên máy chủ của Lark.
   - `im:message:send_as_bot`: Quyền cho phép Bot gửi tin nhắn.
6. **BẮT BUỘC:** Ở menu bên trái, chọn **Version Management & Release** -> Nhấn **Create a Version** -> Nhấn **Save** và **Publish**. Bất kì lúc nào bạn đổi quyền, bạn đều phải tạo version mới và Publish thì hệ thống mới nhận!

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

Trong thư mục gốc, bạn sẽ thấy một file tên là `.env` (Nếu không có, hãy tạo một file mới đặt tên đúng như vậy). Điền các thông tin của bạn vào file này:

```env
# CẤU HÌNH CAMERA HIKVISION
CAMERA_IP=192.168.1.64
CAMERA_USER=admin
CAMERA_PASS=mat_khau_camera_cua_ban

# CẤU HÌNH LARK BOT (Lấy từ bước 2)
LARK_APP_ID=cli_xxxxxxxxxxxxxx
LARK_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LARK_USER_EMAIL=email_tai_khoan_lark_cua_ban@gmail.com
```
*Lưu ý: Bạn có thể nhập email của chính bạn để bot gửi thẳng ảnh vào tin nhắn cho bạn.*

---

## 🏃 5. Chạy thử nghiệm và Vận hành

### Bước 5.1: Chạy thử nghiệm (TEST MODE)
Để chắc chắn Bot Lark hoạt động mà không bị lỗi mạng camera, dự án này có sẵn **Chế độ TEST**.
1. Chuẩn bị một bức ảnh bất kì trong máy tính, đổi tên nó thành `test.jpg` và chép vào cùng thư mục với mã nguồn.
2. Mở file `main.py`, chắc chắn rằng dòng 11 đang ghi: `TEST_MODE = True`
3. Quay lại Terminal và chạy lệnh sau:
   *(Lưu ý: Nếu bạn dùng Windows PowerShell, hãy thêm cấu hình mã hóa trước khi chạy để tránh lỗi hiển thị tiếng Việt)*
   ```powershell
   $env:PYTHONIOENCODING="utf-8"; python main.py
   ```
   Nếu dùng MacOS/Linux hoặc CMD bình thường:
   ```bash
   python main.py
   ```
4. Nếu kết quả in ra: `=> QUY TRÌNH HOÀN TẤT THÀNH CÔNG!` thì chúc mừng bạn! Bạn hãy mở Lark lên và xem bức ảnh Bot vừa gửi.

### Bước 5.2: Chạy thực tế với Camera (REAL MODE)
Khi đã Test thành công, bạn có thể áp dụng vào thực tế với Camera!
1. Mở file `main.py`, đổi giá trị tại dòng 11 thành: `TEST_MODE = False`
2. Chạy lại lệnh trên:
   ```bash
   python main.py
   ```
Hệ thống sẽ lấy ảnh thực tế từ Camera Hikvision của bạn và đẩy lên hệ thống Lark. 

---

## 💡 Xử lý lỗi thường gặp
- **Lỗi `Access denied`**: Bạn cấp thiếu quyền cho Bot trên Lark. Vui lòng quay lại **Bước 2**, kiểm tra lại các scopes và nhớ phải **Publish version mới**.
- **Lỗi `ModuleNotFoundError`**: Bạn quên cài thư viện. Hãy chạy lệnh `pip install -r requirements.txt`.
- **Lỗi `UnicodeEncodeError`**: Xảy ra trên máy tính Windows. Cách khắc phục là chạy lệnh `$env:PYTHONIOENCODING="utf-8"` như đã hướng dẫn ở bước 5.
