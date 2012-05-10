# audio.py - manipulates pyglet.media.Player according to game events

import os, sys, pygame, event

class DoomMixer:
# manages playback of streaming audio files (music) and static audio files (sound effects)

# audio source files
#should be separated by event type
#    entitysources = [['../snd/clientgreeting1.ogg', '../snd/clientfarewell1.ogg'],
#                     ['../snd/clientgreeting2.ogg', '../snd/clientfarewell2.ogg']  ]
    roomsource = ['../snd/bio.ogg', '../snd/boom.ogg', '../snd/cosmic.ogg', '../snd/informatics', '../snd/meeting.ogg', '../snd/psycho.ogg', '../snd/reception.ogg']
    bgmsources = ['../snd/sciencegroove.ogg']
#    inputsources = []


#    sfxsources = []
#    voicesources = []
#  
    def __init__(self, event_manager):
        self.event = event_manager
        #unique room sound should play when a room is built
        self.event.register("input_build", self.play_room) 
        self.entitysnd = []
        self.voice = {}
        self.room_snd = []
        self.bgm = []
        
 #       for path in entitysources:
 #           pass
        
        for i in range(len(roomsources)):
            self.room_snd.append(pygame.mixer.Sound(roomsources[i]))
 #       for name in voicesources:
  #          pass
            
   #     for name in bgmsources:
    #        pass

        pygame.mixer.init()
    
  
    def play_room(self, room_id):
        self.room_snd[room_id].play()
    
    # generic audio call
    def make_noise(self):
        pass


    # play new background music, current track faded out or cut
    def playbgm(self, title, sharp = True):
        bgm = self.sfx[title]
    
        if sharp == true:
            pygame.mixer.music.queue(bgm)
            pygame.mixer.music.stop()       
        else:
            pygame.mixer.music.queue(bgm)
            pygame.mixer.music.fadeout()  

