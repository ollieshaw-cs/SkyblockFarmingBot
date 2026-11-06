import modules.Inputs as Inputs
import time
import random
import json
import minescript as ms


from modules.MacroBot import MacroBot
from typing_extensions import override
from modules.Utilities.BotJsonPath import getBotJsonPath
from modules.Utilities import ScoreboardHandler

class MelonBot(MacroBot):

    def __init__(
        self,
        *,
        farmingToolKeybind: str,
        squeakyMousematKeybind: str
        
    ):
        self.farmingDirection = "left"
        self.onFarmLeftCooldown = False
        self.onFarmRightCooldown = False

        self.farmingToolKeybind = farmingToolKeybind
        self.squeakyMousematKeybind = squeakyMousematKeybind

        super().__init__(BOT_ID="pumpkin")

        with open(getBotJsonPath(__file__), 'r') as f:
            data = json.load(f)
            data[self.BOT_ID] = "running"

        with open(getBotJsonPath(__file__), 'w') as f:
            json.dump(data, f, indent=4)
        

    def farmRight(self):

        if (self.onFarmRightCooldown): return

        self.onFarmLeftCooldown = False
        Inputs.leftMouseUp()
        time.sleep(random.uniform(2, 4))
        Inputs.releaseAllInputs()
        self.farmingDirection = "right"

        time.sleep(random.uniform(1, 3))
        Inputs.leftMouseDown()
        time.sleep(random.uniform(0.1, 1))

        self.onFarmRightCooldown = True
        Inputs.pressKey("w")
        Inputs.pressKey("d")


    def farmLeft(self):

        if (self.onFarmLeftCooldown): return

        self.onFarmRightCooldown = False
        Inputs.leftMouseUp()
        time.sleep(random.uniform(2, 4))
        Inputs.releaseAllInputs()
        self.farmingDirection = "left"

        Inputs.pressKey(self.squeakyMousematKeybind, random.uniform(0, 0.75))
        time.sleep(random.uniform(1, 2))
        Inputs.leftMouseDown()
        Inputs.leftMouseUp()
        time.sleep(random.uniform(0.5, 1.5))
        Inputs.pressKey(self.farmingToolKeybind)
        time.sleep(random.uniform(0.5, 2))

        Inputs.leftMouseDown()
        time.sleep(random.uniform(0.5, 1))

        self.onFarmLeftCooldown = True
        Inputs.pressKey("w")
        Inputs.pressKey("a")

    def warpBackToStart(self):
        Inputs.releaseAllInputs()

        self.onFarmLeftCooldown = False
        self.onFarmRightCooldown = False

        time.sleep(random.uniform(1, 3))
        ms.execute("/warp garden")
        time.sleep(random.uniform(1, 3))

    # TODO: make it so the job doesnt end after running '/l'
    def getBackIntoGarden(self):
        Inputs.releaseAllInputs()
        self.onFarmLeftCooldown = False
        self.onFarmRightCooldown = False

        time.sleep(10)
        ms.execute("/l")
        time.sleep(10)
        ms.execute("/play skyblock")
        time.sleep(10)
        ms.execute("/warp garden")
        time.sleep(8)

    @override
    def runLogic(self):

        while self.running:

            try:
                position = MacroBot.get_position()

                if position is None:
                    time.sleep(1)
                    continue

                x, y, z = position

            except Exception:
                # Wait while Minecraft is transitioning worlds
                time.sleep(1)
                continue

            with open(getBotJsonPath(__file__), 'r') as f:
                data = json.load(f)
                shouldStop = data[self.BOT_ID] == "stop"

            if shouldStop:
                self.stop(self.BOT_ID)
                break

            isInGarden = ScoreboardHandler.isInGarden()

            if isInGarden is False:
                print("Transfering you back to the garden...")
                self.getBackIntoGarden()
                continue

            if x == -174.700 and z == 238.700:
                self.warpBackToStart()
                time.sleep(2)
                continue

            if z == -238.700:
                self.farmLeft()

            elif z == 238.700:
                self.farmRight()
                

bot = MelonBot(
    farmingToolKeybind="1",
    squeakyMousematKeybind="6"
)

bot.run(bot.BOT_ID, stopKey="space")