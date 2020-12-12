# Bow related functions
# Author: Chase Reidinger
#
# Wires:
# -- Red: 3 or 5v power
# -- Yellow: GPIO
# -- Black: Ground
#
import RPi.GPIO as GPIO

# GPIO config required to get sensor data
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #listen on pin 7

def bow_ir_data():
    '''
    Get data from IR sensors
    '''

    if(GPIO.input(7) == 0):
       # logging.info("send_shot_data(): Beam Broken")
       return False
    elif(GPIO.input(7) == 1):
       # logging.info("send_shot_data(): Beam Solid")
       return True
    # end if
# end bow_ir_data()


def send_shot_data():
    '''
    Detect a shot
    '''

    ir_data = False
    bow_drawn = False

    while True:

        ir_data = bow_ir_data()

        # If beam is connected set bow_drawn to true
        if(ir_data == True):
            bow_drawn = True
        # end if

        # When the arrow is release and the IR changes to broken
        # send a shot
        if(bow_drawn == True and ir_data == False):

            bow_drawn = False

            logging.info('send_shot_data(): Fired')

            return True
        # end if
    # end while
# end send_shot_data()
