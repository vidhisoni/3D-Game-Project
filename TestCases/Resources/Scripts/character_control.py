import fge
from fge import Player
from fge import Controller
from fge import Animator
from fge import Body


def on_init(id):
    player = fge.GetPlayer(id)
    player.SetMaxVelocity(4.0)

def on_update(id, dt):
    con = fge.GetController(id)
    player = fge.GetPlayer(id)
    animator = fge.GetAnimator(id)
    #update the player
    speed = 0.5
    x = y = 0
    if(con.IsPressed("up")):
        player.Rotate(180)
        y -= speed
    elif(con.IsPressed("down")):
        player.Rotate(0)
        y += speed
    if(con.IsPressed("left")):
        player.Rotate(270)
        x -= speed
    elif(con.IsPressed("right")):
        player.Rotate(90)
        x += speed
    gnd = player.IsGrounded()
    if(x!=0 or y != 0):
        if(gnd):
            animator.ChangeState("Walk")
        else:
            animator.ChangeState("Jump")
        player.Move(x,y)
    if(con.IsTriggered("action1")):
        animator.ChangeState("Jump")
        player.Jump(6.7)

    body  =  fge.GetBody(id)
    vel = body.GetVelocity()
    xV = vel[0]
    zV = vel[2]
    
    if(xV == 0 and zV == 0 and gnd and animator.GetSkellState() != "Idle"):
        animator.ChangeState("Idle")
   