import fge
from fge import Button
from fge import Particles
from fge import Transform

def on_init(id):
    particles = fge.GetParticles(id)
    particles.SetRunning(False)
    particles.mParticleType = "Default"

def on_event(event:Event,id):
    pass
    
def on_update(id, dt):
    button =  fge.GetButton(id) 
    particles = fge.GetParticles(id)
    if(button.IsPressed()):
        trans =  fge.GetTransform(id)
        pos = trans.GetPosition()
        particles.SetPosition(pos[0],pos[1]+3.25,pos[2]-4)
        particles.SetNumber(1500) 
        particles.SetRunning(True)
    else:
        particles.SetRunning(False)
