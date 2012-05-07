import pyglet

import entity
import building

class Model(pyglet.event.EventDispatcher):
    def __init__(self, controller):
        self.controller = controller
        self.building = building.Building(model)
        self.controller.push_handlers(building)

Model.register_event_type('update_room')
Model.register_event_type('add_entity')
Model.register_event_type('remove_entity')
Model.register_event_type('update_entity')
Model.register_event_type('add_elevator')
Model.register_event_type('remove_elevator')
Model.register_event_type('update_elevator')
