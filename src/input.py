import pygame
from pygame.locals import *

import settings

interface_btn = pygame.image.load('img/Buttons.png')
build = pygame.image.load('img/GUI_Build.png')
hire = pygame.image.load('img/GUI_Hire.png')
buildhire_btn = pygame.image.load('img/BuildHireButtons.png')
footer = pygame.image.load('img/GUI_Footer.png')

class Input:
    def __init__(self, window, event_manager, render):
        self.event = event_manager
        self.window = window
        self.render = render
        
        self.widgets = list()
        self.pressed = dict()
        self.over = None
        self.drag = None
        
        self.event.register("key_down", self.key_down)
        self.event.register("mouse_move", self.mouse_move)
        self.event.register("mouse_down", self.mouse_down)
        self.event.register("mouse_up", self.mouse_up)
        self.event.register("window_resize", self.window_resize)
        event_manager.register("new_entity", self.new_entity)
        event_manager.register("remove_entity", self.remove_entity)

        self.hire_btn = Toggle(pygame.Rect(20, 0, 128, 43),
                               out=buildhire_btn.subsurface(pygame.Rect(0,43,128,43)),
                               over=buildhire_btn.subsurface(pygame.Rect(128,43,128,43)),
                               on=buildhire_btn.subsurface(pygame.Rect(128,43,128,43)),
                               event_manager=event_manager, event="open_hire")
        self.build_btn = Toggle(pygame.Rect(168, 0, 128, 43),
                                out=buildhire_btn.subsurface(pygame.Rect(0,0,128,43)),
                                over=buildhire_btn.subsurface(pygame.Rect(128,0,128,43)),
                                on=buildhire_btn.subsurface(pygame.Rect(128,0,128,43)),
                                event_manager=event_manager, event="open_build")
        self.widgets.append(self.hire_btn)
        self.widgets.append(self.build_btn)
        
        self.footer = Static(pygame.Rect(0, 0, 384, 64), footer)
        self.widgets.append(self.footer)
        
        build_popup = PopupWindow(pygame.Rect(20, 20, 384, 384), build, interface_btn, event_manager, open_event="open_build", open = False)
        self.widgets.extend(build_popup.widgets)
        
        hire_popup = PopupWindow(pygame.Rect(20, 20, 384, 384), hire, interface_btn, event_manager, open_event="open_hire", open = False)
        self.widgets.extend(hire_popup.widgets)
        
        self.window_resize(self.window.get_size())
    
    def window_resize(self, size):
        self.footer.rect.bottom = size[1]
        self.hire_btn.rect.bottom = size[1] - 10
        self.build_btn.rect.bottom = size[1] - 10
    
    def key_down(self, key):
        if key == K_UP or key == K_w:
            self.event.notify("step_scroll", True)
        elif key == K_DOWN or key == K_s:
            self.event.notify("step_scroll", False)
        elif key == K_ESCAPE:
            self.event.notify("toggle_menus", False)
    
    def mouse_move(self, pos, rel, buttons):
        if buttons[0] and self.drag:
            self.drag.drag(rel)
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
                if button == 1 and w.draggable:
                    self.drag = w
                break
    
    def mouse_up(self, pos, button):
        if button == 1 and self.drag:
            self.drag = None
        if button in self.pressed:
            self.pressed[button].release(button)
            del self.pressed[button]
    
    def draw(self):
        for widget in reversed(self.widgets):
            sprite = widget.sprite()
            if sprite:
                self.window.blit(sprite, widget.rect.topleft)
    
    def new_entity(self, id, x, y, sprite, character):
        entity = Entity(pygame.Rect(0,0,100,128), id, x, y, self.event, self.render)
        self.widgets.append(entity)
    
    def remove_entity(self, id):
        pass

class Widget:
    def __init__(self, rect, enabled = True, draggable = False, visible = True):
        self.rect = rect
        self.enabled = enabled
        self.draggable = draggable
        self.visible = visible

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
    
    def sprite(self):
        return None
    
    def move(self, rel):
        self.rect = self.rect.move(rel[0],rel[1])
    

class Button(Widget):
    def __init__(self, rect, enabled = True, event_manager = None, event = None, out = None, over = None, pressed = None, on_press = None):
        Widget.__init__(self, rect, enabled=enabled)
        self.is_over = False
        self.is_pressed = False
        self.out_sprite = out
        self.over_sprite = over
        self.pressed_sprite = pressed
        self.event_manager = event_manager
        self.event = None
        self.on_press = on_press
        if event:
            if self.event_manager:
                self.event = event
            else:
                raise ValueError("event_manager missing from Button constructor.")
    
    def drag(self, rel):
        self.move(rel)
    
    def over(self, buttons):
        self.is_over = True
       
    def out(self, buttons):
        self.is_over = False
       
    def press(self, button):
        if button == 1:
            if self.on_press:
                self.on_press()
            if self.event:
                self.event_manager.notify(self.event)
            self.is_pressed = True

    def release(self, button):
        if button == 1:
            self.is_pressed = False

    def sprite(self):
        if not self.visible:
            return None
        elif self.is_pressed and self.pressed_sprite:
            return self.pressed_sprite
        elif self.is_over and self.over_sprite:
            return self.over_sprite
        elif self.out_sprite:
            return self.out_sprite
        else:
            return None

    
class Toggle(Widget):
    def __init__(self, rect, enabled = True, event_manager = None, event = None, out = None, over = None, on = None, onover = None):
        Widget.__init__(self, rect, enabled=enabled)
        self.is_over = False
        self.is_on = False
        self.out_sprite = out
        self.over_sprite = over
        self.on_sprite = on
        self.onover_sprite = onover
        self.event_manager = event_manager
        self.event = None
        if event:
            if self.event_manager:
                self.event = event
                self.event_manager.register(self.event,self.set_state)
            else:
                raise ValueError("event_manager missing from Toggle constructor.")
       
    def over(self, buttons):
        self.is_over = True
       
    def out(self, buttons):
        self.is_over = False
       
    def press(self, button):
        if button == 1:
            self.is_on = not self.is_on
            if self.event:
                self.event_manager.notify(self.event, self.is_on)

    def set_state(self, state):
        self.is_on = state
    
    def sprite(self):
        if not self.visible:
            return None
        elif self.is_on:
            if self.is_over and self.onover_sprite:
                return self.onover_sprite
            elif self.on_sprite:
                return self.on_sprite
        elif self.is_over and self.over_sprite:
            return self.over_sprite
        elif self.out_sprite:
            return self.out_sprite
        else:
            return None
            
class DragBar(Widget):
    def __init__(self, rect, parent, enabled = True):
        Widget.__init__(self, rect, enabled=enabled, draggable=True)
        self.parent = parent
    
    def drag(self, rel):
        self.parent.move(rel)

class Static(Widget):
    def __init__(self, rect, sprite):
        Widget.__init__(self, rect, enabled=False)
        self.__sprite = sprite
    
    def sprite(self):
        if self.visible:
            return self.__sprite
        else:
            return None

class PopupWindow:
    def __init__(self, rect, window_sprite, close_sprite, event_manager, open_event = None, open = False):
        self.widgets = list()
        self.widgets.append(Button(pygame.Rect(rect.right-49,rect.top+10,39,28),
                                   out=close_sprite.subsurface(pygame.Rect(0,0,39,28)),
                                   over=close_sprite.subsurface(pygame.Rect(39,0,39,28)),
                                   on_press=self.close))
        self.widgets.append(DragBar(pygame.Rect(rect.left, rect.top, rect.width, settings.DRAGBAR_HEIGHT), self))
        self.widgets.append(Static(rect, window_sprite))
        self.set_open(open)
        self.event_manager = event_manager
        self.open_event = open_event
        if open_event:
            event_manager.register(open_event, self.set_open)
    
    def set_open(self, open):
        self.__open = open
        for widget in self.widgets:
            widget.visible = open
            widget.enabled = open
    
    def close(self):
        self.set_open(False)
        self.event_manager.notify(self.open_event, False)
    
    def open(self):
        self.set_open(True)
        self.event_manager.notify(self.open_event, True)
    
    def move(self, rel):
        for w in self.widgets:
            w.move(rel)

class Entity(Widget):
    def __init__(self, rect, entity_id, entity_x, entity_y, event_manager, render):
        Widget.__init__(self, rect)
        self.entity_id = entity_id
        self.entity_x = entity_x
        self.entity_y = entity_y
        self.render = render
        event_manager.register("update_entity", self.update_entity)
    
    def update_entity(self, id, x, y):
        if self.entity_id == id:
            self.entity_x = x
            self.entity_y = y
    
    def update(self, dt):
            self.rect.bottomleft = render.get_screen_pos((self.entity_x, self.entity_y))
        
        
