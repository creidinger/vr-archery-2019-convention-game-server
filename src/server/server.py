import socket
import sys
from _thread import *

import archery_tracker

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server = '127.0.0.1'
# server = '10.199.162.20'
server = '192.168.2.10'

port = 8000


global clients

clients = []
logging.info('\n==========================================\nArchery Game socket server\n==========================================\n')

try:
    s.bind((server, port))
except socket.error as e:
    logging.info(str(e))

s.listen(1)
logging.info('Waiting for a connection...')


def threaded_client(conn):

    global player_one_fire
    global player_two_fire
    global player_three_fire

    player_one_fire = '3'
    player_two_fire = '3'
    player_three_fire = '3'

    conn.sendall(str.encode("Connected..."))

    while True:
        data = conn.recv(2048)
        mess = data.decode('utf-8')
        reply = ''
        logging.info(mess)
        # if nothing is being sent, wait
        if not data:
            break

        #     #
        if mess.find('<EOF>') == -1:
            logging.info("EOF BREAK")
            break
        else:

            # remove <EOF> from string
            new_mess = mess.replace('<EOF>', "")

            # if PlayerRegister is found, send to wall
            if new_mess.find('PlayerRegister') == -1:

                if new_mess == 'WallHandshake':
                    # SEND HANDSHAKE
                    wall_conn = conn
                    logging.info('WALL HAS CONNETED')
                # end if

                if new_mess == 'SendSensorData':
                    # SEND SENSOR DATA
                    # logging.info('SENDING SENSOR DATA')

                    tracker_data = track_tackers()
                    reply = tracker_data
                    # logging.info(player_one_fire+player_two_fire+player_three_fire)
                    conn.sendall(str.encode(reply + player_one_fire +
                                            player_two_fire + player_three_fire))

                    if(player_one_fire == '1'):
                        player_one_fire = '0'

                    if(player_two_fire == '1'):
                        player_two_fire = '0'

                    if(player_three_fire == '1'):
                        player_three_fire = '0'
                    # end if
                # end if

                # if a shot has been fired
                if new_mess.find('ShotsFired') != -1:

                    player = new_mess[1]
                    if (player == '1'):

                        player_one_fire = '1'
                    elif (player == '2'):

                        player_two_fire = '1'
                    elif (player == '3'):

                        player_three_fire = '1'
                    # end if

                if new_mess == 'WaitForPlayer':

                    try:
                        for client in clients:
                            client.sendall(str.encode(new_mess))
                    except socket.error as e:
                        logging.info(str(e))
                # end if
            else:
                logging.info('PLAYER REGISTER')

                try:
                    for client in clients:
                        client.sendall(str.encode(new_mess))
                except socket.error as e:
                    logging.info(str(e))
                # end try
        # end if
    # end if

    logging.info(data.decode('utf-8') + " " + reply)

    # end while

    conn.close()


while True:

    conn, addr = s.accept()
    clients.append(conn)
    logging.info("\n==========================================\n\nConnected to: " +
                 addr[0] + ':' + str(addr[1]) + "\n\n==========================================\n")

    start_new_thread(threaded_client, (conn,))
