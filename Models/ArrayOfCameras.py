from  Camera import P
from multiprocessing import Process,Manager
from time import sleep
import cv2
import numpy as np
import os

def createdic(manager,src):
    d = manager.dict()
    d["src"] = src
    d["fulltime"] = True
    return d


if __name__ == '__main__':

    ## create multi camera process
    manager = Manager()
    process = [] 
    dics = []
    sources = [0,1,"http://192.168.1.17:8080/video"]

    for s in sources: ## create dics with sources
        dics.append(createdic(manager,s))

    for d in dics: ## create process with dics
        process.append(P(d))

    for p in process: ## start process
        p.start()

    sleep(2)

    ## sample of image
    for p in process:
        cv2.imshow("frame"+str(p),p.read())
        cv2.waitKey(1)
        sleep(3)

    ## shutting off
    for d in dics:
        d["fulltime"] = False

    for p in process:
        p.join()

    cv2.waitKey(0)

    

    


