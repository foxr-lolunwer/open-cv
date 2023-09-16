"""
Participating members: foxr lolunwer
Time: 2023/9/14 - 2023/9/16
Ver: -1.2 (2023/9/16)
     -1.1 (2023/9/14)
     -1.0 (2023/9/14)
Test:
- Use the mouse to select three points in sequence.
  These three points form a triangle.
  The triangle is drawn in the picture captured by the camera.
Target:
- Ability to shoot with camera
- Ability to draw simple points, lines, circles, and rectangles
- Mouse operation (for completing the test)
"""

import cv2 as cv
import numpy as np
import time


def mouse_record(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        mouse_pos.append((x, y))
    # 如果绘制超过10个三角形，强制重绘
    if len(mouse_pos) > 30:
        mouse_pos.clear()
        mouse_pos.append((x, y))


# if __name__ == "__main__":
mouse_pos = []
cap = cv.VideoCapture(0)
cv.namedWindow('image')
ret, frame = cap.read()
cv.setMouseCallback("image", mouse_record)
while True:
    time.sleep(0.05)  # 帧率（1/n），默认为0.05（20帧）
    # 一帧一帧捕捉
    ret, frame = cap.read()

    # 我们对帧的操作在这里
    frame = cv.flip(frame, 1)
    # print(mouse_pos)
    len_pos = len(mouse_pos)
    if len_pos:
        k = len_pos % 3
        print(k)
        # 如果坐标列表长度大于三，绘制三角形
        if len_pos >= 3:
            for i in range(1, len_pos // 3 + 1):
                pos = np.array([mouse_pos[3 * i - 3], mouse_pos[3 * i - 2], mouse_pos[3 * i - 1]])
                frame = cv.polylines(frame, np.int32([pos]), 1, (100, 100, 255), 5)
        # 坐标列表除3余二时，绘制线
        if k == 2:
            frame = cv.line(frame, mouse_pos[-2], mouse_pos[-1], (255, 100, 100), 5)
    # 绘制所有点
    for i in mouse_pos:
        cv.circle(frame, i, 2, (0, 0, 255), -1)
    cv.imshow("image", frame)
    # 按'q'键退出，'r'键重绘，'b'键撤销
    key = cv.waitKey(1)
    if key == ord('r'):
        mouse_pos.clear()
    elif key == ord('b'):
        # 预防访问超限
        if len_pos > 0:
            del mouse_pos[-1]
    elif key == ord('q'):
        break

# 当所有事完成，释放 VideoCapture 对象
cap.release()
cv.destroyAllWindows()
