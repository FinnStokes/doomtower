import pygame, sys
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
        self.input = input.Input(window, event_manager, render)
    
    def update(self, dt):
        
        for e in pygame.event.get():
            if e.type == QUIT:
                self.event.notify("quit")
            elif e.type == VIDEORESIZE:
                pygame.display.set_mode((e.size),pygame.RESIZABLE) 
                self.event.notify("window_resize", e.size)
            elif e.type == KEYDOWN:
                self.event.notify("key_down", e.key)
            elif e.type == KEYUP:
                self.event.notify("key_up", e.key)
            elif e.type == MOUSEMOTION:
                self.event.notify("mouse_move", e.pos, e.rel, e.buttons)
            elif e.type == MOUSEBUTTONDOWN:
                self.event.notify("mouse_down", e.pos, e.button )
            elif e.type == MOUSEBUTTONUP:
                self.event.notify("mouse_up", e.pos, e.button)

        self.render.draw()
        self.input.draw()
        pygame.display.update()
