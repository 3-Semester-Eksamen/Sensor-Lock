from sense_hat import SenseHat
from random import randint
from socket import *
from datetime import datetime
import os

sense = SenseHat()
s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
BROADCAST_PORT = 7001;

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

last_change = datetime.utcnow()
#Makes sure that a specified amount of time, has passed, since the last call of the function.
def anti_spam(event):
    if event.action == "pressed":
        global last_change
        if (datetime.utcnow() - last_change).seconds >= 10:
            stick_direction_change(event)
            last_change = datetime.utcnow();


#Represents an event, that should be fired once a "user" tries to unlock the door with a key card.
#Currently using the JoyStick of the SenseHat PI.
card_ids = { "up": 1, "down": 2, "left": 3, "right": 4 }
def stick_direction_change(event):
    id_key_card = card_ids[event.direction]
    id_door = 1;
    msg = "door opened" if event.action == "pressed" else "door closed"
    broadcast_result(id_key_card, id_door, msg)
    show_result(id_key_card, id_door, msg)


def broadcast_result(id_key_card, id_door, msg):
    data = str(id_key_card) + "," + str(id_door) + "," + msg
    s.sendto(data.encode(), ("255.255.255.255", BROADCAST_PORT))
    print("Broad casted: " + data)


def show_result(id_key_card, id_door, msg):
    sense.show_message(str(id_key_card), text_colour = green, back_colour = blue)


sense.stick.direction_any = anti_spam

while True:
    pass