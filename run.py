import sys
import minescript as ms
import time
import modules.MacroBot as MacroBot
import json
import modules.Inputs as Inputs
from modules.Utilities.BotJsonPath import getBotJsonPath

timeConversion = {
    "seconds" : 1,
    "minutes" : 60,
    "hours" : 3600
}

# print()
# for idx, arg in enumerate(sys.argv):
#     print(f"{idx}: {arg}")
# print()

if len(sys.argv) == 2:
    runTime = 86400 * 7
elif len(sys.argv) == 3:
    runTime = int(sys.argv[2])
else:
    runTime = int(sys.argv[2]) * timeConversion.get(sys.argv[3])

scriptToRun: str = sys.argv[1]

scripts = {
    "mushroom" : "Scripts\Farm\Mushroom\Mushroom_bot",
    "pumpkin" : "Scripts\Farm\Pumpkin\Pumpkin_bot",
    "melon" : "Scripts\Farm\Melon\Melon_bot"
}

endTime = int(time.time()) + runTime

if scriptToRun in list(scripts.keys()):

    jsonPath = getBotJsonPath(__file__)

    with open(jsonPath, 'r') as file:
        data = json.load(file)

    data[scriptToRun] = ["running", endTime]

    with open(jsonPath, 'w') as file:
        json.dump(data, file, indent=4)

    ms.execute(f"\{scripts.get(scriptToRun)}")

else:
    ms.echo()
    ms.echo(rf"§2\run <script> <duration> <time unit>")
