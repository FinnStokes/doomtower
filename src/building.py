import event

class Building:
    def __init__(self, event_manager):
        self.event = event_manager
        self.event.push_handlers(self)
    
    def update(self, dt):
        pass # update elevator position and room actions
    
    def build_room(self, floor, room_id):
        # construct new room at floor (check that this is next above or below)
        self.model.dispatch_event('update_room', floor, room_id)
    
    def build_elevator(self, left, floors):
        # construct new elevator servicing given floors (on left if left is true, on right if false)
        # determine initial position
        self.model.dispatch_event('add_elevator', left,floors,y)
    
    def get_elevator(self, floor, left):
        pass # get the elevator at floor (on left if left is true, on right if false)

class Elevator:
    def __init__(self, floors, y):
        pass
    
    def distance_from(floor):
        pass # calculate distance from given floor
    
    def call_to(floor):
        pass # add floor to queue of passenger pickups

event.Event.register_event_type('update_room')
event.Event.register_event_type('add_elevator')
event.Event.register_event_type('remove_elevator')
event.Event.register_event_type('update_elevator')

