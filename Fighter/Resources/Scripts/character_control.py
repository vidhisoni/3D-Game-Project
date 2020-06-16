import fge
from fge import Audio
from fge import AttackEvent
from fge import ResetEntityEvent
from fge import Event
from fge import Player
from fge import Controller
from fge import Animator
from fge import Body
from fge import Particles
from fge import PhysicsManager

init = {}

def on_init(id):
    player = fge.GetPlayer(id)
    player.SetMaxVelocity(20.0)
    particles = fge.GetParticles(id)
    particles.SetRunning(False)
    particles.mParticleType = "Explosion"
    audio = fge.GetAudio(id)
    audio.Load("Hurt02.mp3")
    global init_x
    trans = fge.GetTransform(id)
    if(trans):
        init[id] = trans.GetPosition()[0]


def on_event(id,event):
    if(event.GetType()=="AttackEvent"):
        attack = event
        player = fge.GetPlayer(id)
        attacks = fge.GetChildren(id, "Glove")
              
        if(attack.mAttack not in attacks):
            phy = PhysicsManager.GetInstance()
            my_col = fge.GetCollider(id)
            a_col = fge.GetCollider(attack.mAttack)
            did_hit = phy.OnTriggerEnter(my_col,a_col) or phy.OnTriggerStay(my_col,a_col)
            did_exit = phy.OnTriggerExit(my_col,a_col)
            if(did_hit):
                body = fge.GetBody(id)
                trans_my = fge.GetTransform(id)
                pos_my = trans_my.GetPosition()
                trans_a = fge.GetTransform(attack.mAttack)
                pos_a = trans_a.GetPosition()
                max = ((pos_my[0]-pos_a[0])**2 + (pos_my[1]-pos_a[1])**2 +(pos_my[2]-pos_a[2])**2)**(.5)
                reaction = ( (pos_my[0]-pos_a[0])/max, (pos_my[1]-pos_a[1])/max, (pos_my[2]-pos_a[2])/max )
                force = attack.mForce
                body.SetVelocity(reaction[0] * force,reaction[1]* force,reaction[2]* force)
                
                part = fge.GetParticles(attack.mAttack) 
                part.SetPosition(pos_my[0],pos_my[1],pos_my[2])
                part.SetRunning(True)
                audio = fge.GetAudio(id)
                audio.Volume(0.6)
                audio.Play()
            elif(did_exit):
                part = fge.GetParticles(attack.mAttack) 
                part.SetRunning(False)

    elif(event.GetType()=="ResetEntityEvent"):
        reset = event
        if(id ==  reset.mObjectId): 
            global init
            fge.GetTransform(id).SetPosition(init[id],reset.mResetY,reset.mResetZ)
            fge.GetBody(id).SetVelocity(0,0,0)
    

def on_update(id, dt):
    con = fge.GetController(id)
    player = fge.GetPlayer(id)
    
    #update the player
    speed = 5
    x = y = z = 0
    rotate = 0
    r_count = 0;
    if(con.IsPressed("up")):
        r_count +=1
        rotate +=180
        y -= speed
    elif(con.IsPressed("down")):
        r_count +=1
        rotate +=0
        y += speed
    if(con.IsPressed("left")):
        r_count +=1
        rotate +=270
        x -= speed
    elif(con.IsPressed("right")):
        r_count +=1
        rotate += 90
        x += speed
    if(x!=0 or y != 0):
        player.Move(x,y)
    if(con.IsTriggered("jump")):
        z =1
        player.Jump(10)
    if(r_count > 0):
        player.Rotate(rotate/r_count)
    parts = fge.GetChildren(id, "InvisibleCube")    
    
    for p in parts:
        particles = fge.GetParticles(p)
        bool  = x != 0 or y != 0 or z !=0
        particles.SetRunning(bool)
        particles.mSpread = 0.5
        trans =  fge.GetTransform(p)
        pos = trans.GetPosition()
        particles.SetPosition(pos[0],pos[1],pos[2])
