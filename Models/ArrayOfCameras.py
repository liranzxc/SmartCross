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
    sources = [
    "http://193.251.18.40:8001/mjpg/video.mjpg","http://187.157.229.132/mjpg/video.mjpg",
    "http://118.243.204.173/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER",
    "http://46.252.143.150/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER",
    "http://162.245.149.145/mjpg/video.mjpg",
    "http://90.176.96.128/img/video.mjpeg",
    "http://185.2.241.221:8090/mjpg/video.mjpg",
    "http://174.6.126.86/mjpg/video.mjpg"
    
     ] ## list of source of camera 

    for s in sources: ## create dics with sources
        dics.append(createdic(manager,s))

    for d in dics: ## create process with dics
        process.append(P(d))

    for p in process: ## start process
        p.start()

    sleep(5)

    ## sample of image
    for i in range(3000):
        for p in process:
            try:
                cv2.imshow("frame"+str(p),p.read())
                cv2.waitKey(1)
            except:
                pass
           

    ## shutting off
    for d in dics:
        d["fulltime"] = False

    for p in process:
        p.join()

    print("stopped")
    cv2.destroyAllWindows()

    

    

    


