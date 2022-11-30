from sense_hat import SenseHat
from udp_broadcaster import Broadcast
from random import randint
from datetime import datetime
from time import sleep
from threading import Timer
import math
import os

OPEN_DURATION = 1
BROADCAST_PORT = 7001
MAC_ADDRESS = "00:00:5e:00:53:af"

sense = SenseHat()
udp = Broadcast(MAC_ADDRESS, BROADCAST_PORT)

colors = {"empty": (0, 0, 0), "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0)}
# Lock state indicates, whether current access is being handled. To make opening the door, run synchronously.
lock_ready = False


# Function that gets called, once the joystick on the SenseHat is fired.
def trigger_open(event):
    global lock_ready
    # Only fire if the event is pressed.
    if (event.action == "pressed") and (lock_ready is True):
        lock_ready = False
        handle_input(get_sensor_id())


# Function that should be called, to generate a test id.
# During testing a number between 1 and 10 is returned.
def get_sensor_id():
    return randint(0, 10)


# Function that handles the input, and reflecting that in the SenseHat display.
# where colors define what happened, if anything.
# Function can also only ever execute, if it's been more that X-seconds, since last executing,
# to prevent overloading of the sensor.
# Id is the user, that tried to open the door.
def handle_input(id_key):
    if id_key > 2:
        accept_entry(id_key)
    else:
        deny_entry(id_key)


# Function that represents successful access to the lock.
def accept_entry(id_key):
    e = colors["empty"]
    g = colors["green"]
    pixels = [
        e, e, e, e, e, e, e, e,
        e, e, e, e, e, e, e, e,
        e, e, e, e, e, e, g, e,
        e, e, e, e, e, g, e, e,
        e, e, e, e, g, e, e, e,
        e, g, e, g, e, e, e, e,
        e, e, g, e, e, e, e, e,
        e, e, e, e, e, e, e, e
    ]
    sense.set_pixels(pixels)
    Timer(1, standby_entry).start()
    udp.broadcast('"sensor": "' + MAC_ADDRESS + '", "opened_by": "' + str(id_key) + '", "message": "door opened"')


# Function that represents failed access to the lock.
def deny_entry(id_key):
    e = colors["empty"]
    r = colors["red"]
    pixels = [
        e, e, e, e, e, e, e, e,
        e, r, e, e, e, e, r, e,
        e, e, r, e, e, r, e, e,
        e, e, e, r, r, e, e, e,
        e, e, e, r, r, e, e, e,
        e, e, r, e, e, r, e, e,
        e, r, e, e, e, e, r, e,
        e, e, e, e, e, e, e, e
    ]
    sense.set_pixels(pixels)
    Timer(1, standby_entry).start()


def standby_entry():
    e = colors["empty"]
    y = colors["yellow"]
    pixels = [
        e, e, e, e, e, e, e, e,
        e, y, y, e, e, y, y, e,
        e, y, e, e, e, e, y, e,
        e, e, e, e, e, e, e, e,
        e, e, e, e, e, e, e, e,
        e, y, e, e, e, e, y, e,
        e, y, y, e, e, y, y, e,
        e, e, e, e, e, e, e, e
    ]
    sense.set_pixels(pixels)
    global lock_ready
    lock_ready = True


sense.stick.direction_any = trigger_open
standby_entry()

while True:
    pass
