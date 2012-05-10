import pygame
from pygame.locals import *
import render
import input

class View:
    def __init__(self, event_manager):
        self.event = event_manager
        self.event.register("update", self.update)
        window = pygame.display.set_mode((800,600),pygame.RESIZABLE)
        pygame.display.set_caption('Doom Tower')       
        self.render = render.Render(window, event_manager)
        self.input = input.Input(window, event_manager)
    
    def update(self, dt):
        
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
            elif e.type == VIDEORESIZE:
                pygame.display.set_mode((e.size),pygame.RESIZABLE) 
            elif e.type == KEYDOWN:
                self.event.notify("key_down", e.key)
            elif e.type == KEYUP:
                self.event.notify("key_up", e.key)
