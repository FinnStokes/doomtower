class Entity:
    def __init__(self, event):
        id = 0 # give them unique ids or pass into constructor
        event.register("input_move", moveTo)
    
    def moveTo(self, entity, floor):
        if entity == self.id:
            pass # move
