#pragma once

#define OBJECT_FACTORY ObjectFactory::GetInstance()

/*!
 * Loads and saves levels
 * 
 */
class ObjectFactory
{
public:
	/*!
	 * Get the ObjectFactory Singleton
	 * reference
	 * 
	 * \return The ObjectFactory reference
	 */
	GEAR_API static ObjectFactory* GetInstance();
	/*!
	 * Adds the specified level to the queue of levels to load
	 * 
	 * \param a_fileName The name of the level file to be loaded
	 */
	GEAR_API void LoadLevel(std::string a_fileName);
	/*!
	 * Loads the levels in the load queue
	 *
	 */
	GEAR_API void LoadLevelQueue();
	/*!
	 * Loads Entities specified in the given root
	 *
	 * \param a_root The root that specifies the Entities to be loaded
	 * \param a_isRuntime A flag indicating whether or not the Entity is being serialized during runtime
	 */
	GEAR_API std::vector<int> LoadEntities(Json::Value a_root, bool a_isRuntime, std::string a_scene= "");
	/*!
	 * Saves the level into the specified
	 * file
	 * 
	 * \param a_fileName The name of the file that the level is being saved to
	 */
	GEAR_API void SaveLevel(std::string a_fileName);
	/*!
	 * Deletes the ObjectFactory Singleton
	 * 
	 */
	GEAR_API void Cleanup();

private:
	GEAR_API ObjectFactory();
	GEAR_API ~ObjectFactory();
	GEAR_API void LoadInnerReferences(bool a_isRuntime);

private:
	static ObjectFactory* mInstance;

	std::queue<std::string> mLoadQueue;
public:
	std::string mCurrentLevel;
};