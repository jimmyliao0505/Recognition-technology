import cv2
import numpy as np

def process_frame(frame):
    # 轉為灰階
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 邊緣偵測
    edges = cv2.Canny(blur, 50, 150)
    
    # 定義ROI區域 (方形區域)
    height, width = frame.shape[:2]
    mask = np.zeros_like(edges)
    region = np.array([[
        (width // 4, height * 3 // 4),
        (width * 3 // 4, height * 3 // 4),
        (width * 3 // 4, height),
        (width // 4, height)
    ]], dtype=np.int32)
    cv2.fillPoly(mask, region, 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    
    # Hough 轉換偵測線段
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=200)
    left_lines, right_lines = [], []
    lane_mask = np.zeros_like(frame)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0] 
            slope = (y2 - y1) / (x2 - x1 + 1e-6)
            
            if slope < -0.5:
                y1 = height
                x1 = width//2-350    #避免左側最接近車輛處無虛線時偵測不出來(強制從左下車輛處開始繪製)
                left_lines.append((x1, y1, x2, y2))
            elif slope > 0.5:
                y2 = height
                x2 = width//2+230    #避免右側最接近車輛處無虛線時偵測不出來(強制從右下車輛處開始繪製)
                right_lines.append((x1, y1, x2, y2))
    
    # 繪製車道線並填充區域
    lane_overlay = np.zeros_like(frame)
    for line in left_lines + right_lines:
        x1, y1, x2, y2 = line
        cv2.line(lane_overlay, (x1, y1), (x2, y2), (0, 255, 0), 3)
    
    # 填充車道線之間的區域
    if left_lines and right_lines:
        left_points = [(x1, y1) for x1, y1, x2, y2 in left_lines] + [(x2, y2) for x1, y1, x2, y2 in reversed(left_lines)]
        right_points = [(x1, y1) for x1, y1, x2, y2 in right_lines] + [(x2, y2) for x1, y1, x2, y2 in reversed(right_lines)]
        lane_area = np.array(left_points + right_points, dtype=np.int32)
        cv2.fillPoly(lane_overlay, [lane_area], (0, 255, 0))
    
    # 疊加填充的區域
    frame = cv2.addWeighted(lane_overlay, 0.5, frame, 1, 0)

    # 計算車道中心
    lane_center_x = width // 2
    if left_lines and right_lines:
        left_x = np.mean([line[0] for line in left_lines] + [line[2] for line in left_lines])
        right_x = np.mean([line[0] for line in right_lines] + [line[2] for line in right_lines])
        lane_center_x = int((left_x + right_x) / 2)
    
    # 車輛中心 (假設為畫面中心)
    vehicle_center_x = width // 2

    # 繪製車道中心與車輛中心
    cv2.line(frame, (lane_center_x, height - 50), (lane_center_x, height - 30), (255, 0, 0), 3)
    cv2.line(frame, (vehicle_center_x, height - 50), (vehicle_center_x, height - 30), (0, 0, 255), 3)
    
    return frame

def main(video_path):
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_frame = process_frame(frame)
        cv2.imshow("Lane Detection", processed_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 執行程式
video_path = "LaneVideo.mp4"
main(video_path)
