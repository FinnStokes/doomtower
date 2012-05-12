import settings, random, path

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
        event.register("elevator_open", self.elevator_open)
        event.register("remove_entity", self.remove_entity)
    
    def move_to(self, entity, floor):
        if entity == self.id and floor != self.y:
            off = (0, 1)[self.x <= 0.5]
            src = self.y * 2 + off
            dest = floor * 2
            self.path = self.building.building_graph.getPath(src, dest)
            if not self.path:
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
                self.elevator = self.building.get_elevator(self.y, self.x < 0.5)
                self.elevator.call_to(self.y)
                self.waiting = True

    def elevator_open(self, id, floor):
        if self.elevator and id == self.elevator.id:
            if self.waiting:
                if floor == self.y:
                    self.waiting = not self.elevator.occupy(self.path[0] // 2)
                    if self.waiting:
                        self.event.notify("entity_in_elevator", self.id, self.elevator.id)
            else:
                if floor == self.path[0] // 2:
                    self.event.notify("entity_in_elevator", self.id, -1)
                    self.y = floor
                    self.elevator.exit()
                    self.elevator = None
                    self.event.notify("update_entity", self.id, self.x, self.y)
    
    def remove_entity(self, id):
        if self.id == id:
            self.event.deregister("input_move", self.move_to)
            self.event.deregister("update", self.update)

class Client(Entity):
    def __init__(self, event, id, character, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 2, character, building)
        self.state = "wait_meeting"
        self.progress = 0
    
    def update(self, dt):
        Entity.update(self, dt)
        self.progress += dt
        
        if self.state == "wait_meeting":
            if self.building.get_room(self.y) == 7:
                self.state = "meeting"
                self.progress = 0
                print("meeting")
            elif self.progress > 10:
                self.state = "left"
                self.progress = 0
                self.event.notify("remove_entity", self.id)
        elif self.state == "meeting":
            if self.progress > 10:
                self.state = "wait_manufacture"
                print("wait_manufacture")
                self.progress = 0
        elif self.state == "wait_manufacture":
            if self.building.get_room(self.y) == 3:
                self.state = "manufacture"
                print("manufacture")
                self.progress = 0
            elif self.progress > 10:
                self.state = "left"
                self.progress = 0
                self.event.notify("remove_entity", self.id)
        elif self.state == "manufacture":
            if self.progress > 10:
                self.state = "left"
                self.progress = 0
                self.event.notify("remove_entity", self.id)
                print("left")

class Scientist(Entity):
    def __init__(self, event, id, character, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 0, character, building)


class Igor(Entity):
    def __init__(self, event, id, x, floor, building):
        Entity.__init__(self, event, id, x, floor, 1, -1, building)
