import socket
import json
import time
import picar_4wd as fc
import numpy as np

speed = 10
turn_speed = 5

curr_speed = 0
obstacle = False

distance_traveled = 0

HOST = "172.16.252.49" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

def scan_environment():
    current_angle = -90
    fc.get_distance_at(current_angle)
    time.sleep(0.2)

    dist_list = []
    while True:
        dist = fc.get_distance_at(current_angle)
        dist_list.append(dist)
        if current_angle == 90:
            break
        current_angle += 5
    
    fc.get_distance_at(0)
    time.sleep(0.2)

    dist_list = np.array(dist_list)
    # m is True is nothing infront, false if there is things in front
    m = not np.any((dist_list[12:25] <= 35) & (dist_list[12:25] > 0))
    
    return m

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            
            if data == "0":
                # stop
                fc.stop() 
                curr_speed = 0
            elif data == "87":
                # w
                fc.forward(speed)
                curr_speed = speed
            elif data == "83":
                # s
                fc.backward(speed)
                curr_speed = -speed
            elif data == "65":
                # a
                fc.turn_left(turn_speed)
                curr_speed = 0
            elif data == "68":
                # d
                fc.turn_right(turn_speed)
                curr_speed = 0
            elif data == "scan":
                # scan obstacle
                if scan_environment:
                    obstacle = False
                else:
                    obstacle = True


            data = {
                "curr_speed" : curr_speed,
                "obstacle": obstacle, 
            }
            print(json.dumps(data))
            client.sendall(json.dumps(data)) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    