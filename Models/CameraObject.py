from multiprocessing import Process, Queue,Lock,Value,Manager
import cv2
from time import sleep
def f(d,q):

    cam = cv2.VideoCapture(0)
    sleep(5)
    print(cam)
    while d["con"]:
        grabed,frame = cam.read()
        if grabed:
            q.put(frame)
            cv2.waitKey(1)
       

    cam.release()

if __name__ == '__main__':
    manager = Manager()
    d = manager.dict()
    q = manager.Queue()

    d["con"] = True
    d["src"] = 0
    
    p = Process(target=f, args=[d,q])
    p.start()
    sleep(4)
    for i in range(300):
        frame = q.get()
        print(frame)
    sleep(2)
    d["con"] = False
    p.join()