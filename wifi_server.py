import socket
import json
import time
# import picar_4wd as fc

speed = 10
turn_speed = 5

curr_speed = 0
distance_traveled = 0
battery_percentage = 0

HOST = "127.0.0.1"  # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(None)
    s.bind((HOST, PORT))
    s.listen()

    new_time = time.time()
    prev_time = time.time()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            # receive 1024 Bytes of message in binary format
            data = client.recv(1024)
            print(data)

            new_time = time.time()
            distance_traveled += (new_time - prev_time) * curr_speed
            prev_time = time.time()

            # battery_percentage = fc.power_read()

            if data != b"":
                if data == b"0":
                    # stop
                    # fc.stop()
                    curr_speed = 0
                elif data == b"87":
                    # w
                    # fc.forward(speed)
                    curr_speed = speed
                    start_time = time.time()
                elif data == b"83":
                    # s
                    # fc.backward(speed)
                    curr_speed = speed
                    start_time = time.time()
                elif data == b"65":
                    # a
                    # fc.turn_left(turn_speed)
                    curr_speed = 0
                elif data == b"68":
                    # d
                    # fc.turn_right(turn_speed)
                    curr_speed = 0

            data = dict({
                "curr_speed": curr_speed,
                "distance_traveled": distance_traveled,
                "battery_percentage": battery_percentage,
            })
            print(json.dumps(data))
            # Echo back to client
            client.sendall(json.dumps(data).encode())

    except:
        print("Closing socket")
        client.close()
        s.close()
