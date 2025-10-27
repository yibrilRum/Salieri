from music21 import environment
from scorecreator.menu import main

us = environment.UserSettings()
us["musicxmlPath"] = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"

if __name__ == "__main__":
    main()