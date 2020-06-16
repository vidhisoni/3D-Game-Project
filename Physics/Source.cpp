#include <Gear.h>

class Source : public Engine
{
public:
	Source() : Engine("PhysicsScene", true)
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