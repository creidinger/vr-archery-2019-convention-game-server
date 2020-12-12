# Main socket client that sends player data to Server
# Author: Chase Reidinger

import socket
import threading
import sys
import time
import os
from bow import *
# from player import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#socket config
server = '192.168.2.10'
port = 8000

#Player Data
player_id = os.getenv('PLAYER')    # Player number assocated w/ the PI
shot = False                    # if this is true, send to server


def connect_to_server():
    '''
    Keep trying to connect to socket server.py
    '''

    connected = False

    while not connected:
        try:
            logging.info("connect_to_server(): Connecting to " + server + ":" + str(port))
            logging.info("="*80 + "\n")
            s.connect((server, port))
            connected = True

            response = s.recv(2048)
            logging.info("connect_to_server(): Server Response: ", repr(response))
            logging.info("")

        except socket.error as e:
            logging.info(str(e) + "\n")
            time.sleep(2)
# End connect_to_server()


def register_player():
    '''
    Send player ID and scanner data to server.property
    when barcode is scanned.
    '''

    player = os.getenv('PLAYER')    # Player number assocated w/ the PI

    logging.info("register_player(): Scan player data")
    scan = input()

    data = player_id + ' | ' + scan

    try:
        send_data = "PlayerRegister " + data + " <EOF>"
        s.sendall(send_data.encode("utf-8"))
        logging.info("Data send to server: " + send_data)

    except socket.error as e:
        logging.info("\nError: Unable to register player\n")
        logging.info(str(e) + "\n")
# end register_player()



#### HEADER
logging.info("\n" + "="*80 +  "\n")
logging.info("Archery Game socket client \nPlayer: " + player_id)
logging.info("\n" + "="*80 +  "\n")


connect_to_server()

'''
Enter Main loop
'''

while True:

    # Player register thread
    # Enables ability to register new players while sending shots
    thread1 = threading.Thread(target=register_player)
    thread1.daemon = True
    thread1.start()

    # Get IR data from the bow and determine if a
    # shot has been fired.
    shot = send_shot_data()

    if(shot == True):
        try:
            send_data = player_id + " ShotsFired <EOF>"
            s.sendall(send_data.encode("utf-8"))

        except socket.error as e:
            logging.info("Error: Unable to send Shot!")
            logging.info(str(e) + "\n")
        # end try
    else:
        continue
    # end if

    shot = False # reset

# end while
