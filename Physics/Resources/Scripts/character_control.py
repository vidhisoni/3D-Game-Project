import fge
from fge import Player
from fge import Controller
from fge import Body

init = {}

def on_init(id):
    player = fge.GetPlayer(id)
    player.SetMaxVelocity(8.0)


def on_event(id,event):
    pass
    

def on_update(id, dt):
    con = fge.GetController(id)
    player = fge.GetPlayer(id)
    
    #update the player
    speed = 2
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
        player.Jump(7)
    #if(r_count > 0):
        #player.Rotate(rotate/r_count)  
    
   
