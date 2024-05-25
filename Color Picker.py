import cv2
import numpy as np

# Thiết lập chiều rộng và chiều cao khung hình
frameWidth = 640
frameHeight = 480

# Mở webcam
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)  # Đặt chiều rộng của khung hình
cap.set(4, frameHeight)  # Đặt chiều cao của khung hình

# Hàm rỗng để sử dụng với trackbars
def empty(a):
    pass

# Tạo cửa sổ chứa các thanh điều chỉnh (trackbars) để điều chỉnh giá trị HSV
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

while True:
    success, img = cap.read()  # Đọc hình ảnh từ webcam
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Chuyển đổi ảnh sang không gian màu HSV

    # Lấy các giá trị từ trackbars
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    print(h_min)

    # Đặt ngưỡng cho các giá trị HSV
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)  # Tạo mask
    result = cv2.bitwise_and(img, img, mask=mask)  # Áp dụng mask để lấy phần ảnh theo ngưỡng

    # Chuyển đổi mask sang BGR để hiển thị
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, result])  # Chồng các ảnh lên nhau theo chiều ngang
    cv2.imshow('Horizontal Stacking', hStack)  # Hiển thị ảnh chồng

    # Nhấn phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Giải phóng camera
cv2.destroyAllWindows()  # Đóng tất cả cửa sổ hiển thị
