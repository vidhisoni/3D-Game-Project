import fge
from fge import Button
from fge import Particles
from fge import Renderer
from fge import LocalizationManager
from fge import ComponentManager

def on_init(id):
    pass
    
def on_update(id, dt):
    button =  fge.GetButton(id) 
    
    if(button.IsPressed()):
        loc = LocalizationManager.GetInstance()
        rend = Renderer.GetInstance()
        hello = loc.GetText("thankyou.txt")
        rend.RenderText(hello,10.0, 10.0, 1.0, 1, 0, 1)
        hello = loc.GetText("thankyou.txt","ru")
        rend.RenderText(hello,100.0, -100.0, 0.75, 1.0, 1.0, 0.25)