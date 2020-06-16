import fge
from fge import CameraManager
from fge import Player
from fge import Transform
from fge import InputManager
from fge import Mouse

def on_init(id):
    pass

def on_update(id, dt):
    players = fge.GetComponents("Player")
    player = players[0]
    #check and update the camera
    
    move_x = move_y = move_z = 0
    cam = fge.GetCamera(id)
    cam_pos = cam.GetPos()  
   
    player_pos = fge.GetTransform(player.GetOwnerID()).GetPosition()
   
    cam.MoveCamera(dt,player_pos[0],player_pos[1]+2,player_pos[2])
    
    mouse = Mouse.GetInstance()
    rot_x = rot_y=0
    if(mouse.IsPressed(1)):
        m_x = mouse.MouseDeltaX()
        m_y = mouse.MouseDeltaY()
        if(m_x < 0 ):
            rot_x += rot_sp * .5
        elif(m_x > 0):
            rot_x -= rot_sp  * .5
        if(m_y < 0):
            rot_y += rot_sp  * .5
        elif(m_y > 0):
            rot_y -= rot_sp  * .5
    if(mouse.ScrollUp()):
        move_z += mv_sp
    elif(mouse.ScrollDown()):
        move_z -= mv_sp

   
    
    
    cam.RotateCamera(rot_x,rot_y,True)


    im = InputManager.GetInstance()
    if(im.IsTriggered("cam3")):
        cm = CameraManager.GetInstance()
        cm.SetCurrentCamera(cam)
