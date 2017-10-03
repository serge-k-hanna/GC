import multiprocessing
import time
from multiprocessing import Process, Value, Lock, Manager, Array
from ctypes import c_int, c_char_p
class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue, poison_queue, control, result):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.poison_queue = poison_queue
        self.control = control
        self.result = result

    def run(self):
        while True:
            #print(self.control.val.value)
            if self.control.val.value == 1:
                #print(self.name, 'working', self.task_queue.qsize(), self.result_queue.qsize() )
                if not self.task_queue.empty():
                    next_task = self.task_queue.get()
                    candidate = next_task()
                    if candidate != None:
                        with self.result.lock:
                            if len(self.result.val.value)==0:
                                self.result.val.value = candidate
                            elif candidate!=self.result:
                                with self.control.lock:
                                    self.control.val.value = 0
                                self.result.val.value = None
                            elif candidate==self.result.val.value: pass
                            else: print('what?')
                    else: pass #candidate is not None -> next case                   
                    self.task_queue.task_done()
            elif self.control.val.value ==0:
                #print(self.name, 'Cleaning')
                if not self.task_queue.empty():
                    next_task=self.task_queue.get()
                    self.task_queue.task_done()
            elif self.control.val.value ==-1: #exiting
                break
            else:pass
                #print(self.name, 'passing')
class Consumer2(multiprocessing.Process):
    def __init__(self, sDelData, sParity, sResult, sPermission, sAvai, data, i, numPro):
        multiprocessing.Process.__init__(self)
        self.sDelData = sDelData
        self.sParity = sParity
        self.sResult = sResult
        self.sPermission = sPermission
        self.sAvai = sAvai
        self.data = data
        self.chunkSize=round(self.data.numCase()/numPro)
        self.sidx = i*self.chunkSize
        if i + 1 ==numPro: self.chunkSize=None #None mean till the end
    def run(self):
        while True:
            #print(self.sAvai)
            if self.sPermission < 0:
                self.sPermission+=1
                #print(self.name, 'Permission invoked')
                break
            elif self.sPermission==0:
                #print(self.name, 'Idel')
                pass
            else:
                self.sAvai-=1
                self.sPermission-=1
                #t1=time.time()
                self.data.s=str(self.sDelData)
                #print(self.name, time.time()-t1)
                self.data.p=self.sParity
                #print(self.data.s)
                #print(self.data.p)
                dels=self.data.rcaseGen(self.sidx, self.chunkSize)
                counter=0
                for d in dels:
                    #a=d
                    #print(self.name, 'working on',d)
                    r = self.data.decode(d)
                    counter+=1
                    if r != None:#compare witht the share result
                        
                        if self.sResult == None:
                            self.sResult.set(r)
                            #print(self.name, 'result', r)
                        elif self.sResult == r:
                            pass
                        else: #poision all processes
                            pass
                self.sAvai+=1
                #print(self.name, 'count', counter)
                #print(self.sResult)
                break

    def __str__(self):
        
        return ' | '.join([self.sDelData, self.sParity, self.sResult, self.sPermission, self.sAvai])

class Consumer3(multiprocessing.Process):
    def __init__(self, id, fq, mq, data, numPro):
        multiprocessing.Process.__init__(self)
        self.mq = mq
        self.fq = fq
        self.data = data
        self.chunkSize=round(self.data.numCase()/numPro)
        self.sidx = id*self.chunkSize
        if id + 1 ==numPro: self.chunkSize=None #None mean till the end
        print(self.name,'size', self.sidx, self.chunkSize)
    def run(self):
        while True:
            if not self.fq.empty():
                job = self.fq.get()
                if job ==None:
                    self.mq.put(None)
                    #print(self.name, 'I am done')
                    break
                else:
                    #print(self.name, 'size', self.fq.qsize())
                    self.data.s, self.data.p = job.data()
                    dels=self.data.rcaseGen(self.sidx, self.chunkSize)
                    counter=0
                    rdata=None
                    valid=True
                    for d in dels:
                        #print(self.name, 'Case:', d)
                        r = self.data.decode(d)
                        counter+=1
                        if r != None:#compare witht the share result
                            if rdata == None:
                                rdata = r
                            elif rdata == r:
                                pass
                            else: #poision all processes
                                #print(self.name,"Declare failure!")
                                valid=False
                                #break
                    self.mq.put(Result(job.id, rdata, valid))
                    #print(self.name, 'count', counter)
    def __str__(self):
        return str(self.name)
class Merger(multiprocessing.Process):
    def __init__(self, mq, rq):
        multiprocessing.Process.__init__(self)
        self.mq = mq
        self.rq = rq
        self.numPro = len(mq)
        self.d={}
        self.t1=time.time()
    def run(self):
        terminated=0
        while True:
            for i in range(self.numPro):
                if not self.mq[i].empty():
                    job = self.mq[i].get()
                    if job ==None:
                        terminated+=1
                        #print(self.name, terminated, 'decoding processes terminated')
                    else:
                        lst = self.d.setdefault(job.id,[])
                        lst.append((job.s, job.valid))
                        if len(lst) == self.numPro:
                            self.put(job.id, lst)
            if terminated == self.numPro:
                #print("Merger was terminated.")
                print('Simulation time: ', time.time()-self.t1)
                break
                        #result = d.setdefault(job.id,(job.s, 0, False))
                        #if result[2] == False:
                        #    if job.s == None: pass
                        #    elif result[0] == None:
                        #        result[0]=job.s
                        #    elif job.s == result[0]: pass
                        #    else: #differnt result
                        #        result[0]=None
                        #        result[2] = True
                        #result[1]+=1
                        #if result[1] == self.numPro:
                        #    self.rq.put(Result(result[0])
    def put(self,id , lst):
        r=None
        v=True
        for e, valid in lst:
            if not valid:
                v=False
                break
            if e != None:
                if r == None:
                    r = e
                elif e!=r:
                    r=None
                    break
                else: pass
        self.rq.put(Result(id, r, v))
        del self.d[id]


    def __str__(self):
        return str(self.name)
class Job(object):
    def __init__(self, id, s, p):
        self.id = id
        self.s = s
        self.p = p
    def data(self):
        return self.s, self.p
    def __str__(self):
        return str(id)+": "+self.s +"Parities: "+ str(self.p)
class Result(object):
    def __init__(self, id, s, valid):
        self.id = id
        self.s = s
        self.valid = valid
    def __str__(self):
        return str(id)+": "+self.s
class Task(object):
    def __init__(self, data, d, de):
        self.data = data
        self.d = d
        self.de = de
    def __str__(self):
        return 'Doing job ' + str(self.d)
    def __call__(self):
        return self.data.decode(self.d,self.de)   
class LockedString(object):
    def __init__(self, initval=''):
        manager = Manager()
        self.val = manager.Value(c_char_p, initval)
        self.lock = Lock()
    def set(self, val):
        with self.lock:
            self.val.value = val
    def __getitem__(self, key):
        return self.val.value.__getitem__(key)
    def __len__(self):
        return len(self.val.value)
    def __eq__(self, b):
        return self.val.value == b
    def __str__(self):
        return self.val.value
class LockedInt(object):
    def __init__(self, initval=0):
        self.val = Value(c_int, initval)
        self.lock = Lock()

    def set(self, val):
        with self.lock:
            self.val.value = val

    def __getitem__(self):
        return self.val.value
    
    def __len__(self):
        return len(self.val.value)

    def __iadd__(self, val):
        with self.lock:
           self.val.value+=val
           return self
    def __isub__(self, val):
        with self.lock:
           self.val.value-=val
           return self

    def __lt__(self, b):
        return self.val.value < b
    def __le__(self, b):
        return self.val.value <= b
    def __eq__(self, b):
        return self.val.value == b
    #def __ne__(self, b):
    #    return self.val.value != b
    def __gt__(self, b):
        return self.val.value > b
    def __ge__(self, b):
        return self.val.value >= b

    def __add__(self, b):
        self.set(self.val.value+b)
    def __sub__(self, b):
        self.set(self.val.value-b)

    def __str__(self):
        return str(self.val.value)
class LockedList(object):
    def __init__(self, initval=[0]):
        self.lst = Array('i', initval)
        self.lock = Lock()

    def __setitem__(self, idx, val):
        with self.lock:
            self.lst[idx] = val

    def set(self, a):
        with self.lock:
            for i in range(len(self.lst)):
                self.lst[i]=a[i]
    def __getitem__(self,idx):
        return self.lst[idx]
    
    def __len__(self):
        return len(self.lst)
    def __str__(self):
        o='['+', '.join([str(i) for i in self.lst])+']'
        return o
