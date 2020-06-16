import fge
from fge import *
run_time = 1.0
run_times = {}

def on_init(id):
    global run_times
    global run_time
    run_times[id] = 0
    part = fge.GetParticles(id) 
    part.SetRunning(False)
    part.mParticleType = "Explosion"
    
   

def on_update(id, dt):
    global run_times
    if(run_times[id] > 0):
        run_times[id] -= dt*.001
        trans = fge.GetTransform(id)
        pos_my = trans.GetPosition()
        part = fge.GetParticles(id) 
        part.SetPosition(pos_my[0],pos_my[1]+10,pos_my[2])
        part.SetRunning(run_times[id] >=0)

def on_event(id,event):
    if(event.GetType()=="ContactEvent"):
        c = event
        if c.mId1 != id and c.mId2 != id: return
        ids = []
        for e in fge.GetEntities("Ball"):
            ids.append(e)
        found = False
        for i  in ids:
            if c.mId1 == i or c.mId2 == i:
                found =True
                break
        if(found and (c.mContactType == TriggerEnter or c.mContactType == CollisionEnter)):
            part = fge.GetParticles(id) 
            part.SetRunning(True)
            audio = fge.GetAudio(id)
            audio.Load("Goal01.mp3")
            audio.Play()
            audio.Volume(0.2)
            global run_times
            global run_time
            run_times[id] = run_time
            event = fge.GetContainerMatchEvent()
            event.mContainerID = id
            fge.BroadcastEvent(event)
        