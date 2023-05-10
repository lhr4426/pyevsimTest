import time
import zmq

# 컨텍스트 : 소켓과 소켓의 입출력을 관리하는 객체 
context = zmq.Context()
socket = context.socket(zmq.REP)
# 안정적인 서버가 보통 bind, 클라이언트는 connect 한다.
socket.bind("tcp://*:5555")

while True :
    message = socket.recv()
    print(f"Received request : {message}")

    time.sleep(5)

    if message == "OK" :
        socket.send_string("RUN")
    elif message == "NOT_OK" :
        socket.send_string("CALLBACK")