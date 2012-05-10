import pygame, sys
from pygame.locals import *
import event
import model
import view

event_manager = event.Event()
player_view = view.View(event_manager)
game_model = model.Model(event_manager)
pygame.init()

event_manager.notify("create_client")
event_manager.notify("input_move",0,2)

fpsClock = pygame.time.Clock()
running = True
while running:
    fpsClock.tick(30)
    #phasing out usage of refresh in favour of update
    event_manager.notify("refresh")
    event_manager.notify("update", fpsClock.get_time()/1000.0)
