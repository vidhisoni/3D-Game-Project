import fge
from fge import *
max_time = 60.0
end = False
started = False
team_score = {"blue":0,"green":0}
def on_init(id):
    ob = fge.GetObserver(id)
    global max_time
    ob.SetValue("time", max_time)
    audio = fge.GetAudio(id)
    audio.Load("Bg01.mp3",True)

def on_event(id,event):
     if(event.GetType()=="ContainerMatchEvent"):
         global end
         if(not end):
            global team_score
            entities = fge.GetEntities("Goal")
            str = ""
            for e in entities:
                if(event.mContainerID == e):
                    str = fge.GetName(e)
                    break
            if(str =="Blue-Goal"):
                team_score["green"] += 1
            elif(str == "Green-Goal"):
                team_score["blue"] += 1
     elif(event.GetType() == "PauseEvent"):
        audio = fge.GetAudio(id)
        pause = event
        if(not pause.mPause):
            print('play')
            audio.PlayLoop()
            audio.Volume(.65)
        else:
            audio.Stop()
        
        

def on_update(id, dt):
    global started
    x = 190
    z = 101
    y = 4
    ob = fge.GetObserver(id)
    players = fge.GetComponents("Player")
    loc = LocalizationManager.GetInstance()
    rend = Renderer.GetInstance()
    or_time = ob.GetValue("time")
    time = or_time - dt*.001
    if(time < 0):
        or_time = 0
    balls = fge.GetEntities("Ball")
    objs = []
    for ball in balls:
        objs.append(ball)
        break
    #display team scores
    global max_time
    time_str = "Time Left: "+str(int(or_time))
    rend.RenderText(time_str,0.0, 300.0, 1.1, 1-(or_time/max_time), 0, (or_time/max_time))
    global team_score
    goal = "Blue: "+str(int(team_score["blue"]))
    rend.RenderText(goal,-200.0, 350.0, 1.5, 0.25, 0.25, 1)
    goal = "Green: "+str(int(team_score["green"]))
    rend.RenderText(goal,200.0, 350.0, 1.5, 0.25, 1, 0.25)
    if(time < 0):
        global end
        if(not end):
            audio = fge.GetAudio(id)
            audio.Stop()
            audio = fge.GetAudio(id)
            audio.Load("End.mp3",False)
            audio.Play()
            
        end = True
        s = ""
        color = [1,1,1]
        if(team_score["blue"] > team_score["green"]):
            s = "BLUE WINS!!!"
            color = [0,0,1]
        elif(team_score["green"] > team_score["blue"]):
            s = "GREEN WINS!!!"
            color = [0,1,0]
        else:
            s = "draw.."
        rend.RenderText(s,0.0, 0.0, 1.5,color[0], color[1], color[2])
        #use particles and whatnot
        # add restart logic here
    
    for player in players:
        p_id = player.GetOwnerID()
        objs.append(p_id)
        ob.SetValue("time", time)
    for p_id in objs:
        tr = fge.GetTransform(p_id)
        pos = tr.GetPosition()
        too_fwd = pos[2] > z
        too_back = pos[2] < -z
        too_down = pos[1] < -y/3.0
        too_up = pos[1] > y*8
        too_left = pos[0] < -x
        too_right = pos[0] > x
        if(too_back or too_fwd or too_left or too_right or too_down or too_up):
            reset = fge.GetResetEvent()
            reset.mResetX = 0#randomize based on player
            reset.mResetZ = 0#randomize based on player
            reset.mResetY = 10
            reset.mObjectId = p_id
            fge.SendEvent(reset, p_id)
            
   