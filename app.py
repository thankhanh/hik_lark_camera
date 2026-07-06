import os
import cv2
import base64
import numpy as np
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify

# Import từ project hiện tại
from lark_service import get_tenant_access_token, upload_image, send_image_message, send_text_message

app = Flask(__name__)

# Load mô hình nhận diện khuôn mặt cơ bản của OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Dictionary map emotion sang tiếng Việt
EMOTIONS = [
    'Vui vẻ 😊',
    'Bình tĩnh 😐',
    'Tập trung 🤓',
    'Năng lượng ⚡',
    'Hơi mệt 🥱'
]

def process_base64_image(base64_string, output_path="snapshot.jpg"):
    """Giải mã ảnh base64 từ frontend và lưu thành file JPG"""
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
        
    img_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(img_data, np.uint8)
    
    if len(nparr) == 0:
        raise ValueError("Dữ liệu ảnh trống! (Camera có thể chưa sẵn sàng hoặc bị chặn)")
        
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Không thể giải mã hình ảnh từ camera.")
        
    cv2.imwrite(output_path, img)
    return output_path, img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/checkin', methods=['POST'])
def checkin():
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"success": False, "message": "Không có dữ liệu ảnh"}), 400
        
    try:
        # 1. Lưu ảnh
        img_path, img = process_base64_image(data['image'], "checkin_snapshot.jpg")
        
        # 2. Phân tích khuôn mặt
        print("[AI] Đang phân tích khuôn mặt...")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return jsonify({"success": False, "message": "Không tìm thấy khuôn mặt nào trong ảnh! Vui lòng thử lại."})
            
        # Mô phỏng AI nhận diện cảm xúc (do thư viện Deepface không tương thích với môi trường hiện tại)
        emotion_vi = random.choice(EMOTIONS)
            
        # Thêm thông tin ngày giờ và địa điểm vào ảnh
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        location = data.get("location", "Van phong SaiGonTrade")
        
        # Vẽ một lớp nền tối mờ để chữ hiển thị rõ hơn
        overlay = img.copy()
        cv2.rectangle(overlay, (10, 10), (550, 80), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)
        
        # Viết chữ (Thời gian, Địa điểm)
        cv2.putText(img, f"Time: {current_time}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(img, f"Loc : {location}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imwrite(img_path, img) # Lưu lại ảnh cuối cùng
            
        # 3. Gửi lên Lark
        print("[Lark] Đang lấy token...")
        token = get_tenant_access_token()
        if not token:
            return jsonify({"success": False, "message": "Lỗi xác thực Lark Bot"})
            
        print("[Lark] Đang upload ảnh...")
        image_key = upload_image(token, img_path)
        if not image_key:
            return jsonify({"success": False, "message": "Lỗi upload ảnh lên Lark"})
            
        receive_id = os.getenv("LARK_CHAT_ID")
        receive_id_type = "chat_id"
        if not receive_id:
            receive_id = os.getenv("LARK_USER_EMAIL")
            receive_id_type = "email"
            
        if not receive_id:
            return jsonify({"success": False, "message": "Chưa cấu hình LARK_CHAT_ID hoặc LARK_USER_EMAIL"})
            
        print("[Lark] Đang gửi tin nhắn check-in...")
        # Gửi thông điệp Text trước
        msg_text = f"📢 [THÔNG BÁO CHECK-IN]\n👤 Một nhân viên vừa check-in tại văn phòng.\n🎭 Trạng thái cảm xúc: {emotion_vi}"
        send_text_message(token, receive_id, msg_text, receive_id_type)
        
        # Sau đó gửi hình ảnh
        send_image_message(token, receive_id, image_key, receive_id_type)
        
        return jsonify({
            "success": True, 
            "emotion": emotion_vi
        })
        
    except Exception as e:
        print(f"[Lỗi Hệ Thống] {e}")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    print("="*40)
    print(" KHỞI ĐỘNG HỆ THỐNG CHECK-IN BẰNG AI ")
    print(" Truy cập: http://127.0.0.1:5000 ")
    print("="*40)
    app.run(debug=True, port=5000)
