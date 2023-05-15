import multiprocessing as mp
import time

def test(value) :
    print("sub start")
    time.sleep(5)
    print("sub stop")

if __name__ == "__main__" :
    print("main start")
    p = mp.Process(name = "Sub" , target = test, args=("test",))
    p.start()
    p.join()
    print(p.pid)
    print("main stop")