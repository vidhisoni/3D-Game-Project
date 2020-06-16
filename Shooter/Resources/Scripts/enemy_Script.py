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


def on_init(id):
    pass
    
def on_event(event:Event,id):
    pass

def on_update(id, dt):
    collided = fge.GetCollider(id).mIsCollided()
    if(collided == True):
        isBulletCollider = PhysicsManager.GetInstance().GetCollisionManager().RetrieveFirstContact(fge.GetCollider(id), "BULLET", ContactType.TriggerEnter)
        if isBulletCollider is not None:
            bullet = fge.GetBullet(isBulletCollider.mOwnerID())
            if(bullet.GetOwner() != "Enemy"):
                EnemyHit(id, True)

        isBulletCollider = PhysicsManager.GetInstance().GetCollisionManager().RetrieveFirstContact(fge.GetCollider(id), "Grenade", ContactType.TriggerEnter)
        if isBulletCollider is not None:
            EnemyHit(id, False)


def EnemyHit(id, isBullet):
   if(isBullet == True):
        if(fge.GetEnemy(id).mHealth > 0):
            fge.GetEnemy(id).mHealth -= 20
        if(fge.GetEnemy(id).mHealth == 0):
           fge.GetEnemy(id).Destroy()
   if(isBullet == False):
        fge.GetEnemy(id).Destroy()

    

