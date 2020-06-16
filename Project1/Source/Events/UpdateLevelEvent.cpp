#include "pch.h"
#include "Managers/Log.h"
#include "Core.h"
#include "UpdateLevelEvent.h"

UpdateLevelEvent::UpdateLevelEvent() : Event("UpdateLevelEvent")
{
	mCurrentTime = 0.0f;
		mTextureID = 0;
	mScore = 0;
	mRequiredScore = 0;
	mTextureA = false;
}

UpdateLevelEvent::~UpdateLevelEvent()
{

}

void UpdateLevelEvent::Reset()
{
	mCurrentTime = 0.0f;
	mTextureID = 0;
	mScore = 0;
	mRequiredScore = 0;
	mTextureA = false;
	Event::Reset();
}

UpdateLevelEvent* UpdateLevelEvent::Create()
{
	return new UpdateLevelEvent();
}