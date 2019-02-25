from __future__ import division
from multiprocessing import Process,Manager
import time
import torch 
import torch.nn as nn
import datetime

from torch.autograd import Variable
import numpy as np
import cv2 
import argparse
import os 
import os.path as osp
from yolodata.util import *
from yolodata.darknet import Darknet

#from util import *
#from darknet import Darknet
from yolodata.preprocess_liran import prep_image, inp_to_image

#from preprocess_liran import prep_image,inp_to_image
import pandas as pd
import random 
import pickle as pkl
import itertools
import random
from collections import Counter


class test_net(nn.Module):
    def __init__(self, num_layers, input_size):
        super(test_net, self).__init__()
        self.num_layers= num_layers
        self.linear_1 = nn.Linear(input_size, 5)
        self.middle = nn.ModuleList([nn.Linear(5,5) for x in range(num_layers)])
        self.output = nn.Linear(5,2)
    
    def forward(self, x):
        x = x.view(-1)
        fwd = nn.Sequential(self.linear_1, *self.middle, self.output)
        return fwd(x)
        
def get_test_input(input_dim, CUDA):
    img = cv2.imread("dog-cycle-car.png")
    img = cv2.resize(img, (input_dim, input_dim)) 
    img_ =  img[:,:,::-1].transpose((2,0,1))
    img_ = img_[np.newaxis,:,:,:]/255.0
    img_ = torch.from_numpy(img_).float()
    img_ = Variable(img_)
    
    if CUDA:
        img_ = img_.cuda()
    #num_classes
    return img_



class DetectorOBJ(Process):
    def __init__(self,queue,queue_output):
        super(DetectorOBJ, self).__init__()
        self.queue = queue
        self.output = queue_output
        
    def run(self):
        ## change path 
        modelpath = os.getcwd()
        yolodatapath= os.getcwd()+"\yolodata"
        os.chdir(yolodatapath)
        ### 

        mydicResult = {} 
        batch_size = 1
        confidence = 0.5
        nms_thesh = 0.4
        start = 0

        CUDA = torch.cuda.is_available()

        num_classes = 80
        
        classes = load_classes('data/coco.names') 

        #Set up the neural network
        print("Loading network.....")
        model = Darknet("cfg/yolov3.cfg")
        model.load_weights("yolov3.weights")
        print("Network successfully loaded")


        
    
        model.net_info["height"] = 416
        inp_dim = int(model.net_info["height"])
        assert inp_dim % 32 == 0 
        assert inp_dim > 32

        #If there's a GPU availible, put the model on GPU
        if CUDA:
            model.cuda()
    
    
        #Set the model in evaluation mode
        model.eval()

        while True:
            framesTls = self.queue.get()
            if framesTls is None:
                break
            ## start here
            images,names,times = zip(*framesTls)

            batches = list(map(prep_image, images, [inp_dim for x in range(len(images))]))
            im_batches = [x[0] for x in batches]
            orig_ims = [x[1] for x in batches]
            im_dim_list = [x[2] for x in batches]
            im_dim_list = torch.FloatTensor(im_dim_list).repeat(1,2)

            if CUDA:
                im_dim_list = im_dim_list.cuda()
    
            leftover = 0
    
            if (len(im_dim_list) % batch_size):
                leftover = 1    
        
            if batch_size != 1:
                num_batches = len(images) // batch_size + leftover            
                im_batches = [torch.cat((im_batches[i*batch_size : min((i +  1)*batch_size,
                            len(im_batches))]))  for i in range(num_batches)]        


            i = 0

            write = False
            #model(get_test_input(inp_dim, CUDA), CUDA)
    
            start_det_loop = time.time()
    
            objs = {}
      
            for batch in im_batches:
                #load the image 
                start = time.time()
                if CUDA:
                    batch = batch.cuda()
                

            #Apply offsets to the result predictions
            #Tranform the predictions as described in the YOLO paper
            #flatten the prediction vector 
            # B x (bbox cord x no. of anchors) x grid_w x grid_h --> B x bbox x (all the boxes) 
            # Put every proposed box as a row.
                with torch.no_grad():
                    prediction = model(Variable(batch), CUDA)
            
                
        
               #prediction = prediction[:,scale_indices]

        
            #get the boxes with object confidence > threshold
            #Convert the cordinates to absolute coordinates
            #perform NMS on these boxes, and save the results 
            #I could have done NMS and saving seperately to have a better abstraction
                #But both these operations require looping, hence 
            #clubbing these ops in one loop instead of two. 
            #loops are slower than vectorised operations. 
        
                prediction = write_results(prediction, confidence, num_classes, nms = True, nms_conf = nms_thesh)       
                if type(prediction) == int:
                    i += 1
                    continue

                end = time.time()
                prediction[:,0] += i*batch_size           
          
                if not write:
                    output = prediction
                    write = 1
                else:
                    output = torch.cat((output,prediction))
            
        
        
                for im_num, image in enumerate(images[i*batch_size: min((i +  1)*batch_size, len(images))]):
                    im_id = i*batch_size + im_num
                    objs = [classes[int(x[-1])] for x in output if int(x[0]) == im_id]
            
                        #print("{0:20s} predicted in {1:6.3f} seconds".format(image.split("/")[-1], (end - start)/batch_size))
                    #print("{0:20s} {1:s}".format("Objects Detected:", " ".join(objs)))
                    mydicResult[names[i]] = (dict(Counter(objs)))
                    #print("----------------------------------------------------------")
                i += 1

            
                if CUDA:
                    torch.cuda.synchronize()    
        
        
                torch.cuda.empty_cache()

                ## change path back to parent
            os.chdir(modelpath)
            mydicResult["time"] = str(datetime.datetime.now())
            #print(mydicResult)

            self.output.put(mydicResult)
        



            


if __name__ ==  '__main__':
    manger = Manager()
    d = manger.dict()
    image =  cv2.imread("imgs/giraffe.jpg")
    img2 =cv2.imread("imgs/img2.jpg")
    img3 =cv2.imread("imgs/messi.jpg")

    d['images'] = [image,img2,img3]
    p = DetectorOBJ(d)
    p.start()


    p.join()

    print(d['results'])