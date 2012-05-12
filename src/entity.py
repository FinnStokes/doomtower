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
        e = Client(self.event, self.nextId, random.randint(0,9), settings.SPAWN_POSITION, settings.SPAWN_FLOOR, self.building)
        self.nextId = self.nextId + 1
    
    def create_scientist(self):
        e = Scientist(self.event, self.nextId, random.randint(0,9), settings.SPAWN_POSITION, settings.SPAWN_FLOOR, self.building)
        self.nextId = self.nextId + 1
    
    def create_igor(self):
        e = Igor(self.event, self.nextId, settings.SPAWN_POSITION, settings.SPAWN_FLOOR, self.building)
        self.nextId = self.nextId + 1

class Entity:
    def __init__(self, event, id, x, floor, sprite, character, building):
        self.id = id
        self.x = x
        self.y = floor
        self.target = self.x
        self.path = None
        self.waiting = False
        self.speed = settings.ENTITY_SPEED
        self.event = event
        self.building = building
        self.elevator = None
        event.register("input_move", self.move_to)
        event.register("update", self.update)
        event.notify("new_entity", self.id, self.x, self.y, sprite, character)
    
    def move_to(self, entity, floor):
        if entity == self.id and floor != self.y:
            off = (0, 1)[self.x <= 0.5]
            src = self.y * 2 + off
            dest = floor * 2
            self.path = self.building.building_graph.getPath(src, dest)
            if not self.path:
                print self.building.building_graph.getEdge(src,dest)
                print "no path from "+repr(src)+" to "+repr(dest)
                return
            if self.path.pop(0) != src:
                raise ValueError("Invalid path: start doesn't match")
            if self.path[0] // 2 == self.y:
                self.target = self.path.pop(0) % 2
            else:
                self.target = src % 2
    
    def update(self, dt):
        if not self.elevator:
            if self.path and self.path[0] // 2 == self.y:
                    self.target = self.path.pop(0) % 2
            
            if self.x != self.target:
                if abs(self.x - self.target) < self.speed*dt:
                    self.x = self.target
                else:
                    if self.x < self.target:
                        self.x = self.x + self.speed*dt
                    else:
                        self.x = self.x - self.speed*dt
                self.event.notify("update_entity", self.id, self.x, self.y)
            elif self.path:
                self.building.get_elevator(self.y, self.x < 0.5).call_to(self.y)
                pass # Call elevator


class Client(Entity):
    def __init__(self, event, id, character, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 2, character, building)

class Scientist(Entity):
    def __init__(self, event, id, character, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 0, character, building)


class Igor(Entity):
    def __init__(self, event, id, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 1, -1, building)
