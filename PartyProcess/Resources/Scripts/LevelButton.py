import fge
import struct
from fge import *


def on_init(id):
    levelbutton = fge.GetLevelButton(id, "LevelButton",True)


def on_event(id,event):
    levelbutton = GetLevelButton(id)
    worldID = levelbutton.WorldID
    if(event.GetType() == "ContactEvent"):
        #print(event.mContactType)
        otherID = -1
        if (event.mId1 == id):
            otherID = event.mId2
        else:
            otherID = event.mId1
        contactType = ContactType
        if(event.mContactType == contactType.TriggerEnter):
            levelbutton.IN = True
        if(event.mContactType == contactType.TriggerExit):
            levelbutton.IN = False


       

def on_update(id, dt):
    levelbutton = GetLevelButton(id)
    isUnlocked = levelbutton.isUnlocked
    HighScore = levelbutton.HighScore
    LevelName = levelbutton.LevelName
    UnlockScore = levelbutton.UnlockScore
    worldID = levelbutton.WorldID
    Level_str = "Level : {}".format(LevelName)
    score_str = "High Score : {:0.0f}".format(HighScore)
    unlock_str = "Score {:0.0f} on Previous Level".format(UnlockScore)
    
    SceneMan = SceneManager.GetInstance()
    mWidth = SceneMan.ScreenWidth / 2
    mHeight = SceneMan.ScreenHeight / 2

    scaleVal = (fge.GetWindowWidth() / 1920.0)
    if (scaleVal == 1.0):
        scaleVal *= 0.9

    if(levelbutton.IN):
        Renderer.GetInstance().RenderText(score_str, 0.44 * fge.GetWindowWidth(), 0.05 * fge.GetWindowHeight(), scaleVal * 1.2, 1, 1, 1, 1)
        if(isUnlocked):
            Renderer.GetInstance().RenderText(" Ready to start! ", 0.75 * fge.GetWindowWidth() , 0.05 * fge.GetWindowHeight(), scaleVal, 1, 1, 1, 1)
        else:
            Renderer.GetInstance().RenderText(unlock_str , 0.75 * fge.GetWindowWidth(), 0.05 * fge.GetWindowHeight(), scaleVal, 1, 1, 1, 1)
