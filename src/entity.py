import settings
import random

class Manager:
    def __init__(self, event):
        self.event = event
        self.nextId = 0
        event.register("create_client", self.create_client)
        event.register("create_scientist", self.create_scientist)
        event.register("create_igor", self.create_igor)
    
    def create_client(self):
        e = Client(self.event, self.nextId, random.randint(0,10), settings.SPAWN_POSITION, settings.SPAWN_FLOOR)
        self.nextId = self.nextId + 1
    
    def create_scientist(self):
        e = Scientist(self.event, self.nextId, random.randint(0,10), settings.SPAWN_POSITION, settings.SPAWN_FLOOR)
        self.nextId = self.nextId + 1
    
    def create_igor(self):
        e = Igor(self.event, self.nextId, settings.SPAWN_POSITION, settings.SPAWN_FLOOR)
        self.nextId = self.nextId + 1
    
class Entity:
    def __init__(self, event, id, character, x, floor, sprite):
        self.id = id
        self.x = x
        self.y = floor
        self.target = self.x
        self.speed = settings.ENTITY_SPEED
        self.event = event
        self.character = character
        event.register("input_move", self.move_to)
        event.register("update", self.update)
        event.notify("new_entity", self.id, self.character, self.x, self.y, sprite)
    
    def move_to(self, entity, floor):
        if entity == self.id:
            if floor != self.y:
                self.target = 0
                self.y = floor
    
    def update(self, dt):
        if self.x != self.target:
            if abs(self.x - self.target) < self.speed*dt:
                self.x = self.target
            else:
                if self.x < self.target:
                    self.x = self.x + self.speed*dt
                else:
                    self.x = self.x - self.speed*dt
            self.event.notify("update_entity", self.id, self.x, self.y)

class Client(Entity):
    def __init__(self, event, id, character, x, floor):
        Entity.__init__(self, event, id, character, x, floor, 2)

class Scientist(Entity):
    def __init__(self, event, id, character, x, floor):
        Entity.__init__(self, event, id, character, x, floor, 0)

class Igor(Entity):
    def __init__(self, event, id, x, floor):
        Entity.__init__(self, event, id, 0, x, floor, 1)
