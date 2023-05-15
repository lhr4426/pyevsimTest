# encoding: utf-8

import random
import zmq
import time

context = zmq.Context()
worker = context.socket(zmq.DEALER)
worker.setsockopt_string(zmq.IDENTITY, str(random.randint(0, 8000)))
worker.connect("tcp://172.17.135.29:5555")

start = True
# worker.send_multi_part()
worker.send_string("Hello")
while True:
    if start:
        worker.send_string("recording data: %s" % random.randint(0,100))
        time.sleep(0.5)
    request = worker.recv()
    if request == "START":
        start = True
    if request == "STOP":
        start = False
    if request == "END":
        print ("A is finishing")
        break