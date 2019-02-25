import cv2
import numpy
import random
import time
def Show(frameT):
    frame,name,time = frameT
    try:
        cv2.imshow("Camera: "+name,frame) # for update frames 
        #cv2.imshow("Camera: "+name+"  -  time: "+str(time),frame) # for image each frame
        cv2.waitKey(1)
    except:
        print("error in show method in process ")
        
            

def createdic(manager,src,CameraName):
        d = manager.dict()
        d["src"] = src
        d["name"] = CameraName
        d["fulltime"] = True
        d["ready"] = False

        return d


def grabFrames(p):
    frame,name,time = p.read()
    if frame is not None:
        return (frame,name,time)
    else:
        return (None,name,time)


def Output_Method(outputQueue):
        while True:
                results = outputQueue.get()
                if results is None:
                        break
                else:
                        print(results)