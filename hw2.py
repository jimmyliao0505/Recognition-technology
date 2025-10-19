import cv2
import numpy as np

# 你指定的 RGB 顏色轉成 BGR
target_bgr = (45, 46, 166)
tolerance = 20

lower = np.array([max(0, target_bgr[0] - tolerance),
                  max(0, target_bgr[1] - tolerance),
                  max(0, target_bgr[2] - tolerance)])

upper = np.array([min(255, target_bgr[0] + tolerance),
                  min(255, target_bgr[1] + tolerance),
                  min(255, target_bgr[2] + tolerance)])

# 開啟攝影機
cap = cv2.VideoCapture(0)

# 取得畫面尺寸
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 設定影片儲存參數
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output1.mp4', fourcc, 20.0, (frame_width,  frame_height))

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        break

    # 建立遮罩 + 過濾
    mask = cv2.inRange(frame, lower, upper)
    output = cv2.bitwise_and(frame, frame, mask=mask)

    # 顯示與儲存
    cv2.imshow('oxxostudio', output)
    out.write(output)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
