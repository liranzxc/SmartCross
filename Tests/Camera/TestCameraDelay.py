import cv2
import numpy as np 




cam = cv2.VideoCapture("http://156.110.54.197/oneshotimage1?1550950007")
from time import sleep

sleep(10)
_,frame = cam.read()
cv2.imshow("fram",frame)

cv2.waitKey(0)
print("finish")
cam.release()