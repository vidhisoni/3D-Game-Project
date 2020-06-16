#include "pch.h"
#include "Managers/Log.h"
#include "Core.h"
#include "JsonData.h"

JsonData::JsonData(std::string a_name, std::string a_path, bool a_isConfig) : Resource(a_name)
{
	mPath = a_path;
	misConfig = a_isConfig;
}

JsonData::~JsonData()
{

}

void JsonData::Load()
{
	// Don't load if resource is already loaded
	if (!mLoadFailed)
		return;

	mLoadFailed = false;

	if (!misConfig) {
		// Load Json Text into String
		std::ifstream file(mPath + mName + ".json");
		std::string fileString;
		std::getline(file, fileString, (char)EOF);
		file.close();

		// Create Json Reader
		Json::CharReaderBuilder builder;
		Json::CharReader* reader = builder.newCharReader();

		// Parse Json String
		std::string errorString;
		if (!reader->parse(fileString.c_str(), fileString.c_str() + fileString.size(), &mRoot, &errorString)) {
			LOG_ERROR("Failed to load JsonData " + mName + ": " + errorString);
			mLoadFailed = true;
		}
	}
	else
	{
		std::ifstream file(mPath);
		std::string fileString;
		std::getline(file, fileString, (char)EOF);
		file.close();

		// Create Json Reader
		Json::CharReaderBuilder builder;
		Json::CharReader* reader = builder.newCharReader();

		// Parse Json String
		std::string errorString;
		if (!reader->parse(fileString.c_str(), fileString.c_str() + fileString.size(), &mRoot, &errorString)) {
			LOG_ERROR("Failed to load JsonData " + mName + ": " + errorString);
			mLoadFailed = true;
		}
	}
}