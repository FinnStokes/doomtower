import pygame

import render
import input

class View:
    def __init__(self, event_manager):
        window = pygame.display.set_mode((800,600),pygame.RESIZABLE)
        pygame.display.set_caption('Doom Tower')       
        self.render = render.Render(window, event_manager)
        self.input = input.Input(window, event_manager)
