import fge
from fge import Event
from fge import Button
from fge import Audio

def on_init(id):
    audio = fge.GetAudio(id)
    audio.Load("Test1.wav")
    
def on_event(event:Event,id):
    pass

def on_update(id, dt):
    button =  fge.GetButton(id) 
    audio = fge.GetAudio(id)
    if(button.IsEntered()):
        audio.Play()
        audio.Volume(0.4)
    elif(button.IsReleased()):
        audio.Stop()
