class Render:
    def __init__(self, event):
        event.register("update room", self.updateRoom)
        event.register("add entity", self.addEntity)
        event.register("remove entity", self.removeEntity)
        event.register("update entity", self.updateEntity)
        event.register("add elevator", self.addElevator)
        event.register("remove elevator", self.removeElevator)
        event.register("update elevator", self.updateElevator)
    
    def render():
        pass # render current game state
    
    def updateRoom(floor, room_id):
        pass # change room graphic
    
    def addEntity(id, x, y sprite):
        pass # create entity with given sprite at given position
    
    def removeEntity(id):
        pass
    
    def updateEntity(id, x, y):
        pass # change entity position
    
    def addElevator(id, left, floors, y):
        pass # create lift servicing given floors, on the left if left is true and on the right if it is false, starting at floor y (may be non-integer)
    
    def removeElevator(id):
        pass
    
    def updateElevator(id, y):
        pass # move elevator to floor y (may be non-integer)
    
