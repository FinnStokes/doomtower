Game Sprites Spec Sheet
-----------------------


Building
--------

Position: 187, 0
Dimensions: 760, 600

Floor
-----

Position: Relative
Dimensions: 704, 256
Spacing: 10

Entities
--------

Position: X Variable, (Floor.Y + 80 || Lift.Y + 28)
Frame Dimensions: 100, 160

### Sprite Sheet

Y Index, Name

0: Standing
1: Walking

Lifts
-----

Lift Position: X (left) 120 || (right) 920, Y 
Pulley Position: Lift.X + 26, FloorA.Y
Rope1 Position: Lift.X + 26, FloorA.Y + 20
Rope2 Position: Lift.X + 58, FloorA.Y + 20

Lift Dimensions: 96, 197
Pulley Frame: 42, 40
Rope Frame: 10, Variable based on FloorA/FloorB distance

Lift Door
---------

LiftDoor Position: Lift.X, Lift.Y
LiftDoor Frame: 96, 197

### Sprite Sheet

Y Index, Name

0: Lift
1: DoorOpening