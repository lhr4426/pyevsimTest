from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite, SysMessage
import datetime
import os, signal
import psutil
import multiprocessing as mp
import subprocess as sp
import zmq
import random
import pickle

class PEx(BehaviorModelExecutor):
    START = 0
    CHANGED = 1
    TERMINATED = -1

    def __init__(self, instance_time, destruct_time, name, engine_name, worker):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 1)
        self.insert_state("Checking", 5)
        self.insert_state("Stop", Infinite)

        self.insert_input_port("start")
        self.insert_input_port("result")
        self.insert_output_port("pid")

        self.model_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_pid = os.getpid()
        self.process_pid = 0
        self.process_obj = None
        self.process_state = None
        self.result = None
        self.worker = worker

    def ext_trans(self,port, msg):
        if port == "start":
            print(f"input time : {datetime.datetime.now()}")
            print("program started")
            print(f"file directory : {self.model_dir}")
            self._cur_state = "Generate"
        if port == "result" :
            self.result = msg._msg_list[0]
            print("result : ", self.result)
            self.worker.send({self.TERMINATED, self.result})
            
            self._cur_state = "Checking"

    def output(self):
        if self.get_cur_state() == "Generate" :
            print(f"Generate Time : {datetime.datetime.now()}")
            # p = mp.Process(name="Csharp", target=csharp, args=(self.model_dir,))
            # p.start()
            self.process_obj = sp.Popen(['dotnet', 'run', '--project', self.model_dir], stdout=sp.PIPE, text=True)
            self.process_pid = self.process_obj.pid
            msg = SysMessage(self.get_name(), "pid")
            msg.insert(self.process_obj)
            self.worker.send({self.START, self.process_pid})
            return msg
            
        elif self.get_cur_state() == "Checking" :
            if psutil.pid_exists(self.process_pid) :
                stat = psutil.Process(self.process_pid).status()
                if self.process_state != stat :
                    self.process_state = stat
                    self.worker.send({self.CHANGED, self.process_state})
                    print(stat)
            else :
                print("Not exist PID ", self.process_pid)
                os.kill(self.model_pid, signal.SIGTERM)
        return None
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Checking"
        elif self.get_cur_state() == "Checking" :
                self._cur_state == "Checking"

class returnFinder(BehaviorModelExecutor) :
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Get")
        self.insert_state("Get", Infinite)
        self.insert_state("CheckReturn", 1)
        self.insert_state("Terminated", Infinite)
        
        self.insert_input_port("pid")
        self.insert_output_port("result")

        self.process_pid = 0
        self.process_obj = None
        self.stat = None
    
    def ext_trans(self,port, msg):
        if port == "pid":
            # SysMessage의 구성
            # Source : 메시지를 보낸 모델
            # DST : 메시지를 보낸 출력 포트
            self.process_obj = msg._msg_list[0]
            self.process_pid = self.process_obj.pid
            print("Second Get PID : ",self.process_pid)
            self._cur_state = "CheckReturn"
        
    def output(self):
        # print(">> Second Model : ", self.get_cur_state())
        if self.get_cur_state() == "CheckReturn" :
            msg = SysMessage(self.get_name(), "result")
            result = self.process_obj.poll()  
            if result != None :
                print(self.process_pid, "is terminated")
                msg.insert(result)
                self._cur_state = "Terminated"
                return msg
    
    def int_trans(self):
        if self._cur_state == "CheckReturn":
            self._cur_state = "CheckReturn"


if __name__ == "__main__" : 
    
    mp.freeze_support()
    ss = SystemSimulator()

    context = zmq.Context()
    worker = context.socket(zmq.DEALER)
    worker.setsockopt_string(zmq.IDENTITY, str(random.randint(0, 8000)))
    worker.connect("tcp://172.17.135.29:5555")
    

    ss.register_engine("first", "VIRTURE_TIME", 1)
    ss.get_engine("first").insert_input_port("start")
    gen = PEx(0, Infinite, "Gen", "first", worker=worker)
    ss.get_engine("first").register_entity(gen)
    returnfinder = returnFinder(0, Infinite, "returnFinder", "first")
    ss.get_engine("first").register_entity(returnfinder)

    ss.get_engine("first").coupling_relation(None, "start", gen, "start")
    ss.get_engine("first").coupling_relation(gen, "pid", returnfinder, "pid")
    ss.get_engine("first").coupling_relation(returnfinder, "result", gen, "result")
    
    worker.send_string("CONNECTED")
    request = worker.recv()
    print(request)

    if request == b"START" :
        ss.get_engine("first").insert_external_event("start", None)
        ss.get_engine("first").simulate()
