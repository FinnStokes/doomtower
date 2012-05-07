import pyglet

import model
import view

game_model = model.Model()
player_view = view.View(game_model)

pyglet.app.run()
