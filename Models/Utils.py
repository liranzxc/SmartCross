import cv2
import numpy

def Show(p):
        try:
            cv2.imshow("frame"+str(p),p.read())
            cv2.waitKey(1)
        except:
            print("error in show method in process " + str(p.d["name"]))
            pass
            

def createdic(manager,src):
        d = manager.dict()
        d["src"] = src
        d["name"] = src
        d["fulltime"] = True
        return d

def trygrabframe(p):
    try:
        frame = p.read()
        if frame is not None:
            return frame
        else:
            return None
    except:
        return None

def grabFrames(process):
    frames = []

    for p in process:
        _frame = trygrabframe(p)
        if _frame is None:
            while(_frame is None):
                _frame = trygrabframe(p)
                print("trying to get frame from process : "+str(p))
        else:
            frames.append(_frame)

    print("Successfully grab "+str(len(process)))
    return frames
    