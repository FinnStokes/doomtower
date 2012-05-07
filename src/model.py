import event
import entity
import building

class Model:
    def __init__(self, event_manager):
        self.building = building.Building(event_manager)

event.Event.register_event_type('add_entity')
event.Event.register_event_type('remove_entity')
event.Event.register_event_type('update_entity')
