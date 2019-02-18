from multiprocessing import Process,Manager
from time import sleep
import cv2
import numpy as np
class P(Process):
    def __init__(self,d,fulltime,pulling):
        super(P, self).__init__()
        self.d = d
        self.fulltime = fulltime
        self.pulling = pulling
        
    def run(self):
        cam = cv2.VideoCapture(self.d["src"])
        i = 0
        while self.d["fulltime"]:
            grab , img = cam.read()
            self.fulltime.put(img)

            if self.d["lock"]:
                self.pulling.put(img)
                self.d["lock"] =  False
            print("pulling"+str(i))
            i +=1
        
    
    
           
            
                

        
        cam.release()


        


if __name__ == '__main__':
    manager = Manager()
    d = manager.dict()
    fulltime = manager.Queue()
    pulling = manager.Queue()

    d["src"] = 0
    d["fulltime"] = True
    d["lock"] = False

    p = P(d,fulltime,pulling)
    p.start()

    while True:
       pass

    # for i in range(30):
    #     d["lock"]= True
    #     while pulling.empty():
    #        pass
    #     frame = pulling.get()
    #     cv2.imshow("frame"+str(i),frame)
    #     cv2.waitKey(1)
    #     sleep(30)

    d["fulltime"] = False
    p.join()
    cv2.waitKey(0)
   