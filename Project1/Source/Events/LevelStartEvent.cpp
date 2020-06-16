#include "pch.h"
#include "Managers/Log.h"
#include "Core.h"
#include "LevelStartEvent.h"

LevelStartEvent::LevelStartEvent() : Event("LevelStartEvent")
{

}

LevelStartEvent::~LevelStartEvent()
{

}

LevelStartEvent* LevelStartEvent::Create()
{
	return new LevelStartEvent();
}
