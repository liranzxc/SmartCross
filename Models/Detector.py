import cv2
import numpy
from multiprocessing import Process,Manager



class Detector(Process):
    def __init__(self,d):
        super(Detector, self).__init__()
        self.d = d 
        
    def run(self):
        pass