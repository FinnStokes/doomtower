class Building:
    def __init__(self, event):
        self.event = event
        event.register("input build", buildRoom)
        event.register("input elevator", buildElevator)
    
    def update(self, dt):
        pass # update elevator position and room actions
    
    def buildRoom(self, floor, room_id):
        # construct new room at floor (check that this is next above or below)
        self.event.notify("update room", floor, room_id)
    
    def buildElevator(self, left, floors):
        # construct new elevator servicing given floors (on left if left is true, on right if false)
        # determine initial position
        self.event.notify(left,floors,y)
    
    def getElevator(self, floor, left):
        pass # get the elevator at floor (on left if left is true, on right if false)

class Elevator:
    def __init__(self, floors, y):
        pass
    
    def distanceFrom(floor):
        pass # calculate distance from given floor
    
    def callTo(floor):
        pass # add floor to queue of passenger pickups
