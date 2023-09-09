import cv2 as cv
# import numpy as np

START = 0    # 修改检测阈值
END = 3      # 修改容错率


def circle_detect(image):
    global flag, count_start, count_end, detect_list
    # 灰度化/自适应阈值/反转图像/高斯模糊
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 13, 2)
    gray = cv.GaussianBlur(gray, (17, 17), 0)

    # 输出图像大小，方便根据图像大小调节minRadius和maxRadius
    # print(image.shape)
    # 霍夫变换圆检测
    paraml2 = 120
    # 参数说明可以见：http://www.juzicode.com/opencv-python-houghcircles/
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1.5, 200, param1=300, param2=paraml2, minRadius=10,
                              maxRadius=250)
    # 如果检测到圆
    if circles is not None:
        # print(circles)
        for circle in circles[0]:
            # 圆的基本信息
            # print(circle[2])
            x = int(circle[0])
            y = int(circle[1])
            r = int(circle[2])
            print("|pos:(%d, %d, %d)|" % (x, y, r), end="")
            # 在原图用指定颜色标记出圆的边界
            cv.circle(image, (x, y), r, (0, 0, 0), 3)
            # 画出圆的圆心
            cv.circle(image, (x, y), 5, (0, 0, 0), -1)
            if flag == 0:
                detect_list.append((x, y, r))
                count_start += 1
                if count_start >= START:
                    flag = 1
                    count_start = 0
            else:
                print("\n-" + str(detect_list) + "-")
                for i in range(len(detect_list)):
                    # 防止内存溢出
                    if len(detect_list) >= 10:
                        detect_list = []
                        flag = 0
                        count_end = 0
                        cv.imshow("circles_demo", image)
                        return
                    if abs(x - detect_list[i][0] < 10) and abs(y - detect_list[i][1] < 10) and abs(r - detect_list[i][2] < 10):
                        del detect_list[i]
                        detect_list.append((x, y, r))
                        print("real pos: (%d, %d)" % (x, y))
                        # 在原图用指定颜色标记出圆的边界
                        cv.circle(image, (x, y), r, (0, 0, 255), 3)
                        # 画出圆的圆心
                        cv.circle(image, (x, y), 5, (0, 255, 0), -1)
                        # 在原图用指定颜色标记出圆的边界
                        cv.circle(gray, (x, y), r, (0, 0, 255), 3)
                        # 画出圆的圆心
                        cv.circle(gray, (x, y), 5, (0, 255, 0), -1)
                    else:
                        if count_end >= END:
                            count_end = 0
                            flag = 0
                            detect_list = []
                            return
                        count_end += 1
    else:
        flag = 0
        detect_list = []
        print("-None-")

    cv.imshow("circles_image", image)
    cv.imshow("circles_gray", gray)


flag = 0                       # 检测标志，当为零时代表重新开始检测，直到检测出连续结果时变为1
count_start = START            # 检测阈值，当连续n次均监测到圆形时，flag = 1 开始检测，阈值越大，开始进行检测的标准越严格，默认为0
count_end = END                # 容错率，当连续n次圆检测没有连续结果时，flag = 0 重置检测
detect_list = []               # 存储上次检测结果，与此次结果比对，判断结果是否连续
cap = cv.VideoCapture(0)
while True:
    # 一帧一帧捕捉
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    # 我们对帧的操作在这里
    circle_detect(frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# 当所有事完成，释放 VideoCapture 对象
cap.release()
cv.destroyAllWindows()
