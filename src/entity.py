import settings
import random
import path

class Manager:
    def __init__(self, event, building):
        self.event = event
        self.building = building
        self.nextId = 0
        event.register("create_client", self.create_client)
        event.register("create_scientist", self.create_scientist)
        event.register("create_igor", self.create_igor)
    
    def create_client(self):
        e = Client(self.event, self.nextId, random.randint(0,9), settings.SPAWN_POSITION, settings.SPAWN_FLOOR)
        self.nextId = self.nextId + 1
    
    def create_scientist(self):
        e = Scientist(self.event, self.nextId, random.randint(0,9), settings.SPAWN_POSITION, settings.SPAWN_FLOOR)
        self.nextId = self.nextId + 1
    
    def create_igor(self):
        e = Igor(self.event, self.nextId, settings.SPAWN_POSITION, settings.SPAWN_FLOOR)
        self.nextId = self.nextId + 1
    
class Entity:
    def __init__(self, event, id, x, floor, sprite, character, building):
        self.id = id
        self.x = x
        self.y = floor
        self.target = self.x
        self.speed = settings.ENTITY_SPEED
        self.event = event
        self.building = building
        event.register("input_move", self.move_to)
        event.register("update", self.update)
        event.notify("new_entity", self.id, self.x, self.y, sprite, character)
    
    def move_to(self, entity, floor):
        
        off = (0, 1)[self.x <= 0.5]
        src = self.y * 2 + off
        dest = floor * 2
    
        if entity == self.id:
            if floor != self.y:
                self.building.building_graph.getPath(src, dest)           
                #self.target = 0
                #self.y = floor
    
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
    def __init__(self, event, id, character, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 2, character, building)

class Scientist(Entity):
    def __init__(self, event, id, character, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 0, character, building)


class Igor(Entity):
    def __init__(self, event, id, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 1, -1, building)
