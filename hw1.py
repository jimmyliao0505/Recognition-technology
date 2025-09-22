import cv2
import datetime
import time
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
# 获取视频宽度
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# 获取视频高度
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#文字坐标
word_x = int(frame_width / 10)
word_y = int(frame_height / 10)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')          # 設定影片的格式為 MJPG
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width,  frame_height))  # 產生空的影片
fps = 0
# 初始化計數器
frame_count = 0
start_time = time.time()
elapsed_time = 1
while True:
    ret, frame = cap.read()             # 讀取影片的每一幀
    frame_count += 1
    time_text = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    cv2.putText(frame, time_text, (word_x,word_y),cv2.FONT_HERSHEY_SIMPLEX,1,(100,255,250),2)
    # 計算FPS
    elapsed_time = time.time() - start_time
    if elapsed_time >=1:
        start_time = time.time()
        fps = frame_count / elapsed_time
        frame_count = 0
    cv2.putText(frame, f"FPS: {float(fps)}", (word_x,word_y+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    if not ret:
        print("Cannot receive frame")   # 如果讀取錯誤，印出訊息
        break
    out.write(frame)       # 將取得的每一幀圖像寫入空的影片
    cv2.imshow('real_time', frame)     # 如果讀取成功，顯示該幀的畫面
    if cv2.waitKey(1) == ord('q'):      # 每一毫秒更新一次，直到按下 q 結束
        break

cap.release()                           # 所有作業都完成後，釋放資源
out.release()
cv2.destroyAllWindows()                 # 結束所有視窗
