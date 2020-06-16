import fge
from fge import *
from math import sin
from math import pi

INITIAL_POS_Z = 0.0
MAX_Y = 170.0
MIN_Y = 90.0
time = 2.05
current_time = 0.0

def on_init(id):
    global INITIAL_POS_Z
    INITIAL_POS_Z = fge.GetTransform(id).GetPosition()[2]
    cam = fge.GetCamera(id)
    cam.RotateCamera(0.0, 3.0 * 3.1415, True)
    audio = fge.GetAudio(id)
    audio.Load("PublicLoop.mp3",True)
 

def on_event(id,event):
    if(event.GetType()=="ContainerMatchEvent"):
         global time
         global current_time
         current_time = time
    elif(event.GetType()=="PauseEvent"):
         audio = fge.GetAudio(id)  
         pause = event
         if(pause.mPause):
             audio.Stop()
         else:
            audio.PlayLoop()
            audio.Volume(.04)

def on_update(id, dt):
    global current_time
    global time
    audio = fge.GetAudio(id)
    if(current_time > 0):
        current_time -= .001*dt
        audio.Volume(0.51*( current_time/time)+0.04)
    else:
        audio.Volume(.04)

    global INITIAL_POS_Z
    cam = fge.GetCamera(id)
    cameraPos = fge.GetTransform(id).GetPosition()
    sumX = absX = 0.0
    sumZ = INITIAL_POS_Z *5.0
    playerIDs = fge.GetEntities("PlayerObject")
    playerIDs += fge.GetEntities("Ball")
    for playerID in playerIDs:
        playerTransform = fge.GetTransform(playerID)
        sumX += playerTransform.GetPosition()[0]
        sumZ += playerTransform.GetPosition()[2] 
    for id1 in playerIDs:
        for id2 in playerIDs:
            if(id2 <= id1): continue
            t1 = fge.GetTransform(id1)
            t2 = fge.GetTransform(id2)
            absX += abs(t1.GetPosition()[0]-t2.GetPosition()[0])
    
    sumX /= len(playerIDs) +3
    sumZ /= len(playerIDs) +3
    ymove = 0
    global MAX_Y
    global MIN_Y
    absX /= len(playerIDs)
    MID_POINT =(MAX_Y + MIN_Y)/2.0 
    if(len(playerIDs) > 1):
        if(absX > 8.0 and cameraPos[1] < MAX_Y):
            ymove = MAX_Y - cameraPos[1]/absX
        if(absX > 6.5 and cameraPos[1] <= MID_POINT):
            ymove = (MID_POINT - cameraPos[1] )/absX
        elif(absX <5.0 and absX > 0 and cameraPos[1] >= MIN_Y):
            ymove = (MIN_Y - cameraPos[1] )/absX
    if(cameraPos[1]  < MIN_Y): 
        ymove = MIN_Y - cameraPos[1] 
    cam.MoveCamera(dt,sumX - cameraPos[0],ymove,sumZ - cameraPos[2], False, False, False)

    im = InputManager.GetInstance()
    if(im.IsTriggered("cam2")):
        cm = CameraManager.GetInstance()
        cm.SetCurrentCamera(cam)