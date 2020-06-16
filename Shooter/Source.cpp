#include <Gear.h>



class Source : public Engine
{
public:
	Source() : Engine("Test", true)
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