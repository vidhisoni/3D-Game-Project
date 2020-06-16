#include <Gear.h>



class Source : public Engine
{
public:
	Source() : Engine("BaseFightLevel", false)
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