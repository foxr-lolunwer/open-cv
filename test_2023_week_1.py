"""
Participating members: foxr lolunwer
Time: 2023/9/14 - 2023/9/16
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
import time


def mouse_record(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        mouse_pos.append((x, y))
    if len(mouse_pos) > 3:
        del mouse_pos[0]


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
    print(mouse_pos)
    len_pos = len(mouse_pos)
    if len_pos % 3 == 0 and len_pos != 0:
        cv.line(frame, mouse_pos[-3], mouse_pos[-2], (255, 0, 0), 5)
        cv.line(frame, mouse_pos[-3], mouse_pos[-1], (255, 0, 0), 5)
        cv.line(frame, mouse_pos[-2], mouse_pos[-1], (255, 0, 0), 5)
    elif len_pos % 2 == 0 and len_pos != 0:
        cv.line(frame, mouse_pos[-2], mouse_pos[-1], (255, 0, 0), 5)
    for i in mouse_pos:
        cv.circle(frame, i, 2, (0, 0, 255), -1)
    cv.imshow("image", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# 当所有事完成，释放 VideoCapture 对象
cap.release()
cv.destroyAllWindows()
