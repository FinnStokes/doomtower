import pyglet

import event
import model
import view

event_manager = event.Event()
game_model = model.Model(event_manager)
player_view = view.View(event_manager)

pyglet.app.run()
