import fge
from fge import *

TEXTURE_SEQUENCE = [ "5thGearLogo", "DevCredits", "FacultyCredits", "DigiPenCredits", "ToolAttribution", "Thanks" ]
TEXTURE_DURATION = 10.43
TEXTURE_INDEX = 0
NEXT_SCENE = "MainMenu"
TIMER = 0.0

def on_init(id):
    global TEXTURE_SEQUENCE
    global TEXTURE_INDEX
    global TIMER
    global TEXTURE_INDEX
    
    TEXTURE_INDEX = 0
    TIMER = 0.0

    Renderer.GetInstance().mAntiAliasing = False
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
    if (TIMER > TEXTURE_DURATION):
        TIMER = 0.0
        TEXTURE_INDEX = TEXTURE_INDEX + 1
        if (TEXTURE_INDEX < len(TEXTURE_SEQUENCE)):
            model = fge.GetModel(id)
            model.mpMaterial = ResourceManager.GetInstance().LoadMaterial(TEXTURE_SEQUENCE[TEXTURE_INDEX])
    
    if (TEXTURE_INDEX >= len(TEXTURE_SEQUENCE) or InputManager.GetInstance().IsTriggered("Interact") or InputManager.GetInstance().IsTriggered("confirm") or InputManager.GetInstance().IsTriggered("start") or InputManager.GetInstance().IsTriggered("click_left") or InputManager.GetInstance().IsTriggered("click_right")):
        Renderer.GetInstance().mAntiAliasing = True
        fge.ChangeScene(NEXT_SCENE)