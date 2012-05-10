from pygame.locals import *

class Input:
    def __init__(self, window, event_manager):
        self.event = event_manager
        self.event.register("key_down", self.key_down)

    def key_down(self, key):
        if key == K_UP:
            self.event.notify("step_scroll", True)
        elif key == K_DOWN:
            self.event.notify("step_scroll", False)


