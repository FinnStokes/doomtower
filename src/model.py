import event
import entity
import building

class Model:
    def __init__(self, event_manager):
        self.building = building.Building(event_manager)
        self.entities = entity.Manager(event_manager)
