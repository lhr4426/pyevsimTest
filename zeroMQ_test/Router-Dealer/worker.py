# encoding: utf-8

import random
import zmq
import time
import socket

socket_open = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_open.connect(('www.google.co.kr', 443))
inner_ip = socket_open.getsockname()[0]
context = zmq.Context()
worker = context.socket(zmq.DEALER)
worker.setsockopt_string(zmq.IDENTITY, str(random.randint(0, 8000)))
worker.connect("tcp://localhost:5556")
start = False
worker.send_string("Hello")
while True:
    if start:
        worker.send_string("hello")
        time.sleep(0.5)
    request = worker.recv()
    if request == "START":
        start = True
    if request == "STOP":
        start = False
    if request == "END":
        print ("A is finishing")
        break