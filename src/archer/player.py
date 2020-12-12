# Player related functions
# Author: Chase Reidinger
#
import os

def register_player():
    '''
    Send player ID and scanner data Barcode is scanned
    '''

    player_id = os.getenv('PLAYER')    # Player number assocated w/ the PI

    logging.info("register_player(): Scan player data")
    scan = input()

    data = player_id + ' | ' + scan

    return data
# end register_player()
