import os
from multiprocessing import Manager, Process
from time import sleep

import cv2
import numpy as np

from Camera import P
from Utils import *


if __name__ == '__main__':

    ## create multi camera process
    manager = Manager()
    process = [] 
    dics = []
    sources = [
    "http://90.176.96.128/img/video.mjpeg",
    "http://185.2.241.221:8090/mjpg/video.mjpg",
    "http://174.6.126.86/mjpg/video.mjpg",
    "http://93.157.18.93:8083/oneshotimage1?1550665664",
    "http://160.218.245.169:8080/snap.jpg?JpegSize=M&JpegCam=1&r=1550665077"

    
     ] ## list of source of camera 

    for s in sources: ## create dics with sources
        dics.append(createdic(manager,s))

    for d in dics: ## create process with dics
        process.append(P(d))

    for p in process: ## start process
        p.start()

    ## wait for all request https from all process  
    sleep(5)

    ## sample of image
    
    print("here before")
    list(map(Show,process)) ## each process return a image and display her
    sleep(2)

    frames = grabFrames(process)
    print(len(frames))

   
    ## shutting off
    for d in dics:
        d["fulltime"] = False

    for p in process:
        p.join()

    print("stopped")
    cv2.destroyAllWindows()

    

    

    


