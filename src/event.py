import pyglet

class Event(pyglet.event.EventDispatcher):
    pass

# update_room(floor, room_id)
# This event should be produced when a new room gets built, a room is destrpyed (setting id to 0)
# or a room is remodelled.
# Render should react by changing the graphic accordingly.
event.Event.register_event_type('update_room')

# new_elevator(id, left, floors, y)
# This event should be produced when a new elevator is added.
#  The integer id should be a unique identifier amongst elevators.
#  The boolean left should indicate what side of the building the elevator is on.
#  The set floors should indicate what floors the elevator services.
#  The float y should indicate what height the elevator should start at.
# Render should react by adding the relevant graphic.
event.Event.register_event_type('new_elevator')

# remove_elevator(id)
# This event should be produced when an elevator is removed.
# Render should react by deleting the relevant graphic.
event.Event.register_event_type('remove_elevator')

# update_elevator(id, y)
# This event should be produced when an elevator changes position.
# Render should react by changing the elevator graphic to reflect this.
event.Event.register_event_type('update_elevator')

# new_entity(id, x, y)
# This event should be produced when a new entity enters the building.
#  The integer id should be a unique identifier amongst entities.
#  The float x should indicate how far across the building the entity is (0 = left wall, 1 = right wall).
#  The integer y should indicate what floor the entity is on.
# Render should react by adding the relevant graphic.
event.Event.register_event_type('new_entity')

# remove_entity(id)
# This event should be produced when an entity is removed.
# Render should react by deleting the relevant graphic.
event.Event.register_event_type('remove_entity')

# update_entity(id, x, y)
# This event should be produced when an entity changes position.
#  The integer id should be the unique identifier amongst entities.
#  The float x should indicate how far across the building the entity is (0 = left wall, 1 = right wall).
#  The integer y should indicate what floor the entity is on.
# Render should react by moving the entity graphic.
event.Event.register_event_type('update_entity')
