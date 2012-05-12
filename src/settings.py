TOP_FLOOR = 10
BOTTOM_FLOOR = -5

ROOM_WIDTH = 706
ROOM_HEIGHT = 256

# Funds
STARTING_FUNDS = 12000

# Costs
ROOM_COSTS = [ 0,
    0, # LOBBY
    5000, # WAITING
    10000, # BIO
    5000, # BOOM
    10000, # COSMO
    5000, # PSYCH
    1000, # INFO
    5000, # MEETING
]
SCIENTIST_COSTS = [
    500, # Korsakov
    500, # Mayamoto
    500, # Rutherford
    500, # Edison
    500, # Thomson
    500, # Planck
    500, # Curie
    500, # Tesla
    500, # Einstein
    500, # Newton
]
IGOR_COST = 200

# Pays
ROOM_PAYS = [ 0,
    0, # LOBBY
    0, # WAITING
    2000, # BIO
    1000, # BOOM
    8000, # COSMO
    2500, # PSYCH
    500, # INFO
    0, # MEETING
]
ROOM_UPKEEP = [ 0,
    0, # LOBBY
    0, # WAITING
    1000, # BIO
    500, # BOOM
    2000, # COSMO
    500, # PSYCH
    100, # INFO
    0, # MEETING
]

# Period of staff wages (secs)
WAGE_PERIOD = 30

# Period of room upkeep costs (secs)
UPKEEP_PERIOD = 60

# The number of seconds spent on each frame of the animation
ANIMATION_TIME = 0.2

# The number of frames taken to scroll to a given floor
SCROLL_TIME = 20

# The x position and floor new entities should spawn at
SPAWN_POSITION = 0.5
SPAWN_FLOOR = 0

# Period of client spawning (secs)
SPAWN_PERIOD = 10


# The horizontal speed the entities should move at in rooms per second
ENTITY_SPEED = 0.2

# The size of the bounding rectangle for each entity
ENTITY_WIDTH = 100
ENTITY_HEIGHT = 160

# The height of the drag bar for pop-up windows in pixels
DRAGBAR_HEIGHT = 75

# The bottom panel
BOTTOM_PANEL_HEIGHT = 64
BOTTOM_PANEL_COLOUR = (217,41,56)

# Details of the background 
SKY_COLOUR = (196,207,255)
GROUND_COLOUR = (115,57,0)
GROUND_HEIGHT = 96

# Time taken for stages of process
MEETING_TIME = 10
MANUFACTURE_TIME = 5

# Room IDs
ROOM_EMPTY = 0
ROOM_LOBBY = 1
ROOM_WAITING = 2
ROOM_BIO = 3
ROOM_BOOM = 4
ROOM_COSMO = 5
ROOM_PSYCH = 6
ROOM_INFO = 7
ROOM_MEETING = 8

# Entity IDs
ENTITY_SCIENTIST = 0
ENTITY_IGOR = 1
ENTITY_CLIENT = 2
