import cv2
import numpy as np

#def warp_perspective(img, src_pts, dst_pts, size):
#    M = cv2.getPerspectiveTransform(np.float32(src_pts), np.float32(dst_pts))
#    return cv2.warpPerspective(img, M, size)

img = cv2.imread('hwRoad1.png')  # 開啟圖片，預設使用 cv2.IMREAD_COLOR 模式

ww, hh, rh, r = 640, 400, 0.6, 3
xx1, yy1, xx2, yy2 = int(ww * 0.4), int(hh * rh), int(ww * 0.6), int(hh * rh)
p1, p2, p3, p4 = [r + 71, hh - r], [ww - r - 80, hh - r], [xx2 - 80, yy2], [xx1 + 55, yy2]

img1 = cv2.resize(img, (ww, hh))  # 產生 640x400 的圖

output = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
cv2.imshow('oxxostudio', output)
cv2.waitKey(0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
output = cv2.dilate(output, kernel)  # 膨脹
cv2.imshow('oxxostudio', output)
cv2.waitKey(0)

output = cv2.GaussianBlur(output, (5, 5), 0)  # 指定區域單位為 (5,5) 模糊化，去除雜訊
cv2.imshow('oxxostudio', output)
cv2.waitKey(0)

output = cv2.erode(output, kernel)  # 侵蝕，將白色小圓點移除
cv2.imshow('oxxostudio', output)
cv2.waitKey(0)

output = cv2.Canny(output, 150, 200)  # 偵測邊緣150 200
cv2.imshow('oxxostudio', output)
cv2.waitKey(0)

# ROI: Region Of Interest (關注區域)
zero = np.zeros((hh, ww, 1), dtype='uint8')  # ROI
area = [p1, p2, p3, p4]  # bottom left, bottom right, upper right, upper left
pts = np.array(area)
zone = cv2.fillPoly(zero, [pts], 255)
output1 = cv2.bitwise_and(output, zone)  # 使用 bitwise_and
cv2.imshow('oxxostudio_1', output1)
cv2.waitKey(0)

HOUGH_THRESHOLD, HOUGH_MIN_LINE_LENGTH, HOUGH_MAX_LINE_GAP = 40, 15, 70
lines = cv2.HoughLinesP(output1, 1, np.pi / 180, HOUGH_THRESHOLD, None, HOUGH_MIN_LINE_LENGTH, HOUGH_MAX_LINE_GAP)
done, s1, s2, b1, b2 = 0, 0, 0, 0, 0
img2 = img1.copy()
co = (255, 0, 0)

if lines is not None:
    for i in range(0, len(lines)):
        l = lines[i][0]
        x1, y1, x2, y2 = l[0], l[1], l[2], l[3]
        # 計算直線的斜率與截距
        s = (y2 - y1) / (x2 - x1)  # s = slope
        b = y1 - s * x1  # y = s * x + b
        if min(x1, x2) < 30 or max(x1, x2) > ww - 30:
            continue
        if s < 0 and s < s1:
            done = done | 1
            s1, b1 = s, b
        if s > 0 and s > s2:
            done = done | 2
            s2, b2 = s, b
        if done == 3:
            y1, y2 = hh-r, hh-hh*0.175
            x = (int)(((y1-b1)/s1 + (y1-b2)/s2)/2)
            if abs(x-(int(ww/2)-1)) > 45: co = (0, 0, 255)
            cv2.line(img2, (x, y1), (x, y1-15), co, 2)
            p1 = [(int)((y1-b1)/s1), (int)(y1)]
            p2 = [(int)((y2-b1)/s1), (int)(y2)]
            p3 = [(int)((y1-b2)/s2), (int)(y1)]
            p4 = [(int)((y2-b2)/s2), (int)(y2)]
            area = [p1, p2, p4, p3]
            # print(p1)
            # print(p2)
            # print(p3)
            # print(p4)
            # 透視變換，獲取鳥瞰視角
            zero = np.zeros((hh, ww, 3), dtype='uint8')

            pts = np.array(area)
            mask = cv2.fillPoly(zero, [pts], (0, 50, 0))
            img2 = cv2.addWeighted(img2,1.0, mask,1.0, 0)

            area = np.float32([p2,p1,p3])
            a2 = np.float32([[ww/2,hh],[ww/2,hh*2],[ww,hh*2]])
            M = cv2.getAffineTransform(area, a2)
            output = cv2.warpAffine(img2, M, (hh*2, ww*2))
            cv2.imshow('oxxostudio', output) ; cv2.waitKey(0)
    cv2.imshow('oxxostudio_2', output) ; cv2.waitKey(0)


x, y = int(ww/2)-1, hh-r
cv2.line(img2, (x, y), (x, y-12), (255,0,0), 2)

for i in range(1,10):
    x, y = int(ww/2)-1, hh-r
    cv2.line(img2, (x-i*15, y), (x-i*15, y-3), (0,255,0), 2)
    cv2.line(img2, (x+i*15, y), (x+i*15, y-3), (0,255,0), 2)

cv2.imshow('oxxostudio_3', img2) ; cv2.waitKey(0)
cv2.destroyAllWindows()

