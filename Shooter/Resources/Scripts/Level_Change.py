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
from fge import LevelEditor
from fge import ObjectFactory

def on_init(id):
    pass
    
def on_event(event:Event,id):
    pass

def on_update(id, dt):
    collided = fge.GetCollider(id).mIsCollided()
    wall = fge.GetWall(id)
    wallType = wall.mType
    if(wallType == "LevelChange"):
        if(collided == True):
            print("Yes")
            isPlayerCollider = PhysicsManager.GetInstance().GetCollisionManager().RetrieveFirstContact(fge.GetCollider(id), "Player", ContactType.TriggerEnter)
            if isPlayerCollider is not None:
                levelchange = LevelEditor.GetInstance()
                levelchange.ChangeLevel()
                objectfac = ObjectFactory.GetInstance()
                objectfac.mChangeLevel = "Test"



    

