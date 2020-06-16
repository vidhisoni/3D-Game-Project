import fge
from fge import *

def on_init(id):
    audio = fge.GetAudio(id)
    audio.Load("Main.mp3", True)
    audio.PlayLoop()
    

def on_event(id,event):
    pass

def on_update(id, dt):
    pass

