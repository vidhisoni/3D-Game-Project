import fge
from fge import AttackEvent
from fge import ContactEvent
from fge import Event
from fge import Body
from fge import Particles
from fge import PhysicsManager


def on_init(id):
    particles = fge.GetParticles(id)
    particles.SetRunning(False)
    particles.mParticleType = "Explosion"
    


def on_event(id,event):
    if(event.GetType()=="AttackEvent"):
        attack = event
        phy = PhysicsManager.GetInstance()
        my_col = fge.GetCollider(id)
        a_col = fge.GetCollider(attack.mAttack)
        did_hit = phy.OnTriggerEnter(my_col,a_col)
        did_exit = phy.OnTriggerExit(my_col,a_col)
        if(did_hit):
            body = fge.GetBody(id)
            trans_my = fge.GetTransform(id)
            pos_my = trans_my.GetPosition()
            trans_a = fge.GetTransform(attack.mAttack)
            pos_a = trans_a.GetPosition()
            max = ((pos_my[0]-pos_a[0])**2 + (pos_my[1]-pos_a[1])**2 +(pos_my[2]-pos_a[2])**2)**(.5)
            reaction = ( (pos_my[0]-pos_a[0])/max, 0, (pos_my[2]-pos_a[2])/max )#maybe y issues here
            force = attack.mForce
            body.SetVelocity(reaction[0] * force,reaction[1]* force,reaction[2]* force)
                
            part = fge.GetParticles(attack.mAttack) 
            part.SetPosition(pos_my[0],pos_my[1],pos_my[2])
            part.SetRunning(True)
            part = fge.GetParticles(id) 
            part.SetPosition(pos_my[0],pos_my[1],pos_my[2])
            part.SetRunning(True)
            audio = fge.GetAudio(id)
            audio.Load("pushBall01.mp3",False,False)
            audio = fge.GetAudio(id)
            audio.Play()
        elif(did_exit):
            part = fge.GetParticles(id) 
            part.SetRunning(False)

    elif(event.GetType()=="ResetEntityEvent"):
        reset = event
        if(id ==  reset.mObjectId): 
            fge.GetTransform(id).SetPosition(reset.mResetX,reset.mResetY,reset.mResetZ)
            fge.GetBody(id).SetVelocity(0,0,0)
            part = fge.GetParticles(id) 
            part.SetRunning(False)
    elif(event.GetType()=="ContactEvent"):
        c = event
        if c.mId1 != id and c.mId2 != id:
            return
        ids = []
        for e in fge.GetEntities("Goal"):
            ids.append(e)
        found = False
        for i  in ids:
            if c.mId1 == i or c.mId2 == i:
                found =True
                break
        if(found):
            trans = fge.GetTransform(id)
            pos = trans.GetPosition()
                
            part = fge.GetParticles(id) 
            part.SetPosition(pos[0],pos[1],pos[2])
            part.SetRunning(True)

            reset = fge.GetResetEvent()
            reset.SetTime(1.0)
            reset.mResetX = 0#randomize based on player
            reset.mResetZ = 0#randomize based on player
            reset.mResetY = 5
            reset.mObjectId = id
            fge.BroadcastEvent(reset)
            audio = fge.GetAudio(id)
            audio.Load("score04.mp3")
            audio = fge.GetAudio(id)
            audio.Play()
        
    

def on_update(id, dt):
    pass
