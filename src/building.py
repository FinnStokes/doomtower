import os, sys, event
class Building:
        
    floor_height = 10

    def __init__(self, event_manager, numfloors = 6):
        
        self.event = event_manager
        self.event.register("input_build", self.build_room)
        self.event.register("input_elevator", self.build_elevator)
        self.floors = []
        self.lifts = []
        #fill building with empty floors
        for i in range(numfloors):
            self.floors.append(Room()) 
            self.model.dispatch_event('floor_init', i)
    
    def update(self, dt):      
        pass # update elevator position and room actions
    
    def build_room(self, floor, room_id):
        # construct new room at floor (check that this is next above or below)
        self.event.notify('update_room', floor, room_id)
        self.floors[floor] = Room(room_id)
    
    def build_elevator(self, left, floors):
        # construct new elevator servicing given floors (on left if left is true, on right if false)
        # determine initial position (initialised to minimum floor)          
        self.lifts[int(not left)] = Elevator(floors, min(floors) * floor_height)
        self.event.notify('new_elevator', left, floors)
           
    
    def get_elevator(self, floor, left):
        if self.lifts[int(not left)].curr_floor == floor:
            return self.lifts[int(not left)]
        else: 
            return None  # get the elevator at floor (on left if left is true, on right if false)

class Elevator:

    lift_speed = 2

    def __init__(self, floors, y):
        self.floors = floors
        self.curr_floor = min(floors)
        self.y = y
        self.capacity = 1
        self.occupants = 0
       
    # calculate distance from given floor
    def distance_from(self, floor):
        return self.curr_floor - floor

    def call_to(self, floor):
        if floor in self.floors:
            move(self, floor)
        else:  
            pass # add floor to queue of passenger pickups

    def move(self, dest):
        pass   



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
     
    miscroomtypes = {'reception': [10000],
                     'meeting': [10000]
    }
       

    def __init__(self, room_id = 'empty'):
        self.room_id = room_id
        self.jobs = []
    
