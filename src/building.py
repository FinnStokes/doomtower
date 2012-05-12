import os, sys, event, path, settings
#encapsulates all building data in the current game
class Building:
    #floor_height = 10

    def __init__(self, event_manager):
        numfloors = settings.TOP_FLOOR - settings.BOTTOM_FLOOR +1
  
        self.event = event_manager
        self.event.register("input_build", self.build_room)
        self.event.register("input_elevator", self.build_elevator)
        self.event.register("update", self.update)
        self.player_funds = settings.STARTING_FUNDS
        self.floors = []
        self.lifts = [],[]
        self.nextElevator = 0
        #Graph with elevator doors as nodes and paths between as edges
        #indexed left-right, bottom-top
        self.building_graph = path.Graph()
 
        for i in range(settings.BOTTOM_FLOOR, settings.TOP_FLOOR):
            self.building_graph.addNode(i*2)
            self.building_graph.addNode(i*2 + 1)

        #add initial edges
        for i in range(settings.BOTTOM_FLOOR, settings.TOP_FLOOR):
            self.building_graph.addEdge(i*2,     i*2 + 1, 1)
            self.building_graph.addEdge(i*2 + 1, i*2,     1)

        # fill building with empty floors
        for i in range(numfloors):
            self.floors.append(Room()) 
            self.event.notify("new_room")


        # add lobby at ground floor
        self.build_room(0,1)

        # add test floors
        self.build_room(1,2)
        self.build_room(-1,3)
        self.build_room(2,4)
        self.build_room(3,3)
    def update(self, dt):      
    #   Elevators
        for i in range(len(self.lifts[0])):
            self.lifts[0][i].move(dt)
        for i in range(len(self.lifts[1])):
            self.lifts[1][i].move(dt)
    #   Rooms
        for i in range(len(self.floors)):
            self.floors[i].operate(dt)

        pass # update elevator position and room actions
    
    def build_room(self, floor, room_id):
        # construct new room at floor (check that this is next above or below)
        floor_index = floor-settings.BOTTOM_FLOOR
        self.event.notify('update_room', floor_index, room_id)
        self.floors[floor_index] = Room(room_id)

    def build_elevator(self, left, floors):
        side = int(not left)
        doors = []        

        # construct new elevator servicing given floors (on left if left is true, on right if false)
        # determine initial position (initialised to minimum floor)          
        elevator = Elevator(self.nextElevator, floors, min(floors), self.event)
        self.nextElevator = self.nextElevator + 1
        self.lifts[side].append( elevator )# * floor_height))
        self.event.notify('new_elevator', elevator.id, left, floors, elevator.y)
        
        #add edges provided by elevator to building_graph
        for i in range(len(floors)-1):
            self.building_graph.addEdge(floors[i]*2 + side,   floors[i+1]*2 + side, abs(floors[i] - floors[i+1])+0.1)
            self.building_graph.addEdge(floors[i+1]*2 + side, floors[i]*2 + side,   abs(floors[i] - floors[i+1])+0.1)
                 

    def remove_elevator(self, left, index):
        pass


    #gets elevator servicing given floor on given side of building       
    def get_elevator(self, floor, left): 
        side = int(not left)
        for i in range(len(self.lifts[side])):               
            if floor in self.lifts[side][i].floors:
                return self.lifts[side][i]
  
        return None  # get the elevator at floor (on left if left is true, on right if false)

    def service(self):
        pass

    def save_game(self):
        pass


class Elevator:
    lift_speed = 0.5

    #elevator will service a list of arbitrary floors and be initially positioned at the lowest
    def __init__(self, id, floors, y, event_manager):
        self.floors = floors
        self.id = id
        self.y = y
        self.event = event_manager
        self.capacity = 1
        self.occupants = 0
        self.pickups = []
     #   self.ascending = True
        self.moving = False
        self.occupied = False
        self.target = 0

    # calculate distance from given floor
    def distance_from(self, floor):
        return self.y - floor
    
    # add floor to queue of passenger pickups
    def call_to(self, floor):
        if not self.moving:
            self.moving = True

        if floor in self.floors:
            self.pickups.append(floor)
        else:  
            pass 

    # move to next floor in pickup queue  
    def move(self, dt):
        if not self.moving:
            return None
 
        if self.occupied:
            dest = self.target
        else:
            dest = self.pickups[0]
        
        deltay = Elevator.lift_speed * dt
        if deltay <= abs(dest - self.y):
            distance = self.distance_from(dest)
            self.y = self.y - deltay * (distance / abs(distance))
        else:
            if not self.occupied:
                self.pickups.pop(0)
            self.y = dest
            self.open_doors()
        self.event.notify("update_elevator", self.id, self.y)

    # when elevator reaches a requested floor it must stop and allow ingress/egress
    def open_doors(self):
        self.moving = False
        self.event.notify("elevator_open", self.id, self.y)
    
    def occupy(self, target):
        if not self.occupied:
            self.occupied = True
            self.target = target
            self.moving = True
            return True
        else:
            return False
    
    def exit(self):
        if self.occupied:
            self.occupied = False
            if len(self.pickups) > 0:
                self.moving = True

class Room:
    #product types
    products = {'time_bomb': 'boom',
                'gravity_bomb': 'boom',
                'culture_bomb': 'boom',
                'super_virus': 'bio',
                'hybrid': 'bio',
                're-animator': 'bio',
                'shapeshifter': 'bio',
                'mind_ray': 'psycho',
                'mind_drugs': 'psycho',
                'jacker': 'info',
    }
    #define some lab attributes as defined in design doc
    #each entry includes: key(room_id) = buy_cost, upkeep, decomm_cost, income
    labtypes = {'boom': [5000, 500, 1000, 1000], 
                'bio': [10000, 1000, 3000, 200 ], 
                'psycho': [5000, 500, 1000, 2500], 
                'info': [1000, 100, 300, 500], 
                'cosmic': [10000, 2000, 3000, 8000]
    }
    #define some lab attributes as defined in design doc
    #each entry includes: key(room_id) = buy_cost, upkeep, decomm_cost
    miscroomtypes = {'reception': [1000, 100, 300],
                     'meeting': [1000, 100, 300]
    }       

    def __init__(self, room_id = 'empty', size = 1):
        self.room_id = room_id
        self.size = size
        self.jobs = []

    def operate(self, dt):
        pass

    def produce(self, product):
        if products[product] == self.room_id:
            self.jobs.append(product)
