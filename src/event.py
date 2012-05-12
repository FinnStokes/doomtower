class Event():
    def __init__(self):
        self.handlers = dict()

    def register(self, event, handler):
        if not event in self.handlers:
            self.handlers[event] = set()
        self.handlers[event].add(handler)
        return self

    def deregister(self, event, handler):
        if event in self.handlers:
            try:
                self.handlers.remove(handler)
            except:
                raise ValueError("Handler is not handling this event, so cannot deregister it.")
        else:
            raise ValueError("Event is not registered, so cannot deregister it.")
        return self

    def notify(self, event, *args, **kargs):
        if event in self.handlers:
            for handler in self.handlers[event]:
                handler(*args, **kargs)


# update(dt)
# This event should be produced periodically with dt set to the time in seconds since it was last produced.

# key_down(key)
# This event should be produced whenever a key is pressed, where key is the key id (use pygame.locals to interpret)

# create_client()
# This event should be produced when a new client should enter the building at the spawn location.
# Entity should respond by creating a new Client

# create_scientist()
# This event should be produced when a new scientist should enter the building at the spawn location (i.e. is hired).
# Entity should respond by creating a new Scientist

# create_igor()
# This event should be produced when a new igor should enter the building at the spawn location (i.e. is hired).
# Entity should respond by creating a new Igor

# input_move(entity, floor)
# This event should be produced when the player commands an entity to go to a new floor.
# Entity should respond by starting the referenced entity moving towards the given floor

# update_room(floor, room_id)
# This event should be produced when a new room gets built, a room is destrpyed (setting id to 0)
# or a room is remodelled.
# Render should react by changing the graphic accordingly.

# new_elevator(id, left, floors, y)
# This event should be produced when a new elevator is added.
#  The integer id should be a unique identifier amongst elevators.
#  The boolean left should indicate what side of the building the elevator is on.
#  The set floors should indicate what floors the elevator services.
#  The float y should indicate what height the elevator should start at.
# Render should react by adding the relevant graphic.

# remove_elevator(id)
# This event should be produced when an elevator is removed.
# Render should react by deleting the relevant graphic.

# update_elevator(id, y)
# This event should be produced when an elevator changes position.
# Render should react by changing the elevator graphic to reflect this.

# new_entity(id, x, y, sprite, character)
# This event should be produced when a new entity enters the building.
#  The integer id should be a unique identifier amongst entities.
#  The float x should indicate how far across the building the entity is (0 = left wall, 1 = right wall).
#  The integer y should indicate what floor the entity is on.
# Render should react by adding the relevant graphic.

# remove_entity(id)
# This event should be produced when an entity is removed.
# Render should react by deleting the relevant graphic.

# update_entity(id, x, y)
# This event should be produced when an entity changes position.
#  The integer id should be the unique identifier amongst entities.
#  The float x should indicate how far across the building the entity is (0 = left wall, 1 = right wall).
#  The integer y should indicate what floor the entity is on.
# Render should react by moving the entity graphic.

# entity_in_elevator(entity_id, elevator_id)
# This event should be produced when an entity moves into or back from an elevator.
#  The integer entity_id should be the unique identifier amongst entities.
#  The integer elevator_id should be the unique identifier amongst elevators if the entity is moving into an elvator
#   or -1 if the entity is moving out.
