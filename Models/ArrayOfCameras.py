import os
import sys
sys.path.append("B:\SmartCross\Models\yolodata") ## change to folder with detector path
from multiprocessing import Manager, Process
from time import sleep
from Detector import DetectorOBJ
import cv2
import numpy as np
from Camera import P
from Utils import *


if __name__ == '__main__':
    ## create multi camera process
    
    manager = Manager()
    queue = manager.Queue()
    queue_output = manager.Queue()

    ## detection
    config_path= "B:\SmartCross\Models\yolodata\config.json" # change to your path config
    k = DetectorOBJ(queue,queue_output,config_path) ## need to import Detector
    k.start() ## start detection

    outputprocess = Process(target=Output_Method,args=(queue_output,))
    outputprocess.start()

    process = [] 
    dics = []
    sources = [

        
        ("Fronted Camera",0)#("Second Camera",1),
        #("Movie",r"B:\Earthcam\crossing.mkv")
        #("Phone  camera","http://192.168.1.5:8080/video")
        #("Rogaland","http://195.1.188.76/mjpg/video.mjpg"),
        #("Tokyo, Tokyo","http://118.243.204.173/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER"),
        #("Madrid, Paracuellos De Jaram","http://46.24.35.53/mjpg/video.mjpg"),
        #("Kuala Lumpur","http://58.26.96.56/mjpg/video.mjpg")
        #("Fast Roading Road","http://138.188.42.155:88/mjpg/video.mjpg"),
        #("Morelos","http://187.157.229.132/mjpg/video.mjpg")
        #("Mobotix camera ","http://50.246.145.122/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER"),
        #("Oklahoma, Fort Cobb ","http://156.110.54.197/oneshotimage1?1550950007"),
        #("Bristol","http://69.27.83.101/oneshotimage1?1550950433"),
        #("Geneve","http://138.188.42.155:88/mjpg/video.mjpg")
    
    
     ] ## list of source of camera 

    for s in sources: ## create dics with sources
        name , src = s
        dics.append(createdic(manager,src,name))

    for d in dics: ## create process with dics
        process.append(P(d))

    for p in process: ## start process
        p.start()

    

    ## wait for all request https from all process  
    #print("sleep for 15 seconds - loading all camera ")
    #waiting_time = time.time()
    while(any(d["ready"] == False for d in dics)):
        pass
        #print("waiting...")
      #  sleep(1)
    #print("Waiting Time is "+str(time.time() - waiting_time))
    #sleep(5)

    print("started")

   
    for i in range(15):
        framesTls = []
        framesTls = list(map(grabFrames,process))
        
        frames,names,times = zip(*framesTls)
        if any(f is None for f in frames):
            print("Found Frame is None")   
        else:
            queue.put(framesTls) ## producer
            list(map(Show,framesTls)) ## each process return a image and display her
            
        sleep(0.5)

    queue.put(None)
    print("stop Detector")
    k.join()
    print(" Detector stopped")

    print("stop output Thread")
    queue_output.put(None)
    outputprocess.join()
    print("stoped output Thread")
    ## shutting off
    for d in dics:
        d["fulltime"] = False

    print("Waiting For Close Cameras")
    for p in process:
        p.join()

    print("stopped All")
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    

    

    


