import pygame, sys
from pygame.locals import *
import event
import model
import view

event_manager = event.Event()
player_view = view.View(event_manager)
game_model = model.Model(event_manager)
pygame.init()

fpsClock = pygame.time.Clock()
running = True

event_manager.notify("create_client")
event_manager.notify("create_scientist")
event_manager.notify("create_igor")

event_manager.notify("input_elevator",True,[-1, 0, 3])
event_manager.notify("input_elevator",False,[0, 1])
event_manager.notify("input_elevator",False,[2, 3])

def close():
    global running
    running = False

event_manager.register("quit", close)

while running:
    fpsClock.tick(30)
    #phasing out usage of refresh in favour of update
    event_manager.notify("refresh")
    event_manager.notify("update", fpsClock.get_time()/1000.0)
