#include <Gear.h>



class Source : public Engine
{
public:
	Source() : Engine("SplashSequence", false)
	{
 	}

	~Source()
	{

	}
};

Engine* CreateApplication()
{
	return new Source;
}