#include "pch.h"
#include "SceneManager.h"
#include "EntityManager.h"
#include "ComponentManager.h"
#include "ObjectFactory.h"
#include "ResourceManager.h"
#include "MemoryManager.h"
#include "InputManager.h"
#include "EventManager.h"
#include "Engine.h"
#include "Components/UIComponent.h"
#include "Resources/JsonData.h"
#include "Managers/Log.h"
#include "Resources/Text.h"
#include "Managers/InputManager.h"
#include "Managers/Renderer.h"
#include "Events/RequestFilledEvent.h"
#include "Events/ResetGridEvent.h"


#include <winerror.h> //for HRESULT
#include <comdef.h>     // Added
#include <comutil.h> //for _bstr_t (used in the string conversion)
#include "shlobj.h"
#include "atlbase.h"
#include "atlstr.h"


SceneManager* SceneManager::mInstance = nullptr;

void SceneManager::Update()
{

	mScreenHeight = Engine::GetInstance()->mWindowHeight;
	mScreenWidth = Engine::GetInstance()->mWindowWidth;

	if (InputManager::GetInstance()->IsTriggered("start"))
	{
		std::string current = GetCurrent();
		if ((current == "DigiPen01Level" ||
			current == "DigiPen02Level" ||
			current == "DigiPen03Level" ||
			current == "DigiPen04Level" ||
			current == "DigiPen05Level" ||
			current == "Coffee01Level" ||
			current == "Coffee02Level" ||
			current == "Coffee03Level" ||
			current == "Coffee04Level" ||
			current == "Coffee05Level" ||
			current == "Needle01Level" ||
			current == "Needle02Level" ||
			current == "Needle03Level" ||
			current == "Needle04Level" ||
			current == "Needle05Level" ||
			current == "LevelScreenFinal") && RENDERER->GetFadeMultiplier() >= 1.0f) {
			std::string menuString = "PauseMenu";
			if (current == "LevelScreenFinal")
				menuString = "MapPauseMenu";
			PauseEvent* pPauseEvent = static_cast<PauseEvent*>(MEMORY_MANAGER->GetEventFromMemory("PauseEvent"));
			pPauseEvent->mPause = true;
			EVENT_MANAGER->BroadcastEvent(pPauseEvent);
			PushScene(menuString);
			ObjectFactory::GetInstance()->LoadLevel(menuString);
		}
		else if (current == "PauseMenu" || current == "MapPauseMenu") {
			SCENE_MANAGER->ClearLevel(current);
			PauseEvent* pPauseEvent = static_cast<PauseEvent*>(MEMORY_MANAGER->GetEventFromMemory("PauseEvent"));
			pPauseEvent->mPause = false;
			EVENT_MANAGER->BroadcastEvent(pPauseEvent);
		}
		/*else if(mSceneStack.front() == "DigiPenLevel")
		{
			PushScene("PauseMenu");
			ObjectFactory::GetInstance()->LoadLevel("PauseMenu");
		}
		else
		{
			ClearLevel(mSceneStack.front());
		}*/
	}

	if (INPUT_MANAGER->IsPressed(SDL_SCANCODE_LCTRL) && INPUT_MANAGER->IsTriggered(SDL_SCANCODE_W))
	{
		Cheats(mWorldID);
	}
	if (INPUT_MANAGER->IsPressed(SDL_SCANCODE_LCTRL) && INPUT_MANAGER->IsTriggered(SDL_SCANCODE_A))
	{
		Cheats(mWorldID,true);
	}
	if (INPUT_MANAGER->IsPressed(SDL_SCANCODE_LCTRL) && INPUT_MANAGER->IsTriggered(SDL_SCANCODE_C))
	{
		std::vector<Entity*> grids = ENTITY_MANAGER->GetEntities("Grid");
		for (Entity* pGridEntity : grids) {
			std::vector<int> children = ENTITY_MANAGER->GetEntity(pGridEntity->GetID())->GetChildIDs();
			for (int i = 0; i < children.size(); ++i) {
				Entity* pChild = ENTITY_MANAGER->GetEntity(children[i], true);
				pChild->SetAllEnabled(false);
			}
		}

		RequestFilledEvent* reqFilled = static_cast<RequestFilledEvent*>(MEMORY_MANAGER->GetEventFromMemory("RequestFilledEvent"));
		EventManager::GetInstance()->BroadcastEvent(reqFilled);
	}

}

GEAR_API void SceneManager::LoadScene(std::string aScene)
{
	if (mScenes.find(aScene) == mScenes.end())
		mScenes.emplace(aScene, std::list<int>());
}

void SceneManager::LoadActionScene(std::string aActionScene)
{
	//ClearLevel(GetCurrent());
	mCurrentLevel = aActionScene;
	PushScene(mCurrentLevel);
	ObjectFactory::GetInstance()->LoadLevel(mCurrentLevel);
}

void SceneManager::PushScene(std::string aLevel)
{
	if (mScenes.find(aLevel) == mScenes.end()) 
		LoadScene(aLevel);
	/*if (mSceneStack.size() > 0) {
		mSceneStack.pop_front();
	}*/
	mSceneStack.push_front(aLevel);

}

void SceneManager::SwapScene(std::string aLevel)
{
	if (mScenes.find(aLevel) == mScenes.end())
		LoadScene(aLevel);
	if (mSceneStack.size() > 0) {
		//reset level
		mSceneStack.pop_front();
	}
	mSceneStack.push_front(aLevel);
}

int SceneManager::PopScene()
{
	mSceneStack.pop_front();
	return -1;
}

GEAR_API std::list<int> SceneManager::PeekScene()
{
	std::string sceneName = GetCurrent();
	std::list<int> sceneIds;
	if (mScenes.find(sceneName) != mScenes.end())
		sceneIds = mScenes.at(sceneName);
	return sceneIds;
}

GEAR_API int SceneManager::AddEntity(int aId, std::string a_scene)
{
	std::string sceneName = a_scene;
	if (a_scene.empty()) 
		sceneName = GetCurrent();
	
	if (mScenes.find(sceneName) != mScenes.end()) {
		mScenes.at(sceneName).push_back(aId);
		return 1;
	} 
	else
		return 0;
}

GEAR_API int SceneManager::RemoveEntity(int aId)
{
	std::string sceneName = GetCurrent();

	std::list<int> sceneIds;
	if (mScenes.find(sceneName) != mScenes.end()) {
		mScenes.at(sceneName).erase(std::remove(mScenes.at(sceneName).begin(), mScenes.at(sceneName).end(), aId), mScenes.at(sceneName).end());
		return 1;
	}
	return 0;
}

GEAR_API std::string SceneManager::GetCurrent()
{
	std::string current = "";
	if (mSceneStack.size() > 0)
		current = mSceneStack.front();
	return current;
}

SceneManager::SceneManager() : mSceneID(-1)
{
}


SceneManager::~SceneManager()
{
}

SceneManager * SceneManager::GetInstance()
{
	if (!mInstance)
		mInstance = new SceneManager();
	return mInstance;
}

GEAR_API void SceneManager::Init()
{
	if (!mInstance)
		mInstance = new SceneManager();
	
	ReadLevelData();
	SetColor();
	mScreenHeight = Engine::GetInstance()->mWindowHeight;
	mScreenWidth = Engine::GetInstance()->mWindowWidth;
	mCompletedWorld = 0;

}

void SceneManager::Cleanup()
{
	WriteDataToSaveFile();
	delete mInstance;
}

std::vector<LevelData>* SceneManager::GetLevelData()
{
	return &mLevelData;
}

std::unordered_map<char, glm::vec3> SceneManager::GetColorData()
{
	return mGradeColor;
}

GEAR_API void SceneManager::ReadLevelData()
{
	LPWSTR wszPath = NULL;
	HRESULT hr;
	hr = SHGetKnownFolderPath(FOLDERID_Documents, KF_FLAG_CREATE, NULL, &wszPath);

	if (SUCCEEDED(hr)) {
		_bstr_t bstrPath(wszPath);
		mFilePath = std::string((char*)bstrPath) + "\\ShipIT\\";
		CreateDirectory(mFilePath.c_str(), NULL);
		mFilePath += "UnlockLevelData.txt";
	}

	Text* pLevelText;
	std::ifstream cfile(mFilePath);
	
	if (!cfile.good()) {	//Deafault Save File read
		pLevelText = RESOURCE_MANAGER->LoadText("UnlockLevelData", false);
	}
	else {					// Read file from user/documents
		pLevelText = RESOURCE_MANAGER->LoadText("UnlockLevelData", true, mFilePath);
	}

	std::string sdata;
	int i = 1;
	while (std::getline(pLevelText->mFileStream, sdata)) {

		std::istringstream stringStream(sdata);
		//std::pair<bool, std::pair<int,int>> data;

		std::string worldNum;
		std::getline(stringStream, worldNum, ',');

		std::string levelName;
		std::getline(stringStream, levelName, ',');

		std::string isUnlock;
		std::getline(stringStream, isUnlock, ',');
		const char *temp = isUnlock.c_str();

		//2 players
		std::string unlockScore2;
		std::getline(stringStream, unlockScore2, ',');

		//3 players
		std::string unlockScore3;
		std::getline(stringStream, unlockScore3, ',');

		//4 players
		std::string unlockScore4;
		std::getline(stringStream, unlockScore4, ',');

		std::string scoreData;
		std::getline(stringStream, scoreData, ',');

		std::string grade;
		std::getline(stringStream, grade, ',');
		char g = grade[0];

		bool unlock = temp[0] == 'Y' ? true : false;

		LevelData data(std::stoi(worldNum), levelName, i, unlock, 
			std::stoi(unlockScore2), std::stoi(unlockScore3), std::stoi(unlockScore4), std::stoi(scoreData), g);
		mLevelData.push_back(data);
		i++;
	}

	pLevelText->mFileStream.clear();
	pLevelText->mFileStream.seekg(0, std::ios::beg);
}

GEAR_API void SceneManager::WriteDataToSaveFile()
{
	std::ofstream savefile;
	savefile.open(mFilePath);

	std::vector<LevelData> *levelData = GetLevelData();

	for (LevelData &element : *levelData)
	{
		savefile << element.worldNumber << ",";
		savefile << element.LevelName << ",";
		char temp = element.isUnlocked == true ? 'Y' : 'N';
		savefile << temp << ",";
		savefile << element.scoreToUnlock_2Players << ",";
		savefile << element.scoreToUnlock_3Players << ",";
		savefile << element.scoreToUnlock_4Players << ",";
		savefile << element.highScore << ",";
		savefile << element.grade << "\n";
	}
	savefile.close();
}

void SceneManager::SetColor()
{
	mGradeColor.insert({ 'A', glm::vec3(255,223,0) });
	mGradeColor.insert({ 'B', glm::vec3(173,204,255) });
	mGradeColor.insert({ 'C', glm::vec3(202,56,8) });
	mGradeColor.insert({ 'D', glm::vec3(68,68,68) });
	mGradeColor.insert({ 'F', glm::vec3(68,68,68) });


}

void SceneManager::SetWorldID(int aWorldID)
{
	mWorldID = aWorldID;
}

void SceneManager::Cheats(int worldID, bool aAll)
{
	std::vector<LevelData> *levelData = GetLevelData();

	bool once = true;
	for (LevelData &element : *levelData)
	{
		if (!aAll) {
			if (element.worldNumber == mWorldID)
			{
				element.isUnlocked = true;
				element.grade = element.grade == 'X' ? 'F' : element.grade;
			}
			if (element.worldNumber == mWorldID + 1 && once)
			{
				element.isUnlocked = true;
				element.grade = element.grade == 'X' ? 'F' : element.grade;
				once = false;
			}
		}
		else {
			element.isUnlocked = true;
			element.grade = element.grade == 'X' ? 'F' : element.grade;
		}
	}
}

void SceneManager::UpdateLevelData(float a_Score, std::string a_Grade)
{
	std::string temp = GetCurrent();
	int length = temp.length();
	std::string CompletedLevel = temp.substr(0, length - 5);

	std::vector<LevelData> *levelData = GetLevelData();

	for (LevelData &element : *levelData)
	{

		if (element.LevelName.compare(CompletedLevel) == 0)
		{
			if (element.highScore < a_Score) {
				element.highScore = (int)a_Score;
				element.grade = a_Grade[0];
			}
		}
	}
}

void SceneManager::ClearLevel(std::string a_SceneName)
{
	std::list<int> sceneIds;

	std::unordered_map<std::string, std::list<int>>::iterator sceneItr = mScenes.find(a_SceneName);
	if (sceneItr != mScenes.end()) {
		sceneIds = mScenes.at(a_SceneName);
		std::list<int>::iterator begin = sceneIds.begin();
		std::list<int>::iterator end = sceneIds.end();
		for (std::list<int>::iterator itr = begin; itr != end; ++itr)
		{
			ENTITY_MANAGER->DeleteEntity(*itr);
		}
		mScenes.erase(sceneItr);
		mSceneStack.remove(a_SceneName);
	}
}

void SceneManager::ClearAll()
{
	std::list<std::string> tempScenes = mSceneStack;
	for (std::list<std::string>::iterator itr = tempScenes.begin(); itr != tempScenes.end(); ++itr)
	{
		ClearLevel(*itr);
	}
}
