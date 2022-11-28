from sense_hat import SenseHat
from random import randint
# from socket import *
from datetime import datetime
import math
import os

sense = SenseHat()
# s = socket(AF_INET, SOCK_DGRAM)
# s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
# BROADCAST_PORT = 7001;

colors = {"empty": (0, 0, 0), "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255)}


# Function that gets the MAC-address of the Raspberry IP, and returns it.
def get_sensor_mac_address():
    # Placeholder MAC-Address
    return "00:00:5e:00:53:af"


# Function that gets called, once the joystick on the SenseHat is fired.
def trigger_open(event):
    # Only fire if the event is pressed.
    if event.action == "pressed":
        handle_input(get_id_from_humid())


# Function that should be called, to generate a test id.
def get_id_from_humid():
    return math.floor(sense.get_humidity() / 10)


# Function that handles the input, and reflecting that in the SenseHat display.
# where colors define what happened, if anything.
# Function can also only ever execute, if it's been more that X-seconds, since last executing,
# to prevent overloading of the sensor.
# Id is the user, that tried to open the door.
last_change = datetime.utcnow()


def handle_input(idKey):
    global last_change
    # Guard clause, that prevents overloading of the sensor.
    if (datetime.utcnow() - last_change).seconds >= 1:
        last_change = datetime.utcnow()
        # Only allow entry, if the id is a power of 2.
        if idKey % 2 == 0:
            accept_entry(idKey)
        else:
            deny_entry(idKey)


# Function that represents a succesfull access to the lock.
def accept_entry(idKey):
    e = colors["empty"]
    g = colors["green"]
    pixels = [
        e, e, e, e, e, e, e, e,
        e, e, e, e, e, e, e, g,
        e, e, e, e, e, e, g, e,
        e, e, e, e, e, g, e, e,
        g, e, e, e, g, e, e, e,
        e, g, e, g, e, e, e, e,
        e, e, g, e, e, e, e, e,
        e, e, e, e, e, e, e, e
    ]
    sense.set_pixels(pixels)
    # DoBroadcast


# Function that represents a failed access to the lock.
def deny_entry(idKey):
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


sensor_id = get_sensor_mac_address()
sense.stick.direction_any = trigger_open

while True:
    pass