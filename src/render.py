import pyglet
import settings

pyglet.resource.path = ['../img']
pyglet.resource.reindex()
room_image = pyglet.resource.image('rooms.png')
room = pyglet.sprite.Sprite(room_image, 100,100);
#room_sprites = pyglet.image.ImageGrid(room_image, 4, 1);
class Render:
    def __init__(self, window, event_manager):
        window.push_handlers(self)
        event_manager.push_handlers(self)
        
        self.window = window
        self.label = pyglet.text.Label('Hello, world',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=window.width//2, y=window.height//2,
                                  anchor_x='center', anchor_y='center')
        self.rooms = []
        for i in range(settings.TOP_FLOOR-settings.BOTTOM_FLOOR+1):
            self.rooms.append(Room(0))

    def on_draw(self): # render current game state
        self.window.clear()
        self.label.draw()
        room.draw()
    
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