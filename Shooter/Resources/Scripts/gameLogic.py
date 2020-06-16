import fge
from fge import Event
from fge import Button
from fge import Audio
from fge import Transform
from fge import Collider
from fge import Audio
from fge import PhysicsManager
from fge import CollisionManager
from fge import BulletComp
from fge import ContactType
from fge import Enemy
from fge import Wall
from fge import Mouse
from fge import InputManager
from fge import EnemyStateManager
from fge import RayCast
from fge import *

playerHealth = 0

currentDelta = 0
previousDelta = 0
maxFireRate = 0.2

def on_init(id):
    global playerHealth
    playerHealth = 100
    pass
    
def on_event(event:Event,id):
    pass

def on_update(id, dt):

    global playerHealth


    """ 
    global currentDelta, previousDelta, maxFireRate 

   #RAY Cast
    currentDelta += dt / 1000.0
    raycast = RayCast.GetInstance()
    input = InputManager.GetInstance()
    mouse = Mouse.GetInstance()
    mousePos = mouse.GetScreenPos()

    raycast.MoveCrossHair(mousePos[0], mousePos[1])
    
    #Fire Bullet
    if mouse.IsPressed(0):
        if currentDelta - previousDelta > maxFireRate:
            raycast.CastRay(mousePos[0], mousePos[1], True)
            previousDelta = currentDelta;

    #Throw Grenade
    if input.IsReleased(10) :
        raycast.CastRay(mousePos[0], mousePos[1], False)
   """

    #COLLISION
    collided = fge.GetCollider(id).mIsCollided()
    if(collided == True):
        isBulletCollider = PhysicsManager.GetInstance().GetCollisionManager().RetrieveFirstContact(fge.GetCollider(id), "BULLET", ContactType.TriggerEnter)
        if isBulletCollider is not None:
            bullet = fge.GetBullet(isBulletCollider.mOwnerID())
            if(bullet.GetOwner() == "Enemy"):
                PlayerHit(id, True)

    #WIN Condition
    loc = LocalizationManager.GetInstance()
    rend = Renderer.GetInstance()
    player = fge.GetPlayer(id)
    if player.mKilled == 6:
        txt = loc.GetText("victory.txt")
        rend.RenderText(txt,0.0, 0.0, 1.0, 0, 0, 1)
    if playerHealth == 0:
        txt = loc.GetText("defeat.txt")
        rend.RenderText(txt,0.0, 0.0, 1.0, 1, 0, 0)
        ESM = EnemyStateManager.GetInstance()
        ESM.mGameOver = True

    txt = "Enemies Killed :" + str(player.mKilled)
    rend.RenderText(txt , 650.0, -490.0, 1.0, 1, 0, 0)


    txt1 = "Health :" + str(playerHealth)
    rend.RenderText(txt1 ,700.0, -450.0, 1.0, 0, 0, 1)



def PlayerHit(id, isEnemy):
    audio = fge.GetAudio(id)
    global playerHealth
    if isEnemy == True:
        if(playerHealth > 0):
            audio.Play();
            playerHealth -= 10
        if playerHealth == 0:
            print("GG")

        
    



    

