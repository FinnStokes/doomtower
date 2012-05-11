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
                    self.over = w
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
    
    def sprite():
        return None
    
    def move(rel):
        pass


class Button(Widget):
    def __init__(self, rect, enabled = True, event_manager = None, event = None, out = None, over = None, pressed = None):
        Widget.__init__(self, rect, enabled=enabled)
        self.over = False
        self.pressed = False
        self.out_sprite = out
        self.over_sprite = over
        self.pressed_sprite = pressed
        self.event_manager = event_manager
        self.event = None
        if event:
            if self.event_manager:
                self.event = event
            else:
                raise ValueError("event_manager missing from Button constructor.")
       
    def over(self, buttons):
        self.over = True
       
    def out(self, buttons):
        self.out = True
       
    def press(self, button):
        if button == LEFT:
            if self.event:
                self.event_manager.notify(self.event)
            self.pressed = True

    def release(self, button):
        if button == LEFT:
            self.pressed = False

    def sprite():
        if self.pressed and self.pressed_sprite:
            return self.pressed_sprite
        elif self.over and self.over_sprite:
            return self.over_sprite
        elif self.out_sprite:
            return self.out_sprite
        else:
            return None

    
class Toggle(Widget):
    def __init__(self, rect, enabled = True, event_manager = None, event = None, out = None, over = None, on = None, onover = None):
        Widget.__init__(self, rect, enabled=enabled)
        self.over = False
        self.on = False
        self.out_sprite = out
        self.over_sprite = over
        self.on_sprite = on
        self.onover_sprite = onover
        self.event_manager = event_manager
        self.event = None
        if event:
            if self.event_manager:
                self.event = event
            else:
                raise ValueError("event_manager missing from Toggle constructor.")
       
    def over(self, buttons):
        self.over = True
       
    def out(self, buttons):
        self.over = False
       
    def press(self, button):
        if button == LEFT:
            self.on = not self.on
            if self.event:
                self.event_manager.notify(self.event, self.on)
    
    def sprite():
        if self.on:
            if self.over and self.onover_sprite:
                return self.onover_sprite
            elif self.on_sprite:
                return self.on_sprite
        elif self.over and self.over_sprite:
            return self.over_sprite
        elif self.out_sprite:
            return self.out_sprite
        else:
            return None
            
class DragBar(Widget):
    def __init__(self, rect, parent, enabled = True):
        Widget.__init__(self, rect, enabled=enabled, draggable=True)
        self.parent = parent
    
    def drag(rel):
        self.parent.move(rel)

class PopupWindow:
    pass
