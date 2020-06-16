import fge
from fge import Button
from fge import Animator
from fge import ComponentManager
from fge import Component
from fge import Event

def on_init(id):
    pass
  

def on_event(event:Event,id):
    pass

def on_update(id, dt):
    button = fge.GetButton(id)
    playerId = button.mPlayerId
    animators = ComponentManager.GetInstance().GetComponents("Animator")
    amId = -1
    for a in animators:
        if(a.GetOwnerID() !=  playerId):
            amId = a.GetOwnerID()
            break
    model = fge.GetModel(amId)
    if(button.IsEntered()):
        model.MakeRainbow()
