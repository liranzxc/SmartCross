from multiprocessing import Process, Queue
from time import sleep
def f(q):
    print("start to sleep")    
    sleep(10)
    print("stop to sleep")
    q.put([42, None, 'hello'])

if __name__ == '__main__':
        q = Queue()
        p = Process(target=f, args=(q,))
        p.start()
        print(q.get())    # prints "[42, None, 'hello']"
        p.join()
