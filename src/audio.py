# audio.py - manipulates pyglet.media.Player according to game events

import os, sys, pygame, event

class DoomMixer:
# manages playback of streaming audio files (music) and static audio files (sound effects)

# audio source files
#should be separated by event type
    clientsources = [['snd/clientgreeting1.ogg', 'snd/clientfarewell1.ogg'],
                     ['snd/clientgreeting2.ogg', 'snd/clientfarewell2.ogg'],
                     ['snd/browngreeting.ogg', 'snd/brownfarewell.ogg'],
                     ['snd/dextergreeting.ogg', 'snd/dexterfarewell.ogg'],
                     ['snd/elfmangreeting.ogg', 'snd/elfmanfarewell.ogg'],
                     ['snd/farnsworthgreeting.ogg', 'snd/farnsworthfarewell.ogg'],
                     ['snd/frankensteingreeting.ogg', 'snd/frankensteinfarewell.ogg'],
                     ['snd/franknfurtergreeting.ogg', 'snd/franknfurterfarewell.ogg']
                  
    ]

    scientistsources = [['snd/clientgreeting1.ogg', 'snd/clientfarewell1.ogg'],
                        ['snd/clientgreeting2.ogg', 'snd/clientfarewell2.ogg'],
                        ['snd/curiegreeting.ogg', 'snd/curiefarewell.ogg'],
                        ['snd/edisongreeting.ogg', 'snd/edisonfarewell.ogg'],
                        ['snd/einsteingreeting.ogg', 'snd/einsteinfarewell.ogg'],
                        ['snd/newtongreeting.ogg', 'snd/newtonfarewell.ogg'],
                        ['snd/planckgreeting.ogg', 'snd/planckfarewell.ogg'],
                        ['snd/rutherfordgreeting.ogg', 'snd/rutherfordfarewell.ogg'],
                        ['snd/teslagreeting.ogg', 'snd/teslafarewell.ogg'],
                        ['snd/thomsongreeting.ogg', 'snd/thomsonfarewell.ogg']
    ]

    igorsources = ['snd/igoryeth.ogg', 'snd/igordirection.ogg']
    roomsource = ['snd/bio.ogg', 'snd/boom.ogg', 'snd/cosmic.ogg', 'snd/informatics', 'snd/meeting.ogg', 'snd/psycho.ogg', 'snd/reception.ogg']
    bgmsources = ['snd/sciencegroove.ogg', 'snd/sciencegroove2.ogg']
  
    def __init__(self, event_manager):
        self.event = event_manager
        #unique room sound should play when a room is built
        self.event.register("input_build", self.play_room) 
 
        self.clientvox = []
        self.sciencevox = []

        self.bgm = []
        #load sounds

        for i in range(len(clientsources)):
            arr = []
            for j in range(len(clientsources[i])):
                arr.append(pygame.mixer.Sound(clientsources[i][j]))
            self.clientvox.append(arr)
                    
        for i in range(len(scientistsources)):
            arr = []
            for j in range(len(scientistsources[i])):
                arr.append(pygame.mixer.Sound(scientistsources[i][j]))
            self.sciencevox.append(arr)
                    
        for i in range(len(roomsources)):
            self.room_snd.append(pygame.mixer.Sound(roomsources[i]))
           
        for i in range(len(bgmsources)):
            self.bgm.append(pygame.mixer.Sound(bgmsources[i]))   
        
        pygame.mixer.init()
        pygame.mixer.music.queue(self.bgm[0])   
  
    def play_room(self, floor, room_id):
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

