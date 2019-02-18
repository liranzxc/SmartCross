import multiprocessing
import cv2
from multiprocessing import freeze_support,Manager
queue_from_cam = multiprocessing.Queue()
from time import sleep

def cam_loop(queue_from_cam,d):
    cap = cv2.VideoCapture(d["src"])
    while d["con"]:
        hello, img = cap.read()
        queue_from_cam.put(img)
        print("pulling")
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    cap.release()

if __name__ == '__main__':
    freeze_support()
    manager = Manager()
    d = manager.dict()
    q = manager.Queue()

    d["con"] = True
    d["src"] = 0

    cam_process = multiprocessing.Process(target=cam_loop,args=(q,d))
    cam_process.start()

    while q.empty():
        pass

    
    while True:
        from_queue = q.get()
        cv2.imshow('temp.png', from_queue)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    d["con"] = False
    

   
