import fge
from fge import Event
from fge import Button
from fge import Model
from fge import Material
from fge import ComponentManager
from fge import ResourceManager

texture0= "Noise0"
texture1= "Noise1"
currentTex = texture0
def on_init(id):
    pass

def on_event(event:Event,id):
    pass
    
def on_update(id, dt):
    button =  fge.GetButton(id) 
    if(button.IsEntered()):
        models = ComponentManager.GetInstance().GetComponents("ModelComponent")
        global currentTex
        for model in models:
            if(model.mpMaterial.mName == currentTex):
                global texture0
                global texture1
                if(currentTex == texture0):
                    currentTex = texture1
                else:
                    currentTex =texture0
                model.mpMaterial = ResourceManager.GetInstance().LoadMaterial(currentTex)
                break

        
