import fge
from fge import Mouse
from fge import Controller
from fge import UIComponent
from fge import UIActionEvent

global currentIndex
global prevIndex

def on_init(id):
    global currentIndex 
    global prevIndex 
    prevIndex = 0
    currentIndex = 0

def on_event(id,event):
    pass

def on_update(id, dt):
    global prevIndex
    global currentIndex
    mouse = Mouse.GetInstance()
   
    if(mouse.MouseDeltaX() == 0 and mouse.MouseDeltaY() == 0):
        ui_items = fge.GetChildren(id, "UI")
        if(currentIndex < 0):
            for i in range(len(ui_items)): 
                u = fge.GetUIComponent(ui_items[i])
                if(u.mIsSelected):
                    currentIndex = i 
                    break
            for i in range(len(ui_items)): 
                u = fge.GetUIComponent(ui_items[i])
                if(currentIndex != i):
                    u.mIsSelected = False   
        if(currentIndex < 0):
            currentIndex = prevIndex
        con = fge.GetController(id)
        if (currentIndex >= len(ui_items)):
            currentIndex = 0
        ui = fge.GetUIComponent(ui_items[currentIndex])
        if(con.IsTriggered("down")):
            currentIndex += 1
            if(currentIndex > len(ui_items) - 1):
                currentIndex = len(ui_items)  - 1
            ui.mIsSelected = False
        if(con.IsTriggered("up")):
            currentIndex -= 1
            if(currentIndex < 0):
                currentIndex = 0
            ui.mIsSelected = False
        new_ui = fge.GetUIComponent(ui_items[currentIndex])
        new_ui.mIsSelected = True
        ui = new_ui
        if(ui.GetType() == "RADIOBUTTON"):
            options = ui.GetOptions()
            r_index = ui.mSelectId
            if(con.IsTriggered("left")):
                r_index -= 1
            elif(con.IsTriggered("right")):
                r_index += 1
            if(r_index >= 0 and r_index  < len(options)):
                ui.mSelectId = r_index
            elif(r_index < 0):
                ui.mSelectId = 0
            else:
                ui.mSelectId = len(options)-1
            if(con.IsTriggered("Interact")):
                pUIEvent = fge.GetUIActionEvent()
                pUIEvent.mDescription = ui.GetLabel()
                pUIEvent.mOwnerId = ui.GetOwnerID()
                pUIEvent.mData =  options[ui.mSelectId]
                fge.BroadcastEvent(pUIEvent)
           
        elif(ui.GetType() == "SLIDER"):
            val = ui.GetSliderValue()
            val_changed = False
            if(con.IsPressed("left")):
                val_changed = True
                val -= 1
            elif(con.IsPressed("right")):
                val_changed = True
                val += 1
            if(val_changed):
                ui.SetSliderValue(val)
                pUIEvent = fge.GetUIActionEvent()
                pUIEvent.mDescription = "Volume"
                pUIEvent.mOwnerId = ui.GetOwnerID()
                fge.BroadcastEvent(pUIEvent)               
        elif(con.IsTriggered("Interact")):#item is a button
            pUIEvent = fge.GetUIActionEvent()
            pUIEvent.mDescription = ui.GetLabel()
            pUIEvent.mOwnerId = ui.GetOwnerID()
            fge.BroadcastEvent(pUIEvent)
        prevIndex = currentIndex
    else:
        if(currentIndex >= 0):
            ui_items = fge.GetChildren(id, "UI")
            ui = fge.GetUIComponent(ui_items[currentIndex])
            ui.mIsSelected = False
            prevIndex = currentIndex
            currentIndex = -1
