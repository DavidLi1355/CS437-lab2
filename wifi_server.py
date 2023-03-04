import socket
import json
import time
import picar_4wd as fc
import numpy as np

speed = 10
turn_speed = 5

curr_speed = 0
is_obstacle = False
distance_traveled = 0

HOST = "172.16.252.49"  # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            scan_list = fc.scan_step(35)
            if not scan_list:
                continue

            tmp = scan_list[3:7]
            if tmp != [2, 2, 2, 2]:
                is_obstacle = True
            else:
                is_obstacle = False

            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            # receive 1024 Bytes of message in binary format
            data = client.recv(1024)

            if data == "0":
                # stop
                fc.stop()
                curr_speed = 0
                end_time = time.time()
                distance_traveled += (end_time - start_time) * speed
            elif data == "87":
                # w
                fc.forward(speed)
                curr_speed = speed
                start_time = time.time()
            elif data == "83":
                # s
                fc.backward(speed)
                curr_speed = speed
                start_time = time.time()
            elif data == "65":
                # a
                fc.turn_left(turn_speed)
                curr_speed = 0
            elif data == "68":
                # d
                fc.turn_right(turn_speed)
                curr_speed = 0

            data = {
                "curr_speed": curr_speed,
                "is_obstacle": is_obstacle,
                "distance_traveled": distance_traveled,
            }
            print(json.dumps(data))
            client.sendall(json.dumps(data))  # Echo back to client
    except:
        print("Closing socket")
        client.close()
        s.close()
