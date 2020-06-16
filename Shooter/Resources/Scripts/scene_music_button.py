import fge
from fge import Button
from fge import Audio
from fge import Event

ran = False
def on_init(id):
    audio = fge.GetAudio(id)
    audio.Load("BG02.mp3",True,True)
  
    
def on_event(event:Event,id):
    pass

def on_update(id, dt):
    button =  fge.GetButton(id) 
    audio = fge.GetAudio(id)
    global ran
    if(button.IsEntered() and not ran):
        ran = True
        audio.Play(-1)
        audio.Volume(0.25)