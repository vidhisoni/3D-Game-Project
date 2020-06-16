#include "pch.h"
#include "Managers/Log.h"
#include "Core.h"
#include "ObjectFactory.h"
#include "Component.h"
#include "ResourceManager.h"
#include "MemoryManager.h"
#include "EventManager.h"
#include "Renderer.h"
#include "InputManager.h"
#include "../Resources/JsonData.h"
#include "ComponentManager.h"
#include "EntityManager.h"
#include "SceneManager.h"
#include "../Engine.h"
#include "Entity.h"
#include "Renderer.h"
#include "Editor/LevelEditor.h"
#include "Events/InitLevelEvent.h"
#include "Utility.h"
#include "../Resources/Texture.h"

ObjectFactory* ObjectFactory::mInstance = nullptr;

ObjectFactory::ObjectFactory()
{

}

ObjectFactory::~ObjectFactory()
{

}

void ObjectFactory::LoadLevel(std::string a_fileName)
{
	mLoadQueue.push(a_fileName);

	mCurrentLevel = a_fileName;
}

void ObjectFactory::LoadLevelQueue()
{
	bool somethingToLoad = !mLoadQueue.empty();

	while (!mLoadQueue.empty()) {
		std::string fileName = mLoadQueue.front();

		InitLevelEvent* initLevelEvent = nullptr;
		Json::Value levelDataRoot;
		std::vector<std::string> levelNames = GetUniqueDirectoryFiles(".\\Resources\\LevelData\\");
		if (std::find(levelNames.begin(), levelNames.end(), fileName) != levelNames.end()) {
			levelDataRoot = RESOURCE_MANAGER->LoadJsonData(fileName, ".\\Resources\\LevelData\\")->mRoot;
			initLevelEvent = static_cast<InitLevelEvent*>(MEMORY_MANAGER->GetEventFromMemory("InitLevelEvent"));			

			Json::Value levelData = levelDataRoot["LevelFile"];
			if (!levelData.isNull())
				fileName = levelData.asString();
		}

		// Get level json root
		Json::Value root = ResourceManager::GetInstance()->LoadJsonData(fileName, "./Resources/Level/")->mRoot[fileName];
		// Check if root is empty
		if (root.isNull()) {
			LOG_ERROR("Failed to load level " + fileName);
			return;
		}

		std::vector<int> childIDs = LoadEntities(root, false, fileName);
		for (int ids : childIDs) {
			std::vector<Component*> components = COMPONENT_MANAGER->GetComponents(ids, true);

			for (Component* compo : components)
				compo->Init();
		}

		// If level is from one of the worlds, send init level event

		if (initLevelEvent) {
			ENTITY_MANAGER->ClearRuntimeLists();
			COMPONENT_MANAGER->ClearRuntimeLists();

			Json::Value levelData = levelDataRoot["Name"];
			if (!levelData.isNull())
				initLevelEvent->mLevelName = levelData.asString();

			levelData = levelDataRoot["Music"];
			if (!levelData.isNull())
				initLevelEvent->mMusic = levelData.asString();

			levelData = levelDataRoot["Time"];
			if (!levelData.isNull())
				initLevelEvent->mTime = levelData.asFloat();

			levelData = levelDataRoot["Difficulty"];
			if (!levelData.isNull())
				for (unsigned int i = 0; i < levelData.size(); ++i)
					initLevelEvent->mGames.push_back(levelData[i].asInt());

			// Get the number of players
			int numPlayers = 2;
			int numControllers = int(INPUT_MANAGER->GetPlayerGamePads().size());
			if (numControllers > 2)
				numPlayers = numControllers;

			levelData = levelDataRoot["Level Number"];
			if (!levelData.isNull())
				initLevelEvent->mLevelNumber = levelData.asInt();

			levelData = levelDataRoot["Grading"];
			if (!levelData.isNull()) {
				Json::Value grades = levelData[numPlayers - 2];
				for (unsigned int i = 0; i < grades.size(); ++i)
					initLevelEvent->mGrading.push_back(grades[i].asFloat());

			}
			
			levelData = levelDataRoot["Score Textures"];
			if (!levelData.isNull()) {
				Json::Value textures = levelData;
				for (unsigned int i = 0; i < textures.size(); ++i)
				{
					std::vector<unsigned int>* textureArray;
					if (i == 0)
					{
						textureArray = &initLevelEvent->mScoreTexturesF;
					}
					else if (i == 1)
					{
						textureArray = &initLevelEvent->mScoreTexturesD;
					}
					else if (i == 2)
					{
						textureArray = &initLevelEvent->mScoreTexturesC;
					}
					else if (i == 3)
					{
						textureArray = &initLevelEvent->mScoreTexturesB;
					}
					else
					{
						textureArray = &initLevelEvent->mScoreTexturesA;
					}
					for (unsigned int j = 0; j < textures[i].size(); ++j)
					{
						Texture* pTexture = RESOURCE_MANAGER->LoadTexture(textures[i][j].asString());
						textureArray->push_back(pTexture->mTextureID);
					}
				}
			}
			initLevelEvent->mNumPlayers = numPlayers;

			EVENT_MANAGER->BroadcastEvent(initLevelEvent);

			//RENDERER->Fade(true, 1.0f);
		}

		mLoadQueue.pop();
	}

	if (somethingToLoad && RENDERER->GetFadeMultiplier() < 1.0f)
		RENDERER->Fade(true, 1.0f);

	ENTITY_MANAGER->ClearRuntimeLists();
	COMPONENT_MANAGER->ClearRuntimeLists();
}

std::vector<int> ObjectFactory::LoadEntities(Json::Value a_root, bool a_isRuntime, std::string a_scene) {
	std::vector<int> newIDs;
	// Load and reserialize  entities
	for (size_t i = 0; i < a_root.size(); ++i) {
		// Get current entity root
		Json::Value entityRoot = a_root[int(i)];

		// Check if data file exists
		Json::Value dataFile = entityRoot["DataFile"];
		if (!dataFile.isNull()) {
			Entity* pNewEntity;
			if (a_isRuntime) {
				pNewEntity = EntityManager::GetInstance()->CreateRuntimeEntity(dataFile.asString(), a_scene);
			}
			else {
				pNewEntity = EntityManager::GetInstance()->CreateEntity(dataFile.asString(), a_scene);
				SCENE_MANAGER->AddEntity(pNewEntity->GetID(), a_scene);
			}
			newIDs.push_back(pNewEntity->GetID());
			// Reserialize new object
			std::vector<int> childIDs = pNewEntity->Serialize(entityRoot, a_isRuntime, a_scene);
			// It turns out the parent entity doesn't have a Transform at the moment
			// the child is initializing their component.  So when the child calls OnSetParent(),
			// there is no parent transform to use.
			// This change makes it so that after the parent's transform has been created,
			// all the children will need to recompute their transform due to their dirty bit being set.
			for (int i = 0; i < childIDs.size(); ++i) {
				Entity* pChildEntity = ENTITY_MANAGER->GetEntity(childIDs[i], true);
				if (!pChildEntity)
					pChildEntity = ENTITY_MANAGER->GetRuntimeEntity(childIDs[i]);
				if (pChildEntity)
					pChildEntity->SetParentID(pNewEntity->GetID(), false);
			}

			Json::Value dataRoot = entityRoot["IsEnabled"];
			if (!dataRoot.isNull())
				if (pNewEntity->IsEnabled() != dataRoot.asBool())
					ENTITY_MANAGER->EntityEnable(pNewEntity->GetID(), dataRoot.asBool());
			// Reserialize new object's components
			std::vector<Component*> entityComponentList;
			if (a_isRuntime)
				entityComponentList = ComponentManager::GetInstance()->GetRuntimeComponents(pNewEntity->GetID());
			else
				entityComponentList = ComponentManager::GetInstance()->GetComponents(pNewEntity->GetID(), true);
			for (Component* pComponent : entityComponentList)
				pComponent->Serialize(entityRoot[pComponent->GetType()]);
		}
	}

	return newIDs;
}

void ObjectFactory::SaveLevel(std::string a_fileName)
{
// 	// TODO: Implement
	Json::StreamWriterBuilder streamBuilder;
	Json::StreamWriter* writer = streamBuilder.newStreamWriter();
	Json::Value root;

	Json::Value objects(Json::arrayValue);
	int i = 0;
	for (std::pair<int, Entity*> element : ENTITY_MANAGER->mEntityMap) {
		if (element.second) {
			if (element.second->GetParentID() == -1
				&& std::find(LEVEL_EDITOR->mRunTimeTimeList.begin(), LEVEL_EDITOR->mRunTimeTimeList.end(), element.second->GetID()) == LEVEL_EDITOR->mRunTimeTimeList.end()) {
				Json::Value object;
				object["DataFile"] = element.second->GetDataFile();
				element.second->DeSerialize(object);
				objects.append(object);
				i++;
			}
		}
	}
	root[a_fileName] = objects;
	//Deserializer
	std::ofstream output("Resources/Level/" + a_fileName + ".json");
	writer->write(root, &output);
	output.close();

	RESOURCE_MANAGER->ReloadJsonData(a_fileName);
}

void ObjectFactory::LoadInnerReferences(bool a_isRuntime)
{

	std::vector<Component*> components;
	if (a_isRuntime)
		components = COMPONENT_MANAGER->GetAllRuntimeComponents();
	else
		components = COMPONENT_MANAGER->GetAllComponents(true);

	for (Component* com : components)
	{
		com->Init();// initialize position and prevPosition, invMass
	}
}

ObjectFactory* ObjectFactory::GetInstance()
{
	if (!mInstance)
		mInstance = new ObjectFactory();

	return mInstance;
}

void ObjectFactory::Cleanup()
{
	delete mInstance;
	mInstance = nullptr;
}