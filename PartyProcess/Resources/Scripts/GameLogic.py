import fge
import enum
import math
import array as arr
from fge import *

class difficulty(enum.Enum):
    Easy = 0
    Medium = 8
    Hard = 16
    All = 23

class state(enum.Enum):
    Intro = 0
    Gameplay = 1
    Ending = 2

SCORE = 0.0
STARTED = False
PAUSED = False
GAMES = []
GAME_WEIGHTS = []
SCORE_TEXTURES_F = []
SCORE_TEXTURES_D = []
SCORE_TEXTURES_C = []
SCORE_TEXTURES_B = []
SCORE_TEXTURES_A = []
METRIC = []
GRADES = [ "D", "C", "B", "A" ]
UI_IDS = []
MAX_TIME = -1.0
REQUEST_TIME = 0.0
REQUEST_TIME_MAX = 0.0
REWARD = 0.0
MUSIC = ""
STATE = state.Gameplay
CAMERA_START = []
CAMERA_END = []
EXITING = False
TALLY = 0.0
LEVEL_NAME = ""
STARTED_TALLY = False

def on_init(id):
    global EXITING
    global STARTED
    global SCORE
    global LEVEL_NAME
    global STARTED_TALLY
    ob = fge.GetObserver(id)
    ob.SetValue("time", 0.0)
    EXITING = False
    STARTED = False
    LEVEL_NAME = ""
    SCORE = 0.0
    STARTED_TALLY = False
    
def on_event(id,event):
    global PAUSED
    global SCORE
    global GAMES
    global GAME_WEIGHTS
    global METRIC
    global SCORE_TEXTURES_F
    global SCORE_TEXTURES_D
    global SCORE_TEXTURES_C
    global SCORE_TEXTURES_B
    global SCORE_TEXTURES_A
    global UI_IDS
    global MAX_TIME
    global REQUEST_TIME
    global REQUEST_TIME_MAX
    global REWARD
    global MUSIC
    global FINISHED
    global DIFFICULTY
    global CHANGED
    global LIMIT
    global LEVEL_NUMBER
    global STATE
    global CAMERA_START
    global CAMERA_END
    global LEVEL_NAME
    global PREVIOUS_GAME
    if(event.GetType() == "InitLevelEvent"):
        FINISHED = 0
        STARTED = False
        CHANGED = False
        playerIDs = fge.GetEntities("Player", True)
        for playerID in playerIDs:
            playerNum = fge.GetController(playerID).GetPlayer()
            if (playerNum < event.mNumPlayers):
                EntityManager.GetInstance().ToggleEntityEnable(playerID, True)
        MAX_TIME = event.mTime
        LIMIT = event.mGames
        LEVEL_NAME = event.mLevelName
        LEVEL_NUMBER = event.mLevelNumber


        DIFFICULTY = difficulty.Easy.value

        GAMES = function(LEVEL_NUMBER, DIFFICULTY)
        MUSIC = event.mMusic
        numGames = len(GAMES)

        for game in GAMES:
            GAME_WEIGHTS.append(1.0)
        METRIC = event.mGrading
        SCORE_TEXTURES_F = event.mScoreTexturesF
        SCORE_TEXTURES_D = event.mScoreTexturesD
        SCORE_TEXTURES_C = event.mScoreTexturesC
        SCORE_TEXTURES_B = event.mScoreTexturesB
        SCORE_TEXTURES_A = event.mScoreTexturesA
        randomNum = numGames * RNG.GetInstance().GenerateFloat(0.0, 1.0)
        selectionIndex = 0
        comparisonSum = GAME_WEIGHTS[selectionIndex]
        while randomNum > comparisonSum:
            selectionIndex = selectionIndex + 1
            comparisonSum = comparisonSum + GAME_WEIGHTS[selectionIndex]
        gameInt = GAMES[selectionIndex]
        PREVIOUS_GAME = gameInt
     #   print("First Game : ",PREVIOUS_GAME)
        requestMadeEvent = fge.GetRequestMadeEvent()
        requestMadeEvent.mGame = gameInt
        fge.BroadcastEvent(requestMadeEvent)


        gridID = fge.GetEntities("Grid")
        grid = fge.GetGrid(gridID[0])
        recipeSize = len(grid.GetRecipe(gameInt))
        REQUEST_TIME_MAX = 17.5 * recipeSize
        REQUEST_TIME = REQUEST_TIME_MAX
        REWARD = 2.0 * recipeSize
        
        STATE = state.Intro

        audio = fge.GetAudio(id)
        audio.Load(event.mMusic, True)
        audio.PlayLoop()
        audio.Volume(0.1)
        AudioManager.GetInstance().UnPauseAll()
        
        fge.ClearRuntimeLists()

        cameraID = CameraManager.GetInstance().GetCameraID()
        if (cameraID != -1):
            cameraTransform = fge.GetTransform(cameraID)
            CAMERA_END = cameraTransform.GetPosition()
            cameraFront = CameraManager.GetInstance().GetFront()
            CAMERA_START = [CAMERA_END[0] - 2.0 * cameraFront[0], CAMERA_END[1] - 2.0 * cameraFront[1], CAMERA_END[2] - 2.0 * cameraFront[2]]
            cameraTransform.SetPosition(CAMERA_START[0], CAMERA_START[1], CAMERA_START[2])
        
        pauseEvent = fge.GetPauseEvent()
        pauseEvent.mPause = True
        fge.BroadcastEvent(pauseEvent)
    if(event.GetType() == "RequestFilledEvent"):
        FINISHED += 1
        #print("Finished = ",FINISHED)

        game = event.mRequestedGame
        deltaMultiplier = 0.5
        if REQUEST_TIME >= 0.0:
            if REQUEST_TIME > 0.5 * REQUEST_TIME_MAX:
                deltaMultiplier = 2.0
            else:
                deltaMultiplier = 1.0
        SCORE = SCORE + round(REWARD * deltaMultiplier)

        #DIFFICULTY = difficulty.Medium.value if FINISHED == testChangeDiff.Easy else difficulty.Hard.value if FINISHED == testChangeDiff.Medium else DIFFICULTY
        if FINISHED == LIMIT[0]:
            DIFFICULTY = difficulty.Medium.value
            CHANGED = True
        if FINISHED == LIMIT[0] + LIMIT[1]:
            DIFFICULTY = difficulty.Hard.value
            CHANGED = True
        if FINISHED % 10 == 0:
            FINISHED = 0
            DIFFICULTY = difficulty.Easy.value
            CHANGED = True


        GAMES = function(LEVEL_NUMBER, DIFFICULTY)
        numGames = len(GAMES)
      #  print("Length",len(GAMES))
       


        if CHANGED:
     #     print("------------ : ", DIFFICULTY)
          i = 1
          GAME_WEIGHTS.clear()
          for game in GAMES:
            if(DIFFICULTY == 8 and i < 3):
                GAME_WEIGHTS.append(0.5)
                i = i+1
            elif(DIFFICULTY == 16 and i < 5):
                GAME_WEIGHTS.append(1.0)
                i = i+1
            else:
                GAME_WEIGHTS.append(1.5)
          randomNum = numGames * RNG.GetInstance().GenerateFloat(0.0, 1.0)
          CHANGED = False
      #    print("IF WT START")
     #     for x in range(len(GAME_WEIGHTS)):
      #        print(GAME_WEIGHTS[x], "---",GAMES[x] )
     #     print("++++++++++++++")
        else:          
            weightSum = 0.0
            for i in range(numGames):
                if game == GAMES[i]:
                    GAME_WEIGHTS[i] = 0.5 * GAME_WEIGHTS[i]
                else:
                    GAME_WEIGHTS[i] = 2.0 * GAME_WEIGHTS[i]
                weightSum = weightSum + GAME_WEIGHTS[i]
                randomNum = weightSum * RNG.GetInstance().GenerateFloat(0.0, 1.0)
        #    print("ELSE WT START")
        #    for x in range(len(GAME_WEIGHTS)):
         #       print(GAME_WEIGHTS[x], "---",GAMES[x])
        #    print("++++++++++++++")

      #  print(len(GAME_WEIGHTS))
       # print(randomNum)
        selectionIndex = 0
        comparisonSum = GAME_WEIGHTS[selectionIndex]
        while randomNum > comparisonSum:
            selectionIndex = selectionIndex + 1
       #     print(selectionIndex)
          #  if(selectionIndex > len)
            comparisonSum = comparisonSum + GAME_WEIGHTS[selectionIndex]


        if(PREVIOUS_GAME == GAMES[selectionIndex]):
            if(selectionIndex == len(GAMES)-1):
                selectionIndex = selectionIndex-1
            else:
                selectionIndex = selectionIndex+1


        gameInt = GAMES[selectionIndex]
       # print("Previous Game : ",PREVIOUS_GAME)
        PREVIOUS_GAME = gameInt
      #  print("Current Game : ",gameInt)
        requestMadeEvent = fge.GetRequestMadeEvent()
        requestMadeEvent.mGame = gameInt
        fge.BroadcastEvent(requestMadeEvent)



        gridID = fge.GetEntities("Grid")
        grid = fge.GetGrid(gridID[0])
        recipeSize = len(grid.GetRecipe(gameInt))
        REQUEST_TIME_MAX = 17.5 * recipeSize
        REQUEST_TIME = REQUEST_TIME_MAX
        REWARD = 2.0 * recipeSize
        #for i in range(numGames):
        #    if i == selectionIndex:
        #        EntityManager.GetInstance().ToggleEntityEnable(UI_IDS[i], True)
        #    else:
        #        EntityManager.GetInstance().ToggleEntityEnable(UI_IDS[i], False)
    if(event.GetType() == "PauseEvent"):
        PAUSED = event.mPause
        
def on_update(id, dt):
    global MUSIC
    global STATE
    global PAUSED
    global MAX_TIME
    
    if (InputManager.GetInstance().IsPressed("cheat") and InputManager.GetInstance().IsTriggered("time")):
        ob = fge.GetObserver(id)
        ob.SetValue("time", MAX_TIME - 5)
    
    if (STATE == state.Gameplay and not PAUSED):
        UpdateGame(id, dt)
    elif (STATE == state.Intro):
        UpdateIntro(id, dt)
    elif (STATE == state.Ending):
        UpdateEnding(id, dt)
    

def UpdateIntro(id, dt):
    global STATE
    global CAMERA_START
    global CAMERA_END
    global TALLY

    ob = fge.GetObserver(id)
    time = ob.GetValue("time")
    time = time + dt * 0.001
    
    cameraID = CameraManager.GetInstance().GetCameraID()
    if (cameraID != -1):
        t = time
        if (t > 1.0):
            t = 1.0
        newPos = fge.lerp3(CAMERA_START, CAMERA_END, t)
        fge.GetTransform(cameraID).SetPosition(newPos[0], newPos[1], newPos[2])
    scaleVal = (fge.GetWindowWidth() / 1920.0)
    if (scaleVal == 1.0):
        scaleVal *= 0.9
    if (time > 2.0):
       	Renderer.GetInstance().RenderText("Ready?",0.45 * fge.GetWindowWidth(),0.5 * fge.GetWindowHeight(), scaleVal * 7.0, 0, 0, 0, 1.0 - ((max(min(time, 4.0), 3.0) - 3.0) / (4.0 - 3.0)))
    if (time > 4.0):
        STATE = state.Gameplay
        TALLY = 0.0
        
        AudioManager.GetInstance().Load("ModuleDeliver01.mp3", False)
        AudioManager.GetInstance().PlaySFX("ModuleDeliver01.mp3", 0.5, 0.5, 1.0, 1.0)
        
        fge.BroadcastEvent(fge.GetLevelStartEvent())
        
        pauseEvent = fge.GetPauseEvent()
        pauseEvent.mPause = False
        fge.BroadcastEvent(pauseEvent)
        
        time = 0.0
        
    ob.SetValue("time", time)

def UpdateGame(id, dt):
    global SCORE
    global METRIC
    global SCORE_TEXTURES_F
    global SCORE_TEXTURES_D
    global SCORE_TEXTURES_C
    global SCORE_TEXTURES_B
    global SCORE_TEXTURES_A
    global GRADES
    global REQUEST_TIME
    global MAX_TIME
    global STATE

    loc = LocalizationManager.GetInstance()
    rend = Renderer.GetInstance()
    ob = fge.GetObserver(id)
   
    grade = "F"
    grade_index = 0
    score_percentage = 0
    final_textureid = SCORE_TEXTURES_F[0]
    TextureA = 0
    required_score = 0

   # print(SCORE)
   # print("WT START")
   # for x in range(len(METRIC)):
   #     print(METRIC[x])
   # print("++++++++++++++")

    for i in range(len(METRIC)):
        if METRIC[i] <= SCORE:
            grade = GRADES[i]
            grade_index = i
        else:
            score_percentage = (METRIC[grade_index] - SCORE)/(METRIC[grade_index]) * 100
            required_score = METRIC[grade_index]
            n = 100 / len(SCORE_TEXTURES_F)
            for j in range(len(SCORE_TEXTURES_F)):
                if(score_percentage <= n * ( j + 1 )):
                    final_textureid = SCORE_TEXTURES_F[j]
                    break

    SCORE_TEXTURES = [SCORE_TEXTURES_D, SCORE_TEXTURES_C, SCORE_TEXTURES_B, SCORE_TEXTURES_A]
    TEX_LIST = SCORE_TEXTURES[grade_index]

    if(grade_index == len(METRIC) - 1):
        final_textureid = TEX_LIST[0]
        required_score = METRIC[grade_index]
        TextureA = 1
    elif(grade != "F"):	
        score_percentage = (SCORE - METRIC[grade_index])/(METRIC[grade_index+1] - METRIC[grade_index]) * 100
	    #print("score_percentage:", score_percentage)
	    #print("SCORE:",SCORE)
	    #print("Grade:", METRIC[grade_index])
        required_score = METRIC[grade_index + 1]
        n = 100 / len(TEX_LIST)
        for j in range(len(TEX_LIST)):
            if(score_percentage <= n * ( j + 1 )):
                final_textureid = TEX_LIST[j]
                break

    REQUEST_TIME = REQUEST_TIME - dt*.001
    
    or_time = ob.GetValue("time")
    time = or_time
    if(time < MAX_TIME and or_time + dt*.001 >= MAX_TIME):
        AudioManager.GetInstance().Load("GameFinish.mp3", False)
        AudioManager.GetInstance().PlaySFX("GameFinish.mp3", 0.05, 0.05, 1.0, 1.0)
    time = or_time + dt*.001   
    if(time - (MAX_TIME - 7.0) < 0.01 and time - (MAX_TIME - 7.0) > 0.0):
        AudioManager.GetInstance().Load("warningTimeOut.mp3", False)
        AudioManager.GetInstance().PlaySFX("warningTimeOut.mp3", 1.0, 1.0, 1.0, 1.0)

    score_str = "Score {:0.0f} {}".format(SCORE, grade)
    #rend.RenderText(score_str,-800.0,-500.0, 1.0, 1, 1, 1, 1)
    updateLevelEvent = fge.GetUpdateLevelEvent()
    updateLevelEvent.mCurrentTime = time
    updateLevelEvent.mTextureID = final_textureid
    updateLevelEvent.mScore = SCORE
    updateLevelEvent.mRequiredScore = required_score
    updateLevelEvent.mTextureA = TextureA
    fge.BroadcastEvent(updateLevelEvent)

    if(MAX_TIME >= 0.0 and time > MAX_TIME):
        pLevelCompleteEvent = fge.GetLevelCompleteEvent()
        pLevelCompleteEvent.mScore = SCORE
        fge.BroadcastEvent(pLevelCompleteEvent)
        STATE = state.Ending
        pauseEvent = fge.GetPauseEvent()
        pauseEvent.mPause = True
        fge.BroadcastEvent(pauseEvent)
        
        time = 0.0
    
    ob.SetValue("time", time)

def UpdateEnding(id, dt):
    global EXITING
    global TALLY
    global SCORE
    global METRIC
    global GRADES
    global LEVEL_NAME
    global STARTED_TALLY
    
    ob = fge.GetObserver(id)
    time = ob.GetValue("time")
    time = time + dt * 0.001
    
    pointsPerSecond = 25.0
    
    if (time + dt * 0.001 > 2.0):
        if (not STARTED_TALLY):
            STARTED_TALLY = True
            cameraID = CameraManager.GetInstance().GetCameraID()
            if (cameraID is not -1):
                windowID = fge.CreateEntity("Billboard")
                fge.SetParentID(windowID, cameraID)
                windowTransform = fge.GetRuntimeTransform(windowID)
                cameraFront = CameraManager.GetInstance().GetFront()
                cameraPos = fge.GetTransform(cameraID).GetPosition()
                windowTransform.SetPosition(cameraPos[0] + cameraFront[0], cameraPos[1] + cameraFront[1], cameraPos[2] + cameraFront[2])
                windowTransform.SetScale(0.6, 0.6, 0.6)
                windowModel = fge.GetRuntimeModel(windowID)
                windowModel.mpMaterial = ResourceManager.GetInstance().LoadMaterial("WindowBlack")

    if (time > 2.0):
        if (not EXITING):
            TALLY = TALLY + pointsPerSecond * dt * 0.001
            if (TALLY > SCORE):
                TALLY = SCORE
            if (InputManager.GetInstance().IsTriggered("Interact")):
                TALLY = SCORE
                EXITING = True
                Renderer.GetInstance().Fade(False, 1.0)
        grade = "F"
        for i in range(len(METRIC)):
            if METRIC[i] <= TALLY:
                grade = GRADES[i]
            else:
                break
        result_str = ""
        if (math.isclose(TALLY, SCORE)):
            if grade == "F" or grade == "D":
                result_str = "Fail"
            else:
                result_str = "Pass"
        score_str = "Score: {:0.0f}".format(TALLY)
        grade_str = "Grade: {}".format(grade)

        scaleVal = (fge.GetWindowWidth() / 1920.0);
        if (scaleVal == 1.0):
            scaleVal *= 0.9;
        Renderer.GetInstance().RenderText(LEVEL_NAME,0.437 * fge.GetWindowWidth(),0.7 * fge.GetWindowHeight(), scaleVal, 1, 1, 1, 1)
        Renderer.GetInstance().RenderText(score_str,0.47 * fge.GetWindowWidth(),0.55 * fge.GetWindowHeight(), scaleVal, 1, 1, 1, 1)
        Renderer.GetInstance().RenderText(grade_str,0.47 * fge.GetWindowWidth(),0.45 * fge.GetWindowHeight(), scaleVal, 1, 1, 1, 1)
        Renderer.GetInstance().RenderText(result_str,0.49 * fge.GetWindowWidth(),0.25 * fge.GetWindowHeight(), scaleVal,1, 1, 1, 1)
    if (Renderer.GetInstance().GetFadeMultiplier() <= 0.0):
        SceneManager.GetInstance().UpdateLevelData(SCORE, grade)
        AudioManager.GetInstance().StopAll()
        fge.ChangeScene("LevelScreenFinal")
    
    ob.SetValue("time", time)

def UpdatePool(Level):
    pool = []
    for x in range(0,2):
        pool.append(2* (Level - 1) + x)
        pool.append(2 * (4+(Level-1)) + x)
        pool.append(2 * (8+(Level-1)) + x)

   # for x in pool:
   #     print("POOL = ",x)

    return pool

def function(Level, diffType):
    pool = []

    if diffType == difficulty.Easy.value:
        for x in range(0,2):
            pool.append(2* (Level - 1) + x)
    elif diffType == difficulty.Medium.value:
        for x in range(0,2):
            pool.append(2* (Level - 1) + x)
        for x in range(0,2): 
            pool.append(2 * (4+(Level-1)) + x)
    elif diffType == difficulty.Hard.value or diffType == difficulty.All.value:
        for x in range(0,2):
            pool.append(2* (Level - 1) + x)
        for x in range(0,2):
            pool.append(2 * (4+(Level-1)) + x)
        for x in range(0,2):
            pool.append(2 * (8+(Level-1)) + x)

    return pool
#  ^ 
#  |             
#  |
# use weights or random function to choose levels for the pool or return the index
