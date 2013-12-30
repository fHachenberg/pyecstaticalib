pyecstaticalib
============

Python library to load and represent data structures from the 1994 horror game Ecstatica

Ecstatica is published by Psygnosis, Copyright 1994 by Andrew Spencer Studios. 

More information about the library and the data formats can be found on http://ecstatica.wikidot.com/.

Prerequisites
-------------

* Python 3.x
* Ecstatica game files. Please purchase a legal copy of the game!

Assemble test data
------------------
In order to run the unit tests, the library requires a couple of game data files in a subfolder "test" (within the "Ecstatica" folder). Because Ecstatica is a MS-DOS game, the file names might be translated into upper case words. In that case, you have to rename them to lower case or change the filenames in the unit tests. Please copy the following files into the "test" folder

* e_config.
* ecst2. (found in subfolder "FILES")
* ecstatic. (found in subfolder "FILES")
* ecstatic.fan (found in subfolder "CODE")
* offsets.
* off2.
* title2.raw (found in subfolder "GRAPHICS")
* the complete folder "views"


