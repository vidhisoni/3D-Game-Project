#include "pch.h"
#include "Managers/Log.h"
#include "Core.h"
#include "Text.h"
#include "Managers/SceneManager.h"

///
#include <winerror.h> //for HRESULT
#include <comdef.h>     // Added
#include <comutil.h> //for _bstr_t (used in the string conversion)
#include "shlobj.h"
#include "atlbase.h"
#include "atlstr.h"
//


Text::Text(std::string a_name, bool a_isReadOnly, std::string a_FilePath) : Resource(a_name)
{
	//misSystemPath = a_SystemPath;

	mFilePath = a_FilePath;
	misReadOnly = a_isReadOnly;
}

Text::~Text()
{
	if (!mLoadFailed)
		mFileStream.close();
}

void Text::Load()
{
	// Don't load if resource is already loaded
	if (!mLoadFailed)
		return;

	mLoadFailed = false;

	if (!misReadOnly) {
		mFileStream.open(mFilePath + mName + ".txt", std::fstream::in);
	}
	else {
		mFileStream.open(mFilePath);
	}

	if (!mFileStream) {
		LOG_ERROR("Failed to load Text " + mName + ".txt");
		mLoadFailed = true;
	}
}