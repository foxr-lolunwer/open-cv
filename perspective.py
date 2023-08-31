import cv2
import numpy as np

img = cv2.imread("perspective.png")
height, width = img.shape[:2]
# 变换前的四个点
srcArr = np.float32([[0, 0], [400, 0], [0, 400], [400, 400]])
# 变换后的四个点
dstArr = np.float32([[100, 100], [300, 100], [0, 400], [400, 400]])
# 获取变换矩阵
MM = cv2.getPerspectiveTransform(srcArr, dstArr)
dst = cv2.warpPerspective(img, MM, (width, height))
# 查看成果
cv2.imshow("l.png", img)
cv2.imshow("pe.png", dst)
cv2.waitKey(0)
