import settings, random, path, math
client_patience = []
client_requests = []

#Set the patience and potential requests for each client
for i in range(10):
    client_patience.append(20)
    client_requests.append({settings.ROOM_BOOM:0.5, settings.ROOM_BIO:0.5, settings.ROOM_COSMO:0, settings.ROOM_PSYCH:0, settings.ROOM_INFO: 0})
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
        self.event.register("input_move", self.move_to)
        self.event.register("update", self.update)
        self.event.notify("new_entity", self.id, self.x, self.y, sprite, character)
        self.event.register("elevator_open", self.elevator_open)
        self.event.register("remove_entity", self.remove_entity)
    
    def move_to(self, entity, floor):
        if entity == self.id and floor != self.y:
            off = 0 if self.x <= 0.3 else (2 if self.x >= 0.7 else 1)
            src = self.y * 3 + off
            dest = floor * 3 + 1
            self.path = self.building.building_graph.getPath(src, dest)
            if not self.path:
                return
            if self.path.pop(0) != src:
                raise ValueError("Invalid path: start doesn't match")
            if self.path[0] // 3 == self.y:
                self.target = (self.path.pop(0) % 3) / 2.0
            else:
                self.target = (src % 3) / 2.0
    
    def update(self, dt):
        if not self.elevator:
            if self.path and self.path[0] // 3 == self.y:
                    self.target = (self.path.pop(0) % 3) / 2.0
            
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
                self.elevator = self.building.get_elevator(self.y, self.x < 0.5)
                self.elevator.call_to(self.y)
                self.waiting = True

    def elevator_open(self, id, floor):
        if self.elevator and id == self.elevator.id:
            if self.waiting:
                if floor == self.y:
                    self.waiting = not self.elevator.occupy(self.path[0] // 3)
                    if not self.waiting:
                        self.event.notify("entity_in_elevator", self.id, self.elevator.id)
            else:
                if floor == self.path[0] // 3:
                    self.path.pop(0)
                    self.event.notify("entity_in_elevator", self.id, -1)
                    self.y = floor
                    self.elevator.exit()
                    self.elevator = None
                    self.event.notify("update_entity", self.id, self.x, self.y)
    
    def remove_entity(self, id):
        if self.id == id:
            self.event.deregister("input_move", self.move_to)
            self.event.deregister("update", self.update)
            self.event.deregister("elevator_open", self.elevator_open)
            self.event.deregister("remove_entity", self.remove_entity)

class Client(Entity):
    def __init__(self, event, id, character, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 2, character, building)
        self.state = "wait_meeting"
        self.progress = 0
        self.character = character
    
    def update(self, dt):
        Entity.update(self, dt)
        self.progress += dt
        
        if self.state == "wait_meeting":
            if self.building.get_room(self.y) == settings.ROOM_MEETING:
                self.state = "meeting"
                self.progress = 0
            elif self.progress > client_patience[self.character]:
                self.state = "leaving"
                self.progress = 0
                self.event.notify("input_move", self.id, 0)
        elif self.state == "meeting":
            if self.progress > client_patience[self.character]:
                self.state = "wait_manufacture"
                self.progress = 0
        elif self.state == "wait_manufacture":
            if self.building.get_room(self.y) == settings.ROOM_BOOM:
                self.state = "manufacture"
                self.progress = 0
            elif self.progress > client_patience[self.character]:
                self.state = "leaving"
                self.progress = 0
                self.event.notify("input_move", self.id, 0)
        elif self.state == "manufacture":
            if self.building.get_room(self.y) != settings.ROOM_BOOM:
                self.state = "wait_manufacture"
            if self.progress > settings.MANUFACTURE_TIME:
                self.event.notify("entity_carrying", self.id, True)
                self.state = "leaving"
                self.progress = 0
                self.event.notify("input_move", self.id, 0)
        elif self.state == "leaving":
            if self.y == 0 and math.fabs(self.x - 0.5) < 0.01:
                self.state = "left"
                self.progress = 0
                self.event.notify("remove_entity", self.id)

class Scientist(Entity):
    def __init__(self, event, id, character, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 0, character, building)


class Igor(Entity):
    def __init__(self, event, id, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 1, -1, building)
