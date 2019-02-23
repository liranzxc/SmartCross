from multiprocessing import Process,Manager
from time import sleep
import cv2
import numpy as np
import os
import datetime
from Utils import * 
class P(Process):
    def __init__(self,d):
        super(P, self).__init__()
        self.d = d 
        
    def run(self):
        cam = cv2.VideoCapture(self.d["src"])

        self.d["ready"] = True
        print("Process Started! Name:"+self.d["name"])
        while self.d["fulltime"]:
            grab,frame = cam.read()
            if grab:
                self.d["frame"] = frame
            #print("pulling")
           
              

        cam.release()

    def read(self):
        if self.d.get("frame") is not None and self.d["ready"]: 
                return (self.d["frame"],self.d["name"],datetime.datetime.now()) # (frame ,name,time)
        else:
                return (None,self.d["name"],datetime.datetime.now()) # (frame ,name,time)
        
        
     
             
if __name__ == '__main__':
    ## create multi camera process
    manager = Manager()
    d = createdic(manager,0,"Rogaland, Stavanger Camera")
    process = P(d)
    process.start()

    sleep(15)
    for i in range(10):
        print(process.read())
        print("sleep now")
        sleep(1)

    d["fulltime"] = False

    process.join()