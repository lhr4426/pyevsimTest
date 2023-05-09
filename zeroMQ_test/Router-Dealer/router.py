# encoding: utf-8
import zmq
from collections import defaultdict

context = zmq.Context()
# 소켓 생성 (소켓 패턴외에 어떤 정보도 필요하지 않음)
client = context.socket(zmq.ROUTER)

# 소켓 연결
# 172.17.136.52
client.bind("tcp://*:5556")

# Poller 생성 및 설정 
# poller : 두 개 이상의 소켓을 등록하면 소켓 이벤트 감지하여 (소켓, 이벤트) 리스트 리턴
poll = zmq.Poller()
poll.register(client, zmq.POLLIN)
counter = defaultdict(int)

while True:
    # handle input
    # 각 이벤트 (소켓, 이벤트) 형태로 전달 , dictionary 타입 변환
    sockets = dict(poll.poll(1000))
    if sockets:
        identity = client.recv()
        msg = client.recv()
        counter[identity] += 1
    
    # start recording
    for identity in counter.keys():
        client.send_string(str(identity), flags=zmq.SNDMORE)
        client.send_string("START")
        client.send_string("STOP")

    print (counter)