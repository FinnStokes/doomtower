import pygame, sys
from pygame.locals import *
import event
import model
import view

event_manager = event.Event()
game_model = model.Model(event_manager)
player_view = view.View(event_manager)
pygame.init()

fpsClock = pygame.time.Clock()
running = True
while running:
    fpsClock.tick(30)
    event_manager.notify("refresh")
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            pygame.display.set_mode((event.size),pygame.RESIZABLE) 
