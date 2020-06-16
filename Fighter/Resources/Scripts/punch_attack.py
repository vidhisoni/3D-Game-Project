import fge
from fge import *
import math

FORCE =100.0

class State:
    pass

__state = {}
DIS = 0.2


def on_init(id):
    state = State()
    state.hit_duration = 0.5
    state.hit_time = 0
    state.recharge_duration= 1.2
    state.recharge_time = 0
    state.attack = False
    global __state
    __state[id] = state
    audio = fge.GetAudio(id)
    audio.Load("Hit01.mp3")

def on_event(id,event):
    pass

def on_update(id, dt):
    global __state
    if not __state:
        on_init(id)
    _dt =  dt * .001;
    pId = fge.GetParentID(id)
    trans = fge.GetTransform(id)
    gpos = trans.GetPosition()
    pos = trans.GetLocalPosition()
    if(__state[id].attack):
        __state[id].hit_time -= _dt
        global DIS
        distance = DIS *math.sin( __state[id].hit_time / __state[id].hit_duration* 2*math.pi)
        pos[1] = pos[1] +distance
        if(__state[id].hit_time > 0):
            a = fge.GetAttackEvent()
            a.mAttack = id
            global FORCE
            a.mForce = FORCE
            fge.BroadcastEvent(a)
        else:
            __state[id].attack = False
            __state[id].recharge_time =  __state[id].recharge_duration
    else:
        pos[1] = 0
        part = fge.GetParticles(id) 
        part.SetRunning(False)
        if(__state[id].recharge_time > 0):
            __state[id].recharge_time -=  _dt
        else:
            con = fge.GetController(pId)
            if(con.IsTriggered("attack")):
                if (__state[id].recharge_time <= 0 and not __state[id].attack):
                     audio = fge.GetAudio(id)
                     audio.Play()
                     audio.Volume(0.4)
                     __state[id].hit_time = __state[id].hit_duration
                     __state[id].attack = True
    
    trans.SetLocalPosition(pos[0],pos[1],pos[2])
