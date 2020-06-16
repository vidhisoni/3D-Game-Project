import fge
from fge import CameraManager
from fge import Player
from fge import Transform
from fge import InputManager
from fge import Event

def on_init(id):
    pass

def on_event(event:Event,id):
    pass

def on_update(id, dt):
    players = fge.GetComponents("Player")
    player = players[0]
    #check and update the camera
    move_x = move_y = move_z = 0
    cam = fge.GetCamera(id)
    cameraTransform = fge.GetTransform(id)
    cam_pos = cameraTransform.GetPosition()  
   
    player_pos = fge.GetTransform(player.GetOwnerID()).GetLocalPosition()

    diff_x = cam_pos[0] - player_pos[0]
    diff_y = cam_pos[1] - player_pos[1] - 2
    diff_z = cam_pos[2] - player_pos[2] - 8

    if(abs(diff_x) > .25):
        move_x = -diff_x * .25
    if(diff_z > 1):
        move_z = -diff_z * .15
    elif(diff_z < 0):
        move_z = -diff_z  *.35
    if(diff_y > 1):
        move_y =  -diff_y * 1.85
    elif(diff_y < 0):
        move_y = -diff_y  *.45

    cam_pos[0] = cam_pos[0] + dt * move_x * 0.005
    cam_pos[1] = cam_pos[1] + dt * move_y * 0.005
    cam_pos[2] = cam_pos[2] + dt * move_z * 0.005
    cameraTransform.SetPosition(cam_pos[0], cam_pos[1], cam_pos[2])

    im = InputManager.GetInstance()
    if(im.IsTriggered("cam2")):
        cm = CameraManager.GetInstance()
        cm.SetCurrentCamera(cam)
