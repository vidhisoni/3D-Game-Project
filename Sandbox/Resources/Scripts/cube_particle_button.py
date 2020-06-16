import fge
from fge import Event
from fge import Button
from fge import Particles
from fge import Transform

def on_init(id):
    particles = fge.GetParticles(id)
    particles.mParticleType = "Cube"
    particles.SetRunning(False)

def on_event(event:Event,id):
    pass
        
def on_update(id, dt):
    button =  fge.GetButton(id) 
    particles = fge.GetParticles(id)
    if(button.IsPressed()):
        trans =  fge.GetTransform(id)
        pos = trans.GetPosition()
        particles.mSpread = 2.5
        particles.SetPosition(pos[0]+1.5,pos[1]+5,pos[2]-10)
        particles.SetNumber(3000) 
        particles.mParticleType = "Cube"
        particles.SetRunning(True)
    else:
        particles.SetRunning(False)
        