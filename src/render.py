import pygame, math
from pygame.locals import *
import settings

room_images = []
room_images.append(pygame.image.load('img/Floor_Lobby.png'))
room_images.append(pygame.image.load('img/Floor_Waiting.png'))
room_images.append(pygame.image.load('img/Floor_Bio.png'))
room_images.append(pygame.image.load('img/Floor_Boom.png'))
room_images.append(pygame.image.load('img/Floor_Cosmo.png'))
room_images.append(pygame.image.load('img/Floor_Psych.png'))
room_images.append(pygame.image.load('img/Floor_Info.png'))
room_images.append(pygame.image.load('img/Floor_Meeting.png'))
background_image = pygame.image.load('img/Building.png')
entity_images = []
entity_images.append(pygame.image.load('img/Scientist.png'))
entity_images.append(pygame.image.load('img/Igor.png'))
entity_images.append(pygame.image.load('img/MadScientist.png'))
entity_subimages = []
entity_subimages.append(pygame.image.load('img/Scientist-Heads.png'))
entity_subimages.append(None)
entity_subimages.append(pygame.image.load('img/MadScientist-Heads.png'))
elevator_sprite = pygame.image.load('img/Lift.png').subsurface(pygame.Rect(0,0,96,197))
elevator_pulley = pygame.image.load('img/LiftPulley.png')
elevator_rope = pygame.image.load('img/LiftRope.png')
class Render:
    def __init__(self, window, event_manager):
        self.event = event_manager
        self.event.register("update", self.update)
        self.event.register("set_scroll", self.pan_screen)
        self.event.register("step_scroll", self.step_screen)
        self.event.register("new_room", self.new_room)
        self.event.register("update_room", self.update_room)
        self.event.register("new_entity", self.new_entity)
        self.event.register("remove_entity", self.remove_entity)
        self.event.register("update_entity", self.update_entity)
        self.event.register("new_elevator", self.new_elevator)
        self.event.register("remove_elevator", self.remove_elevator)
        self.event.register("update_elevator", self.update_elevator)
        self.event.register("entity_in_elevator", self.entity_in_elevator)
        self.building_height = 0
        self.building_depth = 0
        self.window = window
        self.rooms = []
        self.elevators = dict()
        self.y_pan = 0
        self.y_target = 0
        self.pan_speed = 0
        self.room_width = 704
        self.room_height = 256
        self.room_padding = 10
        self.entities = dict()
        self.anim_timer = 0
        
    def update(self, dt):
        self.anim_timer += dt
        if(self.anim_timer > settings.ANIMATION_TIME):
            anim_step = True
            self.anim_timer -= settings.ANIMATION_TIME
        else:
            anim_step = False

        for id in self.entities:
            entity = self.entities[id]
            col = 0
            row = 0
            subrow = entity.character
            subcol = 0
            if anim_step:
                entity.anim_frame = (entity.anim_frame + 1)%entity.anim_length
            col += entity.anim_frame
            if entity.walking:
                row += 1
                entity.walking = False
            if entity.face_left:
                col += entity.anim_length
                if entity.character >= 0:
                    subcol += 1
            entity.main_rect = pygame.Rect(col*entity.width, row*entity.height, entity.width, entity.height)
            if entity.character >= 0:
                entity.sub_rect = pygame.Rect(subcol*entity.subwidth, subrow*entity.subheight, entity.subwidth, entity.subheight)
                
    def draw(self): # render current game state
        screen_width, screen_height = self.window.get_size()
        if self.pan_speed > 0:
            if self.y_target - self.y_pan < self.pan_speed:
                self.y_pan = self.y_target
                self.pan_speed = 0
            else:
                self.y_pan += self.pan_speed
        elif self.pan_speed < 0:
            if self.y_target - self.y_pan> self.pan_speed:
                self.y_pan = self.y_target
                self.pan_speed = 0
            else:
                self.y_pan += self.pan_speed
        # Draw ground and sky backgrounds
        if self.y_pan < -settings.GROUND_HEIGHT-screen_height:
            self.window.fill(settings.GROUND_COLOUR)
        else:
            self.window.fill(settings.SKY_COLOUR)
            if self.y_pan < settings.GROUND_HEIGHT:
                self.window.fill(settings.GROUND_COLOUR, pygame.Rect(0,screen_height+self.y_pan-settings.GROUND_HEIGHT,screen_width, settings.GROUND_HEIGHT-self.y_pan))
        
        x_offset = (screen_width-self.room_width)/2

        bottom_room = self.y_pan//(self.room_height+self.room_padding)
        top_room = (self.y_pan + screen_height)//(self.room_height+self.room_padding) + 1
        
        for i in range(bottom_room, top_room):
            room = self.get_room(i)
            room_id = room.id - 1
            y_offset = screen_height + self.y_pan - (self.room_height+self.room_padding)*(i+1)
            if room_id in range (0,len(room_images)):
                self.window.blit(room_images[room_id], (x_offset,y_offset))
                self.window.blit(background_image, (x_offset-40,y_offset))
            for entity in room.entities:
                if entity.sprite:
                    self.window.blit(entity.sprite,
                                     (x_offset + entity.x*(self.room_width-settings.ENTITY_WIDTH), y_offset + self.room_height - entity.height),
                                     entity.main_rect)
                if entity.subsprite:
                    self.window.blit(entity.subsprite,
                                     (x_offset + entity.x*(self.room_width-settings.ENTITY_WIDTH), y_offset + self.room_height - entity.height),
                                     entity.sub_rect)
        
        for elevator in self.elevators.itervalues():
            for entity in elevator.entities:
                if entity.sprite:
                    self.window.blit(entity.sprite,
                                     ((x_offset - (elevator.width if elevator.left else -self.room_width),
                                     screen_height + self.y_pan - (self.room_height+self.room_padding)*(elevator.y+1)+20 + (self.room_height - elevator.height))),
                                     entity.main_rect)
                if entity.subsprite:
                    self.window.blit(entity.subsprite,
                                     ((x_offset - (elevator.width if elevator.left else -self.room_width),
                                     screen_height + self.y_pan - (self.room_height+self.room_padding)*(elevator.y+1)+20 + (self.room_height - elevator.height))),
                                     entity.sub_rect)
            
            # Draws Elevator
            self.window.blit(elevator.sprite,
                             (x_offset - (elevator.width if elevator.left else -self.room_width), 
                              screen_height + self.y_pan - (self.room_height+self.room_padding)*(elevator.y+1) + (self.room_height - elevator.height)))
            liftx = x_offset -2-42
            lifty = screen_height + self.y_pan - (self.room_height+self.room_padding)*(elevator.y+1)
            # Draws Elevator Pulley
            self.window.blit(elevator.sprite_pulley, (liftx, lifty), (0, 0, 42, 40))
            # Draws Elevator Ropes
            self.window.blit(elevator.sprite_rope, (liftx+42-10, lifty+40), (0, 0, 10, 10))
            self.window.blit(elevator.sprite_rope, (liftx, lifty+40), (0, 0, 10, 10))
    
    def get_screen_pos(self, pos):
        screen_width, screen_height = self.window.get_size()
        return (screen_width-self.room_width)/2 + pos[0]*(self.room_width-settings.ENTITY_WIDTH), screen_height + self.y_pan - (self.room_height+self.room_padding)*pos[1] - self.room_padding

    def get_world_pos(self, pos):
        screen_width, screen_height = self.window.get_size()
        return (pos[0]-(screen_width-self.room_width)/2)/self.room_width, (screen_height + self.y_pan - pos[1] - self.room_padding)/(self.room_height+self.room_padding)
    
    def pan_screen(self, floor):
        if floor > self.building_height:
            target_floor = self.building_height
        elif floor < self.building_depth:
            target_floor = self.building_depth
        else:
            target_floor = floor
        screen_width, screen_height = self.window.get_size()
        floor_height = (self.room_height+self.room_padding)*(target_floor)
        if floor_height < self.y_pan:
            #scroll down
            self.y_target = floor_height - settings.BOTTOM_PANEL_HEIGHT
            self.pan_speed = (self.y_target - self.y_pan)/settings.SCROLL_TIME
            if self.pan_speed > -(self.room_height/settings.SCROLL_TIME):
                self.pan_speed = -(self.room_height/settings.SCROLL_TIME)
        elif floor_height + self.room_height > self.y_pan + screen_height:
            #scroll up
            self.y_target = floor_height + self.room_height + 2*self.room_padding - screen_height
            self.pan_speed = (self.y_target - self.y_pan)/settings.SCROLL_TIME
            if self.pan_speed < (self.room_height/settings.SCROLL_TIME):
                self.pan_speed = (self.room_height/settings.SCROLL_TIME)
        else:
            #stop scrolling
            self.y_target = self.y_pan
    def step_screen(self, up):
        screen_width, screen_height = self.window.get_size()
        if up:
            top_room = (self.y_pan + screen_height + self.room_padding + self.room_height/2)//(self.room_height+self.room_padding)
            if self.pan_speed > 0:
                self.pan_screen(top_room + 1)
            else:
                self.pan_screen(top_room)
        else:
            bottom_room = (self.y_pan - self.room_padding - self.room_height/2)//(self.room_height+self.room_padding)
            if self.pan_speed < 0:
                self.pan_screen(bottom_room - 1)
            else:
                self.pan_screen(bottom_room)
    def new_room(self):
        self.rooms.append(Room())

    def update_room(self, floor, room_id):
        if room_id !=0:
            height = floor + settings.BOTTOM_FLOOR
            if height > self.building_height:
                self.building_height = height
            elif height < self.building_depth:
                self.building_depth = height
        self.rooms[floor].update(room_id)
    
    def get_room(self, floor_number):
        return self.rooms[floor_number - settings.BOTTOM_FLOOR]
    
    def new_entity(self, id, x, y, sprite, character):
        self.entities[id] = Entity(sprite, character, x, y)
        if y in range(len(self.rooms)):
            self.get_room(y).entities.add(self.entities[id])
    
    def remove_entity(self, id): # remove entity with given id
        if id in self.entities:
            y = self.entities[id].y
            if y in range(len(self.rooms)):
                self.get_room(y).entities.remove(self.entities[id])
            del self.entities[id]
        #else:
            #raise ValueError("Invalid entity id.")
    
    def update_entity(self, id, x, y): # change entity position
        if id in self.entities:
            oldx = self.entities[id].x
            oldy = self.entities[id].y
            if oldy in range(settings.BOTTOM_FLOOR, settings.TOP_FLOOR):
                self.get_room(oldy).entities.discard(self.entities[id])
            if y in range(settings.BOTTOM_FLOOR, settings.TOP_FLOOR):
                self.get_room(y).entities.add(self.entities[id])
            if x < oldx:
                self.entities[id].face_left = True
                self.entities[id].walking = True
            elif x > oldx:
                self.entities[id].face_left = False
                self.entities[id].walking = True
            else:
                self.entities[id].walking = False
            self.entities[id].x = x
            self.entities[id].y = y
        #else:
            #raise ValueError("Invalid entity id.")
    
    def entity_in_elevator(self, entity_id, elevator_id):
        if entity_id in self.entities:
            entity = self.entities[entity_id]
            if elevator_id >= 0:
                if entity.y in range(settings.BOTTOM_FLOOR, settings.TOP_FLOOR):
                    self.get_room(entity.y).entities.discard(entity)
                if elevator_id in self.elevators:
                    self.elevators[elevator_id].entities.add(entity)
            else:
                if entity.elevator in self.elevators:
                    self.elevators[entity.elevator].entities.discard(entity)
            entity.elevator = elevator_id
        

    def new_elevator(self, id, left, floors, y): 
        # create lift servicing given floors, on the left if left is true and on the right if it is false, starting at floor y (may be non-integer)
        self.elevators[id] = Elevator(left, y)
    
    def remove_elevator(self, id):
        del self.elevators[id]
    
    def update_elevator(self, id, y):
        # move elevator to floor y (may be non-integer)
        self.elevators[id].y = y

class Room:
    def __init__(self):
        self.id = 0
        self.entities = set()
        
    def update(self, room_id):
        self.id = room_id

class Entity:
    def __init__(self, sprite_id, character_id, x_coord, y_coord):
        self.sprite = None
        self.width = 100
        self.height = 160
        self.main_rect = pygame.Rect(0,self.height,self.width, self.height)
        if character_id >= 0:
            self.subwidth = 92
            self.subheight = 86
            self.sub_rect = pygame.Rect(0,self.subheight*character_id,self.subwidth, self.subheight)
        self.character = character_id
        if sprite_id in range(len(entity_images)):
            self.sprite = entity_images[sprite_id]
            self.subsprite = entity_subimages[sprite_id]
        self.face_left = True
        self.anim_frame = 0
        self.anim_length = 2
        self.walking = False
        # The id of the current elevator the entity is in "-1 means in the building"
        self.elevator = -1
        self.x = x_coord
        self.y = y_coord

class Elevator:
    def __init__(self, left, y):
        self.left = left
        self.y = y
        self.sprite = elevator_sprite
        self.sprite_pulley = elevator_pulley
        self.sprite_rope = elevator_rope
        self.width = 100
        self.height = 197
        self.entities = set()
