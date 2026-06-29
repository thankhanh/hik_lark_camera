import requests
from requests.auth import HTTPDigestAuth
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

CAMERA_IP = os.getenv("CAMERA_IP")
CAMERA_USER = os.getenv("CAMERA_USER")
CAMERA_PASS = os.getenv("CAMERA_PASS")

def get_snapshot(output_filename="snapshot.jpg"):
    """Lấy ảnh snapshot từ Camera qua ISAPI"""
    url = f"http://{CAMERA_IP}/ISAPI/Streaming/channels/101/picture"
    print(f"[Camera] Đang yêu cầu ảnh từ: {url}...")
    try:
        response = requests.get(
            url, 
            auth=HTTPDigestAuth(CAMERA_USER, CAMERA_PASS), 
            stream=True, 
            timeout=10
        )
        if response.status_code == 200:
            with open(output_filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"[Camera] Thành công! Đã lưu ảnh: {output_filename}")
            return output_filename
        else:
            print(f"[Camera] Lỗi HTTP: {response.status_code}")
            return None
    except Exception as e:
        print(f"[Camera] Lỗi kết nối: {e}")
        return None
