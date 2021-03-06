# audio.py - manipulates pyglet.media.Player according to game events

import os, sys, pygame, event

import settings

class DoomMixer:
# manages playback of streaming audio files (music) and static audio files (sound effects)

# audio source files
#should be separated by event type
    


    vox = [[            ['snd/clientgreeting1.ogg', 'snd/clientfarewell1.ogg'],
                        ['snd/clientgreeting2.ogg', 'snd/clientfarewell2.ogg'],
                        ['snd/rutherfordgreeting.ogg', 'snd/rutherfordfarewell.ogg'],
                        ['snd/edisongreeting.ogg', 'snd/edisonfarewell.ogg'],
                        ['snd/thomsongreeting.ogg', 'snd/thomsonfarewell.ogg'],
                        ['snd/planckgreeting.ogg', 'snd/planckfarewell.ogg'],
                        ['snd/curiegreeting.ogg', 'snd/curiefarewell.ogg'],
                        ['snd/teslagreeting.ogg', 'snd/teslafarewell.ogg'],
                        ['snd/einsteingreeting.ogg', 'snd/einsteinfarewell.ogg'],
                        ['snd/newtongreeting.ogg', 'snd/newtonfarewell.ogg']],
                       [['snd/igoryeth.ogg', 'snd/igordirection.ogg']],
                       [['snd/farnsworthgreeting.ogg', 'snd/farnsworthfarewell.ogg'],
                        ['snd/dextergreeting.ogg', 'snd/dexterfarewell.ogg'],
                        ['snd/browngreeting.ogg', 'snd/brownfarewell.ogg'],   
                        ['snd/evilgreeting.ogg', 'snd/evilfarewell.ogg'],
                        ['snd/rustygreeting.ogg', 'snd/rustyfarewell.ogg'],
                        ['snd/jonasgreeting.ogg', 'snd/jonasfarewell.ogg'],
                        ['snd/elfmangreeting.ogg', 'snd/elfmanfarewell.ogg'],
                        ['snd/frankensteingreeting.ogg', 'snd/frankensteinfarewell.ogg'],
                        ['snd/franknfurtergreeting.ogg', 'snd/franknfurterfarewell.ogg'],  
                        ['snd/nogreeting.ogg', 'snd/nofarewell.ogg']]                     
          ]    
    
    roomsources = ['snd/meeting.ogg', 'snd/reception.ogg', 'snd/bio.ogg', 'snd/boom.ogg', 'snd/cosmic.ogg', 'snd/psycho.ogg', 'snd/informatics.ogg', 'snd/meeting.ogg']
    bgmsources = ['snd/sciencegroove.ogg', 'snd/sciencegroove2.ogg']
    sfxsources = ['snd/gain_funds.ogg', 'snd/spend_funds.ogg', 'snd/deny.ogg']
    
    def __init__(self, event_manager):
        self.event = event_manager
        #unique room sound should play when a room is built
        self.event.register("update_room", self.play_room) 
        self.event.register("new_entity", self.entity_hello )
        self.event.register("remove_entity", self.entity_bye )
        self.event.register("update_funds", self.funds )
        self.event.register("insufficient_funds", self.insufficient_funds )
        
        self.roomsnd = []
        self.vox = []
        self.clientvox = []
        self.sciencevox = []
        self.bgm = []
        self.sfx = []

        self.funds = settings.STARTING_FUNDS
        self.peeps = {}
        #load sounds
        pygame.mixer.init()

        for i in range(len(DoomMixer.vox)):
            arr = []
            for j in range(len(DoomMixer.vox[i])):
                array = []
                for k in range(len(DoomMixer.vox[i][j])):
                    array.append(pygame.mixer.Sound(DoomMixer.vox[i][j][k]))
                arr.append(array)
            self.vox.append(arr)
                                       
        for i in range(len(DoomMixer.roomsources)):
            self.roomsnd.append(pygame.mixer.Sound(DoomMixer.roomsources[i]))
           
        for i in range(len(DoomMixer.bgmsources)):
            self.bgm.append(DoomMixer.bgmsources[i])   
        
        for sfx in DoomMixer.sfxsources:
            self.sfx.append(pygame.mixer.Sound(sfx))
        
        pygame.mixer.music.load(self.bgm[1])   
        pygame.mixer.music.play(-1)

    def play_room(self, floor, room_id):
         self.roomsnd[room_id - 1].play()
       
    def entity_hello(self, id, x, y, sprite, character):
        #sprite = (0, 1, 2)
        #scientist, igor, client
        self.peeps[id] = (sprite, character);
        self.vox[sprite][character][0].play()
        
    def entity_bye(self, id): 
        sprite = self.peeps[id][0]
        character = self.peeps[id][1]
        self.vox[sprite][character][1].play()
        self.peeps.pop(id)
    
    def funds(self, funds):
        if funds > self.funds:
            self.sfx[0].play()
        elif funds < self.funds:
            self.sfx[1].play()
        self.funds = funds
     
    def insufficient_funds(self):
        self.sfx[2].play()

    # play new background music, current track faded out or cut
    def playbgm(self, title, sharp = True):
        bgm = self.sfx[title]
    
        if sharp == true:
            pygame.mixer.music.queue(bgm)
            pygame.mixer.music.stop()       
        else:
            pygame.mixer.music.queue(bgm)
            pygame.mixer.music.fadeout()  

