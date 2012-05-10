import pygame
from pygame.locals import *

class Input:
    def __init__(self, window, event_manager):
        self.event = event_manager
        self.widgets = list()
        self.pressed = dict()
        self.widgets.append(Button(pygame.Rect(0,0,100,100)))
        self.over = None
        self.event.register("key_down", self.key_down)
        self.event.register("mouse_move", self.mouse_move)
        self.event.register("mouse_down", self.mouse_down)
        self.event.register("mouse_up", self.mouse_up)

    def key_down(self, key):
        if key == K_UP or key == K_w:
            self.event.notify("step_scroll", True)
        elif key == K_DOWN or key == K_s:
            self.event.notify("step_scroll", False)
        elif key == K_ESCAPE:
            self.event.notify("toggle_menus", False)
    
    def mouse_move(self, pos, rel, buttons):
        if buttons[0] and self.over and self.over.draggable:
            self.over.drag(rel)
        else:
            for w in self.widgets:
                if w == self.over and w.contains(pos):
                    break
                if w.enabled and w.contains(pos):
                    w.over(buttons)
                    if self.over:
                        self.over.out(buttons)
                        self.over = None
                    break
            if self.over and not self.over.contains(pos):
                self.over.out(buttons)
                self.over = None
    
    def mouse_down(self, pos, button):
        for w in self.widgets:
            if w.enabled and w.contains(pos):
                w.press(button)
                if button in self.pressed:
                    self.pressed[button].release(button)
                self.pressed[button] = w
                break
    
    def mouse_up(self):
        for button in self.pressed:
            self.pressed[button].release(button)
        self.pressed.clear()

class Widget:
    def __init__(self, rect, enabled = True, draggable = False):
        self.rect = rect
        self.enabled = enabled
        self.draggable = draggable

    def contains(self, point):
        return self.rect.collidepoint(point)
    
    def over(self, buttons):
        pass
    
    def out(self, buttons):
        pass
    
    def press(self, button):
        pass
    
    def release(self, button):
        pass
    
    def drag(self, rel):
        pass

class Button(Widget):
    def __init__(self, rect, enabled = True):
        Widget.__init__(self, rect, enabled)
       
    def over(self, buttons):
        pass#print "over"
       
    def out(self, buttons):
        print "out"
       
    def press(self, button):
        print "press "+repr(button)
       
    def release(self, button):
        print "release "+repr(button)
