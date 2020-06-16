import fge
from fge import *

TEXTURE_SEQUENCE = [ "DigiPenLogo", "SplashControls", "ShipITLogo", "FMODLogo"]
TEXTURE_DURATION = 4.0
TEXTURE_INDEX = 0
NEXT_SCENE = "MainMenu"
TIMER = 0.0

def on_init(id):
    global TEXTURE_SEQUENCE
    global TEXTURE_INDEX
    global TIMER
    
    TEXTURE_INDEX = 0
    TIMER = 0.0
    
    model = fge.GetModel(id)
    model.mpMaterial = ResourceManager.GetInstance().LoadMaterial(TEXTURE_SEQUENCE[TEXTURE_INDEX])
    
def on_event(id,event):
    pass
        
def on_update(id, dt):
    global TEXTURE_SEQUENCE
    global TEXTURE_DURATION
    global TEXTURE_INDEX
    global NEXT_SCENE
    global TIMER

   
    TIMER = TIMER + 17.0 * 0.001
    current_item = TEXTURE_SEQUENCE[TEXTURE_INDEX]
   
    if (TIMER > TEXTURE_DURATION):
        TIMER = 0.0
        TEXTURE_INDEX = TEXTURE_INDEX + 1
        if (TEXTURE_INDEX < len(TEXTURE_SEQUENCE)):
            model = fge.GetModel(id)
            model.mpMaterial = ResourceManager.GetInstance().LoadMaterial(TEXTURE_SEQUENCE[TEXTURE_INDEX])
    im = InputManager.GetInstance()
    continue_pressed =  im.IsTriggered("Interact",0) or \
        im.IsTriggered("confirm",0) or \
        im.IsTriggered("start",0) or \
        im.IsTriggered("click_left") or \
        im.IsTriggered("click_right")
    if (TEXTURE_INDEX >= len(TEXTURE_SEQUENCE) or continue_pressed):
        fge.ChangeScene(NEXT_SCENE)