import pygame, sys
from pygame.locals import *
import event
import model
import view
import settings

event_manager = event.Event()
player_view = view.View(event_manager)
game_model = model.Model(event_manager)
pygame.init()

fpsClock = pygame.time.Clock()
running = True

event_manager.notify("create_client")

event_manager.notify("input_elevator",True,[-4, -2, 0, 2, 4, 6, 8, 10])
event_manager.notify("input_elevator",False,[-5, -4])
event_manager.notify("input_elevator",False,[-3, -2])
event_manager.notify("input_elevator",False,[-1, 0, 1])
event_manager.notify("input_elevator",False,[2, 3])
event_manager.notify("input_elevator",False,[4, 5])
event_manager.notify("input_elevator",False,[6, 7])
event_manager.notify("input_elevator",False,[8, 9])

def close():
    global running
    running = False

event_manager.register("quit", close)
accum = 0.0

while running:
    fpsClock.tick(30)
    event_manager.notify("update", fpsClock.get_time()/1000.0)
    event_manager.update()
    accum +=  fpsClock.get_time()/1000.0
    if int(accum) >= settings.SPAWN_PERIOD:
        event_manager.notify("create_client")
        accum = 0.0    
       

