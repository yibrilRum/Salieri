from music21 import environment
from scorecreator.menu import main

us = environment.UserSettings()
us["musicxmlPath"] = "/usr/local/bin/musescore-flatpak"

if __name__ == "__main__":
    main()