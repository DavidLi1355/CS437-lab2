import socket
import json

# picar
import picar_4wd as fc

speed = 10
turn_speed = 5
curr_speed = 0

distance_traveled = 0

HOST = "172.16.252.49" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

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


            data = {
                "curr_speed" : curr_speed,
            }
            print(json.dumps(data))
            client.sendall(json.dumps(data)) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    