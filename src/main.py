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

event_manager.notify("input_elevator",True,[-1, 0, 3])
event_manager.notify("input_elevator",False,[0, 1])
event_manager.notify("input_elevator",False,[2, 3])

def close():
    global running
    running = False

event_manager.register("quit", close)
accum = 0.0
total = 0

while running:
    fpsClock.tick(30)
    event_manager.notify("update", fpsClock.get_time()/1000.0)
    event_manager.update()
    
    time =  fpsClock.get_time()/1000.0
    accum += time
    total += time
    period = settings.SPAWN_PERIOD - \
            (settings.SPAWN_PERIOD - settings.SPAWN_PERIOD_END) * \
            (total / settings.SPAWN_SCALE_TIME)
    period = max(period, settings.SPAWN_PERIOD_END)
    print(period)
    if int(accum) >= period:
        event_manager.notify("create_client")
        accum = 0.0
