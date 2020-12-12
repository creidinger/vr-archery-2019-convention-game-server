import sys
import logging
import socket
import threading
import time
import json

from threader import ThreadedServer
from game_state import Game

# Basic setup
logging.basicConfig(filename="log/server.log", level=logging.DEBUG)


def run_game():
    """Initialize game and start loop"""

    logging.info('run_game: Game Start')

    logging.info('run_game: device network settings')
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    logging.info(f"run_game: hostname: {hostname}")
    logging.info(f"run_game: ip address: {ip_addr}")

    # game = Game()

    # Main loop
    # Always attempts socket connection
    while True:
        ThreadedServer(ip_addr, 8000, game).bind()
        time.sleep(2)


if __name__ == '__main__':
    logging.info("")
    logging.info("================================")
    logging.info("main.py: Socket Server init")
    logging.info("================================")
    run_game()
