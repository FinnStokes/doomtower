import pyglet

import render
import input

class View:
    def __init__(self, event_manager):
        window = pyglet.window.Window(800,600)
        
        self.render = render.Render(window, event_manager)
        self.input = input.Input(window, event_manager)
