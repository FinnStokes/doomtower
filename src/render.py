import pygame
from pygame.locals import *
import settings

room_image = pygame.image.load('../img/rooms.png')
#room = pyglet.sprite.Sprite(room_image, 100,100);
#room_sprites = pyglet.image.ImageGrid(room_image, 4, 1);
class Render:
    def __init__(self, window, event_manager):
        self.event = event_manager
        self.event.register("update_room", self.update_room)
        self.event.register("add_entity", self.add_entity)
        self.event.register("remove_entity", self.remove_entity)
        self.event.register("update_entity", self.update_entity)
        self.event.register("add_elevator", self.add_elevator)
        self.event.register("remove_elevator", self.remove_elevator)
        self.event.register("update_elevator", self.update_elevator)
        self.event.register("refresh", self.on_draw)
        
        self.window = window
        self.rooms = []
        for i in range(settings.TOP_FLOOR-settings.BOTTOM_FLOOR+1):
            self.rooms.append(Room(0))

    def on_draw(self): # render current game state
        self.window.fill((255,255,0))
        pygame.display.update()
    
    def update_room(self, floor, room_id):
        self.rooms(floor + settings.BOTTOM_FLOOR).update(room_id)
    
    def add_entity(self, id, x, y, sprite):
        pass # create entity with given sprite at given position
    
    def remove_entity(self, id):
        pass
    
    def update_entity(self, id, x, y):
        pass # change entity position
    
    def add_elevator(self, id, left, floors, y):
        pass # create lift servicing given floors, on the left if left is true and on the right if it is false, starting at floor y (may be non-integer)
    
    def remove_elevator(self, id):
        pass
    
    def update_elevator(self, id, y):
        pass # move elevator to floor y (may be non-integer)
    

class Room:
    def __init__(self, room_id):
        self.id = room_id
        
    def update(self, room_id):
        self.id = room_id