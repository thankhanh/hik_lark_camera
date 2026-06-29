import requests
import json
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("LARK_APP_ID")
APP_SECRET = os.getenv("LARK_APP_SECRET")

def get_tenant_access_token():
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 0:
            return data.get("tenant_access_token")
    print("[Lark] Lỗi lấy token:", response.text)
    return None

def upload_image(token, image_path):
    url = "https://open.larksuite.com/open-apis/im/v1/images"
    headers = {'Authorization': f'Bearer {token}'}
    with open(image_path, 'rb') as f:
        image_data = f.read()
    payload = {'image_type': 'message'}
    files = [('image', (os.path.basename(image_path), image_data, 'image/jpeg'))]
    response = requests.post(url, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 0:
            return data["data"]["image_key"]
    print("[Lark] Lỗi upload ảnh:", response.text)
    return None

def send_image_message(token, receiver_email, image_key):
    # Dùng email để gửi thẳng tin nhắn cho 1 cá nhân (dễ test nhất)
    url = "https://open.larksuite.com/open-apis/im/v1/messages?receive_id_type=email"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "receive_id": receiver_email,
        "msg_type": "image",
        "content": json.dumps({"image_key": image_key})
    })
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        if response.json().get("code") == 0:
            print("[Lark] Thành công! Đã gửi tin nhắn.")
            return True
    print("[Lark] Lỗi gửi tin nhắn:", response.text)
    return False
