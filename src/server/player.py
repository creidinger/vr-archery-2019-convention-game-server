import logging
import json
import threading
import datetime

import server_functions as sf


class Player():
    """Handles player position and state"""

    def __init__(self):
        """Init emply player with required settings"""
        self.id = None
        self.name = None
        self.phone = None
        self.score = 0               # Running sum of player's score
        self.state = None
        self.ball_id = None
        self.start_x = None          # start pos of object thrown in game
        self.angle = 0               # angle of ball movement
        self.velocity = 0            # velocity of ball
        # leaderboard
        self.game_over = False
        self.date = str(datetime.date.today())  # required for leaderboard

    def update(self, data):
        """update player state based on incomming data"""
        # convert to string to json object
        # see conversions if you're having problems
        # https://docs.python.org/3/library/json.html#encoders-and-decoders
        try:
            data = json.loads(data)

            # updated player state
            self.id = data['id']
            self.name = data['name']
            self.phone = data['phone']
            self.score = data['score']
            self.state = data['state']
            self.ball_id = data['ball_id']
            self.start_x = data['start_x']
            self.angle = data['angle']
            self.velocity = data['velocity']
            self.game_over = data['game_over']

        except Exception as e:
            logging.error(
                f"Player.update(): {str(e)}")
            logging.error(
                f"Player.update() Player id: {self.id}: {data}\n")
            return False
        else:
            if self.velocity <= 0:
                return False
            else:
                return True

    def player_reset(self):
        """
            Reset the palyer data to ensure no data carries over between rounds
        """

        logging.info(
            f"Player.player_reset(): Player {self.id} score and time reset\n")
        self.id = 0
        self.name = ""
        self.phone = ""
        self.score = 0               # Running sum of player's score
        self.state = "innactive"
        self.ball_id = ""
        self.start_x = 0             # start pos of object thrown in game
        self.angle = 0  # angle of ball movement
        self.velocity = 0  # velocity of ball
        # leaderboard
        self.game_over = False
        self.date = str(datetime.date.today())       # required for leaderboard
