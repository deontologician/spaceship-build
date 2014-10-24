# spaceship-build

## Incredibly detailed spaceship engineering sim

Build a spaceship with a dwarf-fortress level of attention to detail.
This involves making engineering tradeoffs and doing testing to determine if your ship will catastrophically fail in space or survive a firefight.

## How to run the game

```bash
$ python spaceship.py
```

## Concepts

Things you may have to consider:

* Do I have a large enough power core to supply power to all of my spaceship's components?
* What about under load?
* Are the guns being adequately cooled?
* Are the coolant conduits receiving adequate radiation shielding from the power core?

There will also be an in flight component where you use your ship and find out if it's adequate. During battles, you may have damage to the ship and need to compensate.

* Luckily I built in redundant communication buses, so I can still communicate with my engines
* The power core is damaged and only outputting 50% capacity. I'll need to power down some non-essential components.
* Our shield array is not protecting us enough. I'll push it beyond its stated limits hoping we can get out of this fight before it overloads.

The idea of the game is to have you build the ship basically from scratch.
You may have to test each component you build carefully since there aren't easy summary numbers that can tell you whether you've built it correctly.
The emergent properties of the game rules determine suitability, and you must engineer around them.
In other words, if you want to find out if your gun overloads your power supply when it's being fired, test it and find out!

# Vision for right now:

1. Add the ability to build spaceships from a commandline interface
2. Add the ability to test components in isolation
3. Multiplayer
4. Add the ability to create blueprints for quickly re-assembling components you've previously designed
5. Add some kind of graphical element (probably 2D)
6. Implement the game portion, flying in space, repairing on the fly etc.
7. fleets of ships battling, other features...

# Copyright

This file is part of spaceship-build.

spaceship-build is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

spaceship-build is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with spaceship-build.  If not, see <http://www.gnu.org/licenses/>.
