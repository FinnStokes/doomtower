import pygame, sys
from pygame.locals import *
import event
import model
import view
import settings
title_screen = pygame.image.load("img/DoomTowerTitleScreen.png")
window = pygame.display.set_mode((1024,600),pygame.RESIZABLE)
while True:
    e = pygame.event.wait()
    if e.type in (KEYDOWN, MOUSEBUTTONDOWN):
        break
    elif e.type == VIDEORESIZE:
        pygame.display.set_mode((e.size),pygame.RESIZABLE) 
    elif e.type == QUIT:
        sys.exit()
    width, height = window.get_size()
    window.fill((217,86,74))
    window.blit(title_screen, ((width-1024)/2,(height-600)/2))
    pygame.display.update()
event_manager = event.Event()
player_view = view.View(event_manager,window)
game_model = model.Model(event_manager)
pygame.init()

fpsClock = pygame.time.Clock()
running = True

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
accum = settings.SPAWN_PERIOD_END
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
    if int(accum) >= period:
        event_manager.notify("create_client")
        accum = 0.0
