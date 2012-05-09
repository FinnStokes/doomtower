import os, sys, event, settings
#encapsulates all building data in the current game
class Building:
    floor_height = 10

    def __init__(self, event_manager):
        numfloors = settings.TOP_FLOOR - settings.BOTTOM_FLOOR +1
  
        self.event = event_manager
        self.event.register("input_build", self.build_room)
        self.event.register("input_elevator", self.build_elevator)
        self.event.register("update", self.update)
        self.player_funds = settings.STARTING_FUNDS
        self.floors = []
        self.lifts = []

        # fill building with empty floors
        for i in range(numfloors):
            self.floors.append(Room()) 
            self.event.notify("add_room")
        # add lobby at ground floor
        self.build_room(0,1)

        # add test floors
        self.build_room(1,2)
        self.build_room(-1,3)
        self.build_room(2,4)
        self.build_room(3,3)
    def update(self, dt):      
    #   Elevators
        for i in range(len(self.lifts)):
            self.lifts[i].move()
    #   Rooms
        for i in range(len(self.floors)):
            self.floors[i].operate()

        pass # update elevator position and room actions
    
    def build_room(self, floor, room_id):
        # construct new room at floor (check that this is next above or below)
        floor_index = floor-settings.BOTTOM_FLOOR
        self.event.notify('update_room', floor_index, room_id)
        self.floors[floor_index] = Room(room_id)

    def build_elevator(self, left, floors):
        # construct new elevator servicing given floors (on left if left is true, on right if false)
        # determine initial position (initialised to minimum floor)          
        self.lifts[int(not left)].append( Elevator(floors, min(floors) * floor_height))
        self.event.notify('new_elevator', left, floors)
     
    #gets elevator at given floor on given side of building       
    def get_elevator(self, floor, left): 
        
        for i in range(len(self.lifts[int(not left)])):               
            if floor == self.lifts[int(not left)][i].curr_floor:
                return self.lifts[int(not left)]
  
        return None  # get the elevator at floor (on left if left is true, on right if false)

    def service(self):
        pass

    def save_game(self):
        pass


class Elevator:
    lift_speed = 2

    #elevator will service a list of arbitrary floors and be initially positioned at the lowest
    def __init__(self, floors, y):
        self.floors = floors
        self.curr_floor = min(floors)
        self.y = y
        self.capacity = 1
        self.occupants = 0
        self.pickups = []
     #   self.ascending = True
        self.moving = False

    # calculate distance from given floor
    def distance_from(self, floor):
        return self.curr_floor - floor
    
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
 
        dest = self.pickups[0]

        if self.curr_floor != dest:
            distance = distance_from(self, dest)
            self.y = self.y + Elevator.lift_speed * dt * (distance / abs(distance))
            self.curr_floor = int( float(self.y) / float(Building.floor_height))
            pass
        else:
            self.pickups.pop(0)
            open_doors(self)

    # when elevator reaches a requested floor it must stop and allow ingress/egress
    def open_doors(self):
        self.moving = False
        self.event.notify("elevator_open", self.curr_floor)
    

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
                'bio': [10000, 1000, 2000, 200 ], 
                'psycho': [5000, 500, 1000, 2500], 
                'info': [1000, 100, 500, 500], 
                'cosmic': [10000, 2000, 2500, 8000]
    }
    #define some lab attributes as defined in design doc
    #each entry includes: key(room_id) = buy_cost, upkeep, decomm_cost
    miscroomtypes = {'reception': [10000, 1000, 2000],
                     'meeting': [10000, 1000, 2000]
    }       

    def __init__(self, room_id = 'empty', size = 1):
        self.room_id = room_id
        self.size = size
        self.jobs = []

    def operate(self):
        pass

    def produce(self, products):
        pass
