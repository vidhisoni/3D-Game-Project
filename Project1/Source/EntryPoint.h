#pragma once
#include <Windows.h>

#ifdef GEAR_PLATFORM_WINDOWS

extern Engine* CreateApplication();
#undef main
int WINAPI wWinMain(_In_ HINSTANCE hInstance, _In_opt_ HINSTANCE hPrevInstance, _In_ LPWSTR lpCmdLine, _In_ int nCmdShow)
//int main()
{
	auto app = CreateApplication();
	app->Run();
	app->Close();
	delete app;
	return 0;
}

#endif