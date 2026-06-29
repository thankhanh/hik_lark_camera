from camera_service import get_snapshot
from lark_service import get_tenant_access_token, upload_image, send_image_message
import os

def main():
    print("="*40)
    print(" BẮT ĐẦU QUY TRÌNH CHỤP VÀ GỬI ẢNH ")
    print("="*40)
    
    # [TESTING MODE] - Đặt cờ này thành True để test Lark Bot mà không cần Camera
    TEST_MODE = True

    if not TEST_MODE:
        saved_path = get_snapshot("snapshot.jpg")
        if not saved_path:
            return
    else:
        print("\n[Hệ thống] Chế độ TEST: Bỏ qua lấy ảnh từ camera.")
        saved_path = "test.jpg"
        if not os.path.exists(saved_path):
            print(f"[Lỗi] Vui lòng copy một tấm ảnh bất kỳ vào thư mục và đặt tên là 'test.jpg' để test gửi lên Lark!")
            return

    print("\n[Hệ thống] Đang lấy token Lark...")
    token = get_tenant_access_token()
    if not token:
        return

    print(f"\n[Hệ thống] Đang tải ảnh '{saved_path}' lên Lark...")
    image_key = upload_image(token, saved_path)
    if not image_key:
        return

    print(f"\n[Hệ thống] Tiến hành gửi ảnh...")
    receiver_email = os.getenv("LARK_USER_EMAIL")
    if send_image_message(token, receiver_email, image_key):
        print("\n=> QUY TRÌNH HOÀN TẤT THÀNH CÔNG!")

if __name__ == "__main__":
    main()
