import cv2
import numpy as np

# Thiết lập chiều rộng và chiều cao khung hình
frameWidth = 640
frameHeight = 480

# Mở webcam
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)  # Đặt chiều rộng của khung hình
cap.set(4, frameHeight)  # Đặt chiều cao của khung hình
cap.set(10, 150)  # Đặt độ sáng của khung hình

# Định nghĩa các giá trị màu HSV để phát hiện các màu cụ thể
myColors = [[5, 107, 0, 19, 255, 255],
            [133, 56, 0, 159, 156, 255],
            [57, 76, 0, 100, 255, 255],
            [90, 48, 0, 118, 255, 255]]

# Định nghĩa các giá trị màu BGR để vẽ
myColorValues = [[51, 153, 255],  # Màu xanh da trời
                 [255, 0, 255],   # Màu hồng
                 [0, 255, 0],     # Màu xanh lá cây
                 [255, 0, 0]]     # Màu đỏ

# Tọa độ của các điểm đã vẽ
myPoints = []  # [x, y, colorId]

# Hàm để tìm và vẽ các điểm màu được phát hiện
def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Chuyển đổi ảnh sang không gian màu HSV
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)  # Tạo mask
        x, y = getContours(mask)  # Lấy tọa độ các đường viền
        cv2.circle(imgResult, (x, y), 15, myColorValues[count], cv2.FILLED)  # Vẽ vòng tròn tại tọa độ
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
    return newPoints

# Hàm để lấy tọa độ các đường viền
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y

# Hàm để vẽ lên canvas
def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()  # Đọc hình ảnh từ webcam
    imgResult = img.copy()  # Tạo bản sao của ảnh gốc
    newPoints = findColor(img, myColors, myColorValues)  # Tìm các điểm màu
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)  # Vẽ các điểm màu lên canvas

    cv2.imshow("Result", imgResult)  # Hiển thị ảnh kết quả
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Nhấn phím 'q' để thoát
        break

cap.release()  # Giải phóng camera
cv2.destroyAllWindows()  # Đóng tất cả cửa sổ hiển thị
