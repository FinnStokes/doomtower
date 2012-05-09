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
    event_manager.notify("refresh")
    event_manager.notify("update", fpsClock.get_time()/1000.0)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            pygame.display.set_mode((event.size),pygame.RESIZABLE) 
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                event_manager.notify("step_scroll", True)
            elif event.key == K_DOWN:
                event_manager.notify("step_scroll", False)
