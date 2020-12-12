import socket
import threading
import logging
import time
import json
import random

from player import Player
import server_functions as sf
import archery_tracker


class ThreadedServer():
    """Socket server that received client connections and data"""

    def __init__(self, host, port, game):
        """Init the threaded server settings"""
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = None
        self.server_comm_pause_start = 0
        self.thread_name = None
        self.game = game
        # self.send_comm = False

    def bind(self):
        """Bind IP address and Port for the server"""
        try:
            logging.info(
                'ThreadedServer.bind(): Try to create socket on {}:{}'.format(self.host, self.port))
            self.sock.bind((self.host, self.port))

        except socket.error as e:
            logging.error('ThreadedServer.bind(): {}'.format(str(e)))

        else:
            logging.info(
                'ThreadedServer.bind(): Socket created on {}.{}'.format(self.host, self.port))
            logging.info("==========" * 7)

            self.listen()

    def listen(self):
        """
        Listen for new connections to the server
        and start a new thread for each new connection
        """
        logging.info(
            "ThreadedServer.listen(): listening for new client connection...")
        self.sock.listen(5)

        while True:
            client, address = self.sock.accept()
            self.client = client
            new_player = Player()
            # client.settimeout(10)

            # if connected, make threads
            if self.verify_client_conn(client):
                logging.info(
                    "================================================================\nThreadedServer.listen(): Connected to: {}:{}\n==========================================================================\n".format(address[0], str(address[1])))
                t1 = threading.Thread(target=self.speak_to_client, name="send_" + self.thread_name, args=(
                    client, address, new_player))
                t2 = threading.Thread(target=self.listen_to_client, name="recv_" + self.thread_name, args=(
                    client, address, new_player))

                t1.start()
                t2.start()

            logging.info(
                f"ThreadedServer.listen() Show active threads \n{threading.enumerate()}\n")

    def verify_client_conn(self, client):
        """Make sure handshake happens before makeing threads"""

        logging.info(
            "ThreadedServer.verify_client_conn(): Verifying connection...")

        connected = False

        while not connected:

            data = self.get_msg(client)
            response = '''{"connected": "True"}'''

            if data == "":
                continue
            else:
                # connection confirmation
                if data == "Handshake_1":
                    self.thread_name = 'kiosk_1'
                    connected = True
                elif data == "Handshake_2":
                    self.thread_name = 'kiosk_2'
                    connected = True
                elif data == "Handshake_3":
                    self.thread_name = 'kiosk_3'
                    connected = True
                elif data == "Handshake_wall":
                    self.thread_name = 'wall'
                    connected = True
                else:
                    response = '''{"connected": "False"}'''
                    self.send_msg(client, response)
                    client.close()
                    logging.error(
                        f"ThreadedServer.verify_client_conn(): Connection rejected. Data received: {data}\n")
                    break

                self.send_msg(client, response)
                return connected

    def speak_to_client(self, client, address, player):
        """Send messages to clients"""

        t_name = threading.currentThread().getName()

        while True:

            if t_name == "send_pool":
                try:
                    # loop over the flag list, if True
                    # send the data to the pool for that kiosk
                    for r in range(3):
                        if self.game.send_toss_to_pool[r]:
                            data = self.game.players[r]
                            data = json.dumps(data)
                            if self.send_msg(client, data):
                                logging.info(
                                    f'{t_name}: ThreadedServer.speak_to_client: {data}\n')
                                # reset flag
                                self.game.send_toss_to_pool[r] = False
                                time.sleep(.2)
                            else:
                                time.sleep(.2)
                                break
                except Exception as e:
                    logging.error(
                        f"{t_name}: ThreadedServer.speak_to_client(): {e}\n")
                    logging.error(
                        f"{t_name}: ThreadedServer.speak_to_client(): closing thread\n")
                    return False

            # Send pool responses to the kiosks
            # if the flags are set to True
            elif t_name == "send_kiosk_1" and self.game.update_kiosk[0] is True:
                try:
                    data = json.dumps(self.game.kiosk_data[0])
                    if self.send_msg(client, data):
                        self.game.update_kiosk[0] = False
                        time.sleep(.15)
                    else:
                        break
                except Exception as e:
                    logging.error(
                        f"{t_name}: ThreadedServer.speak_to_client(): {e}\n")

            elif t_name == "send_kiosk_2" and self.game.update_kiosk[1] is True:
                try:
                    data = json.dumps(self.game.kiosk_data[1])
                    if self.send_msg(client, data):
                        self.game.update_kiosk[1] = False
                        time.sleep(.15)
                    else:
                        break
                except Exception as e:
                    logging.error(
                        f"{t_name}: ThreadedServer.speak_to_client(): {e}\n")

            elif t_name == "send_kiosk_3" and self.game.update_kiosk[2] is True:
                try:
                    data = json.dumps(self.game.kiosk_data[2])
                    if self.send_msg(client, data):
                        self.game.update_kiosk[2] = False
                        time.sleep(.15)
                    else:
                        break
                except Exception as e:
                    logging.error(
                        f"{t_name}: ThreadedServer.speak_to_client(): {e}\n")

    def listen_to_client(self, client, address, player):
        """Listen for data being sent from the client"""

        t_name = threading.currentThread().getName()

        # Client/server Communication loop
        while True:

            data = self.get_msg(client)

            if data is not False:
                if data == "" or data == "Partial" or data == "toss_received":
                    continue
                else:
                    # Top 5 players to wall
                    if data == "Leaderboard":
                        self.send_msg(client, self.game.send_leaderboard())
                    else:
                        logging.info(
                            f"{t_name}: ThreadedServer.listen_to_client(): {data}\n")

                        if data.find("kiosk") != -1:
                            # INFO:root:recv_pool: ThreadedServer.listen_to_client(): {"kiosk_id":1,"ball_id":3,"score":100}
                            self.game.pool_response(data)

                        else:
                            if player.update(data) and self.game.update_player_data(player):
                                response = '''{"toss_received": "True"}'''
                            else:
                                response = '''{"toss_received": "No Toss"}'''

                            result = self.send_msg(client, response)

                            if player.game_over is True:
                                self.game.update_leaderboard(player)
                                player.player_reset()
                                time.sleep(1)
            else:
                logging.error(
                    f"{t_name}: ThreadedServer.listen_to_client(): closing loop.\n")
                return False

    def get_msg(self, client):
        """Get responses from clients"""

        try:
            data = client.recv(2048).decode()
        except Exception as e:
            logging.error(
                f'ThreadedServer.get_msg(): closing connection... {str(e)}')
            client.close()
            return False
        else:
            # always clean incomming data
            # logging.info(f'ThreadedServer.get_msg(): Raw data: {data}')
            data = sf.clean_json_data(data)
            # logging.info(f'ThreadedServer.get_msg(): Cleaned data: {data}')
            return data

    def send_msg(self, client, data):
        """Send a message to a client"""

        try:
            client.send(str.encode(data))
        except socket.error as e:
            logging.error(
                f"ThreadedServer.send_msg(): closing connection... {str(e)}")
            client.close()
            return False
        else:
            return True
