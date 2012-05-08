import pygame
from pygame.locals import *
import event
import model
import view

event_manager = event.Event()
game_model = model.Model(event_manager)
player_view = view.View(event_manager)
pygame.init()

fpsClock = pygame.time.Clock()

while True:
    event_manager.notify("refresh")
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit();
            sys.exit;
    fpsClock.tick(30)
