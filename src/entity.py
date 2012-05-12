import settings, random, path, math
client_patience = []
client_requests = []

#Set the patience and potential requests for each client
for i in range(10):
    client_patience.append(30)
    client_requests.append({settings.ROOM_BOOM:0.5, settings.ROOM_BIO:0.5, settings.ROOM_COSMO:0, settings.ROOM_PSYCH:0, settings.ROOM_INFO: 0})
class Manager:
    def __init__(self, event, building):
        self.event = event
        self.building = building
        self.nextId = 0
        self.entities = dict()
        event.register("create_client", self.create_client)
        event.register("create_scientist", self.create_scientist)
        event.register("create_igor", self.create_igor)

    def create_client(self):
        self.entities[self.nextId] = Client(self.event, self.nextId, random.randint(0,9), settings.SPAWN_POSITION, settings.SPAWN_FLOOR, self.building, self)
        self.nextId = self.nextId + 1
    
    def create_scientist(self, character):
        wage = settings.SCIENTIST_COSTS[character]
        if self.building.get_funds() >= wage:
            self.building.spend_funds(wage)
            e = Scientist(self.event, self.nextId, character, settings.SPAWN_POSITION, settings.SPAWN_FLOOR, self.building, wage)
            self.nextId = self.nextId + 1
    
    def create_igor(self):
        wage = settings.IGOR_COST
        if self.building.get_funds() >= wage:
            self.building.spend_funds(wage)
            e = Igor(self.event, self.nextId, settings.SPAWN_POSITION, settings.SPAWN_FLOOR, self.building, wage)
            self.nextId = self.nextId + 1
        
    def entity_count(self, room, type):
        count = 0
        for entity in self.entities:
            if self.entities[entity].type == type:
                if self.entities[entity].y == room:
                    count += 1
        return count
        
class Entity:
    def __init__(self, event, id, x, floor, type, character, building, wage):
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
        self.wage = wage
        self.wage_timer = 0
        self.type = type
        self.event.register("input_move", self.move_to)
        self.event.register("update", self.update)
        self.event.notify("new_entity", self.id, self.x, self.y, type, character)
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
        # wages
        self.wage_timer += dt
        if self.wage > 0 and self.wage_timer > settings.WAGE_PERIOD:
            self.building.spend_funds(self.wage)
            self.wage_timer -= settings.WAGE_PERIOD
        
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
    def __init__(self, event, id, character, x, floor, building, manager):
        Entity.__init__(self, event, id, x, floor, 2, character, building, 0)
        self.state = "wait_meeting"
        self.progress = 0
        self.event = event
        self.character = character
        self.request = -1
        self.manager = manager
        self.previous_job = "wait_meeting"
        rand = random.random()
        for room, chance in client_requests[character].items():
            if rand < chance:
                self.request = room
                break
            else:
                rand -= chance
    
    def update(self, dt):
        Entity.update(self, dt)
        self.progress += dt
        if self.state == "wait_meeting":
            # If the client has not yet had a meeting
            if self.building.get_room(self.y) == settings.ROOM_MEETING:
                # If the client is in the meeting room
                if self.manager.entity_count(self.y, settings.ENTITY_SCIENTIST) > 0:
                    # If the scientist is in the meeting room, start the meeting
                    self.set_state("meeting")
                else:
                    # If there is no scientist, wait for a scientist
                    self.previous_job = "meeting"
                    self.set_state("wait_scientist")
                    
            elif self.progress > client_patience[self.character]:
                # If the client is not in the waiting room, leave after patience has elapsed
                self.set_state("leaving")
                self.event.notify("input_move", self.id, 0)
                
              
        elif self.state == "meeting":
            # During a meeting
            if self.building.get_room(self.y) != settings.ROOM_MEETING:
                # If the client leaves the room, reset to waiting for a meeting
                self.set_state("wait_meeting")
            elif self.manager.entity_count(self.y, settings.ENTITY_SCIENTIST) == 0:
                # If the scientist leaves the room, await his return
                self.previous_job = "meeting"
                self.set_state("wait_scientist")
            elif self.progress > settings.MEETING_TIME:
                # If the meeting concludes, proceed to await manufacture
                self.set_state("wait_manufacture")
                self.event.notify("set_entity_request", self.id, self.request)
                
                
        elif self.state == "wait_manufacture":
            # While waiting for manufacture
            if self.building.get_room(self.y) == self.request:
                #If the client is in the correct room
                if self.manager.entity_count(self.y, settings.ENTITY_SCIENTIST) > 0:
                    # If there is a scientist in the room, commence manufacture
                    self.set_state("manufacture")
                else:
                    # Otherwise wait for a scientist
                    self.previous_job = "manufacture"
                    self.set_state("wait_scientist")
            elif self.progress > client_patience[self.character]:
                # Otherwise, leave once patience has elapsed
                self.set_state("leaving")
                self.event.notify("input_move", self.id, 0)
                
                
        elif self.state == "manufacture":
            # During manufacture
            if self.building.get_room(self.y) != self.request:
                # If the client leaves the room, reset to waiting for manufacture
                self.set_state("wait_manufacture")
                self.event.notify("set_entity_request", self.id, self.request)
            elif self.manager.entity_count(self.y, settings.ENTITY_SCIENTIST) == 0:
                # If the scientist leaves the room, await his return
                self.previous_job = "manufacture"
                self.set_state("wait_scientist")
            elif self.progress > settings.MANUFACTURE_TIME:
                # If the manufacture concludes, client satisfied
                self.set_state("satisfied")
                self.event.notify("input_move", self.id, 0)
                
                
        elif self.state == "wait_scientist":
            if self.manager.entity_count(self.y, settings.ENTITY_SCIENTIST) > 0:
                # If the scientist returns, restart procedure
                self.set_state(self.previous_job)
            elif self.progress > client_patience[self.character]:
                # Otherwise, leave once patience has elapsed
                self.set_state("leaving")
                self.event.notify("input_move", self.id, 0)
            
            
        elif self.state in ("leaving", "satisfied"):
            # If client leaving for any reason
            if self.y == 0 and math.fabs(self.x - 0.5) < 0.01:
                # If client at exit, leave building
                self.set_state("left")
                self.event.notify("remove_entity", self.id)

    def set_state(self, state):
        self.state = state
        self.event.notify("set_entity_state", self.id, state)
        self.progress = 0

class Scientist(Entity):
    def __init__(self, event, id, character, x, floor, building, wage):
        Entity.__init__(self, event, id, x, floor, 0, character, building, wage)


class Igor(Entity):
    def __init__(self, event, id, x, floor, building, wage):
        Entity.__init__(self, event, id, x, floor, 1, -1, building, wage)
