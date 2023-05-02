from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from random import randint
import datetime

class PEx(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 1)

        self.insert_input_port("start")

        self.start_num = 0
        self.end_num = 0


    def ext_trans(self,port, msg):
        if port == "start":
            print(f"랜덤 정수 생성기 시작\n시작 숫자와 끝 숫자를 공백을 두어 입력하세요.")
            input_items = input().split(' ')
            self.start_num = int(input_items[0])
            self.end_num = int(input_items[1])
            self._cur_state = "Generate"
        

    def output(self):
        print(f"{randint(self.start_num, self.end_num)}")
        return None
        
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"


ss = SystemSimulator()

ss.register_engine("first", "REAL_TIME", 1)
ss.get_engine("first").insert_input_port("start")
gen = PEx(0, Infinite, "Gen", "first")
ss.get_engine("first").register_entity(gen)

ss.get_engine("first").coupling_relation(None, "start", gen, "start")

ss.get_engine("first").insert_external_event("start", None)
ss.get_engine("first").simulate()

