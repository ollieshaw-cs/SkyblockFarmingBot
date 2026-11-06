import minescript as ms
from typing_extensions import Callable

def isInGarden():

    Scoreboard = ms.get_scoreboard()

    if Scoreboard == None:
        return Scoreboard
    
    ScoreboardEntries = Scoreboard.entries

    isInGarden = False

    for entry in ScoreboardEntries:
        if entry.display_name.lower().find("copper") != -1:
            isInGarden = True

    return isInGarden