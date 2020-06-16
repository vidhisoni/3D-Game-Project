#pragma once
#include "Event.h"

/*!
 * An event for when a Level has started
 *
 */
class LevelStartEvent : public Event
{
public:
	/*!
	 * LevelStartEvent Default Constructor
	 *
	 */
	GEAR_API LevelStartEvent();
	/*!
	 * LevelStartEvent Default Destructor
	 *
	 */
	GEAR_API ~LevelStartEvent();
	/*!
	 * Creates a pointer to a new LevelStartEvent
	 *
	 * \return A pointer to a new LevelStartEvent
	 */
	GEAR_API virtual LevelStartEvent* Create();
};

