import fge
from fge import Button
from fge import Particles
from fge import Transform
from fge import Event

def on_init(id):
    particles = fge.GetParticles(id)
    particles.mParticleType = "Sphere"
    particles.SetRunning(False)
 
    
def on_event(event:Event,id):
    pass


def on_update(id, dt):
    button =  fge.GetButton(id) 
    particles = fge.GetParticles(id)
    if(button.IsPressed()):
        trans =  fge.GetTransform(id)
        pos = trans.GetPosition()
        particles.mRadius_min = 1.3
        particles.mRadius_max = 3.0
        particles.SetPosition(pos[0],pos[1]+4,pos[2]-6)
        particles.SetNumber(1500) 
        particles.SetRunning(True)
    else:
        particles.SetRunning(False)
        