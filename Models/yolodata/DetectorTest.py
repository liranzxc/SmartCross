import cv2
import numpy as np 
import unittest
import sys
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

        while self.detector.readResult() == None:
            pass
        assert(self.detector.readResult()[title] == {'car': 43, 'person': 1, 'truck': 5})
        

       
    def setUp(self):
        
        manager = Manager()
        self.q = manager.Queue()
        self.d = manager.dict()
        self.detector = DetectorOBJ(self.q,self.d)
        self.detector.start()

        sleep(10)
       
    def tearDown(self):
        self.q.put(None)
        self.detector.join()

if __name__ == '__main__':
    os.chdir("..")
    print(os.getcwd())
    unittest.main()