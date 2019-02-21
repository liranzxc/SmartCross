import os
import sys
from multiprocessing import Manager, Process
from time import sleep


from yolodata.Detector import DetectorOBJ

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
    0,1
   
    
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
    
    #print("here before")
    #list(map(Show,process)) ## each process return a image and display her
    #sleep(2)

    frames = grabFrames(process)
    print(len(frames))

    ## detection
    dr = manager.dict()
    dr["images"] = frames
    k = DetectorOBJ(dr) ## need to import Detector
    k.start() ## start detection

    k.join()

    print(dr["results"])
   
    ## shutting off
    for d in dics:
        d["fulltime"] = False

    for p in process:
        p.join()

    print("stopped")
    cv2.destroyAllWindows()

    

    

    


