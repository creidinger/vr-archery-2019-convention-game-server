# Main socket client that sends player data to Server
# Author: Chase Reidinger

import socket
import threading
import time
import logging
import json
import random

logging.basicConfig(filename="log/client.log", level=logging.DEBUG)


def connect_to_server(server, port):
    """Keep trying to connect to socket server.py"""

    connected = False

    while not connected:
        try:
            logging.info(
                f"connect_to_server(): Connecting to {server}:{str(port)}")
            logging.info("==========" * 7)
            s.connect((server, port))

            if verify_server_conn(s):
                connected = True
            else:
                s.close()
        except socket.error as e:
            logging.error(f"connect_to_server(): {str(e)}")
            time.sleep(2)


def verify_server_conn(socket):
    """Try sending handshake to server"""

    s = socket

    # data = '''invalid<EOF>'''
    data = '''Handshake_1<EOF>'''
    # data = '''Handshake_pool<EOF>'''

    try:
        s.send(str.encode(data))
        response = s.recv(2048).decode()
    except socket.error as e:
        logging.error(f"verify_server_conn(): \n{str(e)}")
        time.sleep(2)
    else:
        logging.info(
            f"verify_server_conn(): Server Response: {response}")
        if response == '''{"connected": "True"}''':
            return True
        else:
            return False


def send_data():
    """Send data to server"""

    logging.info("send_data(): Thread open")
    while True:
        # try:
        #     data = '''{"id":1,"name":"xvb cvb","phone":"Canvas","score":0,"state":"inactive","ball_id":"0_1","start_x":486.2099,"angle":45.5,"velocity":17.89495,"game_over":false}<EOF>'''
        #     r = random.randint(1,5)
        #     if r > 3:
        #         data = '''{"id":1,"name":"xvb cvb","phone":"Canvas","score":0,"state":"inactive","ball_id":"0_1","start_x":486.2099,"angle":45.5,"velocity":17.89495,"game_over":true}<EOF>'''
        #     s.send(str.encode(data))

        try:
            r = random.randint(1,5)
            if r > 3:
                # gameover
                data = '''{"id":1,"name":"NO_NAME","phone":"NO_NUMBER","score":0,"state":"inactive","ball_id":"","start_x":0,"angle":-1,"velocity":-1,"game_over":true}<EOF>'''
                s.send(str.encode(data))
                # reset
                data = '''{"id":1,"name":"oo ooo","phone":"000","score":0,"state":"inactive","ball_id":"","start_x":0,"angle":-1,"velocity":-1,"game_over":false}<EOF>'''
                s.send(str.encode(data))
            else:
                #normal send
                data = '''{"id":1,"name":"oo ooo","phone":"000","score":0,"state":"inactive","ball_id":"1_3","start_x":-371.8648,"angle":69.44395,"velocity":1.501734,"game_over":false}<EOF>'''
                s.send(str.encode(data))
        except socket.error as e:
            logging.error(
                f"send_data(): Unable to send data to server {str(e)}")
            s.close()
            return False
        else:
            logging.info("send_data(): data sent to server...")

        time.sleep(random.randint(1, 5))


def recv_data():
    """Receive data from server"""

    logging.info("recv_data(): Thread open")
    while True:
        try:
            # Receive data from server
            data = s.recv(2048).decode()
        except socket.error as e:
            logging.error(

                f"recv_data(): Unable to recevie server data... {str(e)}")
            s.close()
            return False
        else:
            if data == "":
                # logging.info('recv_data(): no data')
                continue
            else:
                logging.info(
                    f"recv_data(): Server Data Received: {data}")
                continue


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # hostname = socket.gethostname()
    # IPAddr = socket.gethostbyname(hostname)
    # connect_to_server(IPAddr, 5000)
    connect_to_server('10.0.0.60', 5000)

    threading.Thread(target=send_data).start()
    threading.Thread(target=recv_data).start()

    while True:
        # soccet connected
        time.sleep(1)
