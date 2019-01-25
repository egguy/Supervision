# encoding: utf-8
import json

import zmq
from collections import defaultdict

context = zmq.Context()
client = context.socket(zmq.ROUTER)
client.bind("tcp://*:5000")

poll = zmq.Poller()
poll.register(client, zmq.POLLIN)
counter = defaultdict(int)

while True:
    # handle input
    sockets = dict(poll.poll(1000))
    if sockets:
        identity, msg = client.recv_multipart()
        msg = json.loads(msg.decode('utf-8'))
        if msg['type'] == "hello":
            counter[identity] += 1
            print(identity)
            print(msg)
            client.send(identity, zmq.SNDMORE)
            client.send_json({
                "id": 12,
                "type": "test",
                "packet_number": 5, # Number of packet sent
                "packet_timeout": 5,  # Maximum timeout between each test
                "standard_test_target":  "192.168.0.1", # ping address
                "speedtest_choice": "",
                "speedtest_target": {
                    "ip": "",
                    "port": ""
                },
                "speedtest_option": "",
                "comment": "",
                "influxdb": "",
            })
        else:
            print("TEST")
            print(msg)

    # start recording
    #for identity in counter.keys():
    #    client.send(identity, zmq.SNDMORE)
    #     client.send_string("START")
