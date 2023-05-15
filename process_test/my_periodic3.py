from pyevsim import SystemSimulator, BehaviorModelExecutor, SysMessage
from pyevsim.definition import *
import datetime

class STARTER(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 3)

        self.insert_input_port("start")
        self.insert_output_port("process")
        self.insert_input_port("result")

    def ext_trans(self,port, msg):
        if port == "start":
            print("First Started")
            self._cur_state = "Generate"
        if port == "result" :
            print("Fisrt : ",msg._msg_list[0])
            self._cur_state = "Generate"

    def output(self):
        msg = SysMessage(self.get_name(), "process")
        msg.insert(f"[Gen][OUT]: {datetime.datetime.now()}")
        return msg
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"

class CHECKER (BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Return", 0)
        self.insert_input_port("recv")
        self.insert_output_port("result")

    def ext_trans(self,port, msg):
        if port == "recv":
            # SysMessage의 구성
            # Source : 메시지를 보낸 모델
            # DST : 메시지를 보낸 출력 포트
            print("Second : ",msg._msg_list[0])
            self._cur_state = "Return"

        
    def output(self):
        msg = SysMessage(self.get_name(), "result")
        msg.insert(f"second to first")
        return msg
        
    def int_trans(self):
        if self._cur_state == "Return":
            self._cur_state = "Wait"

# System Simulator Initialization
ss = SystemSimulator()
ss.register_engine("first", "REAL_TIME", 1)
ss.get_engine("first").insert_input_port("start")
starter = STARTER(0, Infinite, "Starter", "first")
ss.get_engine("first").register_entity(starter)
checker = CHECKER(0, Infinite, "Checker", "first")
ss.get_engine("first").register_entity(checker)
ss.get_engine("first").coupling_relation(None, "start", starter, "start")
ss.get_engine("first").coupling_relation(starter, "process", checker, "recv")
ss.get_engine("first").coupling_relation(checker, "result", starter, "result")
ss.get_engine("first").insert_external_event("start", None)
ss.get_engine("first").simulate()
