import cv2
import numpy as np 
import unittest
import sys
sys.path.append("B:\SmartCross\Models\yolodata")

from Detector import DetectorOBJ
from multiprocessing import Manager 
import os
from time import sleep
import datetime
class DetectorTest(unittest.TestCase):

    def test_image(self):
        print("ImageTest")
        print(os.getcwd())
        image =cv2.imread("datatest\cars1.jpg")
        title = "Car Image"
        sample = (image,title,str(datetime.datetime.now()))
        self.q.put([sample])

        actual_result = self.output.get()
       
        assert(actual_result[title] == {'car': 43, 'person': 1, 'truck': 5})
        

       
    def setUp(self):
        
        manager = Manager()
        self.q = manager.Queue()
        self.output = manager.Queue()
        self.detector = DetectorOBJ(self.q,self.output)
        self.detector.start()

        sleep(10)
       
    def tearDown(self):
        self.output.put(None)
        self.q.put(None)
        self.detector.join()

if __name__ == '__main__':
    unittest.main()