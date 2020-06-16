#pragma once

#include "Component.h"

class Audio;

enum UIType
{
	INVALID = -1,
	IMAGE,
	BUTTON,
	RADIOBUTTON,
	SLIDER,
	TEXT,
	SCORE_IMAGE
};

struct UIData
{
	UIType sType;
	glm::vec3 sTransform;
	glm::vec3 sScale;
	std::string sButtonLabel;
	std::string sButtonAction;
	std::string sRadioButtonLabel;
	std::vector<std::string> sRadioButtonOptions;
	std::string sSliderLabel;
	std::string sTextString;
	int sRadioButtonSelected;
	int sSliderValue;
	int sMinNum, sMaxNum;
	std::string sImageDescription;
	UIData() {
		sType = INVALID, sTransform = glm::vec3(0), sScale = glm::vec3(0), sMinNum = 0, sMaxNum = 0; sRadioButtonSelected = 0; }
};

class UIComponent : public Component
{
public:
	GEAR_API UIComponent();
	GEAR_API ~UIComponent() override;

	GEAR_API void Init() override;
	GEAR_API void Reset() override;
	GEAR_API UIComponent* Create() override;
	GEAR_API void Update(float a_deltaTime) override;
	GEAR_API void DisplayDebug() override;
	GEAR_API void HandleEvent(Event* a_pEvent) override;
	GEAR_API void Serialize(Json::Value a_root) override;
	GEAR_API void DeSerialize(Json::Value& a_root, bool a_ignoreDefault = false) override{}
	GEAR_API void Clone(int objID) override;
	GEAR_API std::vector<std::string> GetOptions() { return mData.sRadioButtonOptions; }
	GEAR_API int GetSliderValue() { return mData.sSliderValue; }
	GEAR_API std::string GetLabel() {
		if (mData.sType == RADIOBUTTON)
			return mData.sRadioButtonLabel;
		if (mData.sType == SLIDER)
			return mData.sSliderLabel;
		return mData.sButtonLabel; 
	}
	GEAR_API std::string GetAction() { return mData.sButtonAction; }
	GEAR_API void SetSliderValue(int a_s) 
	{  
		if (a_s > mData.sMaxNum)
			a_s = mData.sMaxNum;
		if (a_s < mData.sMinNum)
			a_s = mData.sMinNum;
		mData.sSliderValue = a_s; 
	}
	GEAR_API std::string GetType() { 
		switch (mData.sType) {
		case INVALID:
			return "INVALID";
		case IMAGE:
			return "IMAGE";
		case BUTTON:
			return "BUTTON";
		case RADIOBUTTON:
			return "RADIOBUTTON";
		case SLIDER:
			return "SLIDER";
		case TEXT:
			return "TEXT";
		}
	}
private:
	void SetupLevel(std::string a_levelName);

public:
	UIData mData;
	float mTimer, mInitialTime;
	float mScaleFactor;
	glm::vec3 mSliderPosition;


	Audio* mAudio;

	bool mIsSelected;
	bool mIsPressed;
	int mSelectId;
	int mMenuIndex;
	//Test
	std::string originalLabel;
	std::string tempLabel;
	std::string mLevelName;
	int mHighScore;
	bool mIsLevelButton;
	bool mIsUnlocked;
	int mLevelNumber;
	int mUnlockScore;
	unsigned int mTextureid;
	int mScore_;
	int mRequiredScore_;
	bool mTextureA;
};