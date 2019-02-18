from multiprocessing import Process,Manager
from time import sleep
import cv2
import numpy as np
import os
class P(Process):
    def __init__(self,d):
        super(P, self).__init__()
        self.d = d 
        
    def run(self):
        cam = cv2.VideoCapture(self.d["src"])
        while self.d["fulltime"]:
           grab,frame = cam.read()
           self.d["frame"] = frame
           print("pulling forever")

    def read(self):
        return self.d["frame"]

        


if __name__ == '__main__':
    manager = Manager()
    d = manager.dict()
    d["src"] = "http://192.168.1.17:8080/video"
    d["fulltime"] = True
    process = P(d)
    process.start()
    sleep(2)

    for i in range(5):
        cv2.imshow("frame"+str(i),process.read())
        cv2.waitKey(1)
        print("Capture now ! reset !")
        sleep(3)

    d["fulltime"] = False 

    process.join()

    
    
   