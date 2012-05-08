# audio.py - manipulates pyglet.media.Player according to game events
import os, sys, pygame, event

class DoomMixer:
# manages playback of streaming audio files (music) and static audio files (sound effects)

# audio source files
    sfxsources = []
    voicesources = []
    bgmsources = []

    def __init__(self, event_manager):
        self.event = event_manager
        self.sfx = {}
        self.voice = {}
        self.bgm = {}
        
        for name in sfxsources:
            pass

        for name in voicesources:
            pass
            
        for name in bgmsources:
            pass

 #       self.event.register()        
 #       self.event.register()        
 #       self.event.register()        

        pygame.mixer.init()
    
    # creates associative array entry for static audio object   
    def loadsfx(self, sfxname):
        self.sfx[sfxname] = pygame.mixer.Sound(sfxname)
  
    # creates associative array entry for static audio object   
    def loadvoice(self, voicename):
        self.voice[voicename] = pygame.mixer.Sound(voicename)

    # creates associative array entry for streaming audio object   
    def loadbgm(self, bgmname):
        self.sfx[bgmname] = pygame.mixer.Sound(bgmname)


    # generic audio call
    def make_noise(self, ):
        pass

    # play sound effect track
    def playsfx(self, title): 
        self.sfx[title].play()   
    
    # play voice track
    def playvoice(self, title):
        self.voice[title].play()
            

    # play new background music, current track faded out or cut
    def playbgm(self, title, sharp = True):
        bgm = self.sfx[title]
    
        if sharp == true:
            pygame.mixer.music.queue(bgm)
            pygame.mixer.music.stop()       
        else:
            pygame.mixer.music.queue(bgm)
            pygame.mixer.music.fadeout()  

# need some code initialising listening for events, handling events by playing appropriate audio
