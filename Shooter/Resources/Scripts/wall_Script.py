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

def on_init(id):
    pass
    
def on_event(event:Event,id):
    pass

def on_update(id, dt):
    collided = fge.GetCollider(id).mIsCollided()
    wall = fge.GetWall(id)
    wallType = wall.mType
    if(wallType == "wall"):
        if(collided == True):
            isBulletCollider = PhysicsManager.GetInstance().GetCollisionManager().RetrieveFirstContact(fge.GetCollider(id), "BULLET", ContactType.TriggerEnter)
            if isBulletCollider is not None:
                bullet = fge.GetBullet(isBulletCollider.mOwnerID())
                if(bullet.GetOwner() == "Player"):
                    WallHit(id)

    if(wallType == "barrier"):
        trans = fge.GetTransform(id)
        pos = trans.GetPosition()
        if(wall.mKills == 6):
            pos[1] -= 0.005;
            trans.SetPosition(pos[0], pos[1], pos[2])
            if (pos[1] < -1.0):
                wall.Destroy()

def WallHit(id):
    fge.GetWall(id).mHealth -= 10
    wall = fge.GetWall(id)
    wallHealth = fge.GetWall(id).mHealth
    if wallHealth < 200 and wallHealth > 100:
        wall.ChangeColor("Yellow")
    elif wallHealth <= 100 and wallHealth > 0:
        wall.ChangeColor("Red")
    elif wallHealth == 0:
        wall.Destroy()


    

