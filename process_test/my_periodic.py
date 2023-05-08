from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
import datetime
import os

class PEx(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate", 5)

        self.insert_input_port("start")

        self.my_dir = os.path.dirname(os.path.abspath(__file__))

    def ext_trans(self,port, msg):
        if port == "start":
            print(f"input time : {datetime.datetime.now()}")
            print("program started")
            print(f"file directory : {self.my_dir}")
            self._cur_state = "Generate"

    def output(self):
        print(f"output time : {datetime.datetime.now()}")
        os.system(f"dotnet run --project {self.my_dir}")
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

