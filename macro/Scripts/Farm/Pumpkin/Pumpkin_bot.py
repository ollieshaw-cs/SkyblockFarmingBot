import macro.setup as setup
import modules.Inputs as Inputs
import time
import random
import json
import minescript as ms

from modules.MacroBot import MacroBot
from typing_extensions import override
from modules.Utilities.BotJsonPath import getBotJsonPath
from modules.Utilities import ScoreboardHandler


class PumpkinBot(MacroBot):

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
        

    def farmRight(self):

        if (self.onFarmRightCooldown): return

        self.onFarmLeftCooldown = False
        Inputs.leftMouseUp()

        if not self.wait(random.uniform(2, 4)):
            return

        Inputs.releaseAllInputs()
        self.farmingDirection = "right"


        if not self.wait(random.uniform(1, 3)):
            return

        Inputs.leftMouseDown()

        if not self.wait(random.uniform(0.1, 1)):
            return


        self.onFarmRightCooldown = True
        Inputs.pressKey("w")
        Inputs.pressKey("d")


    def farmLeft(self, x):

        if (self.onFarmLeftCooldown): return

        self.onFarmRightCooldown = False
        Inputs.leftMouseUp()

        if not self.wait(random.uniform(2, 4)):
            return

        Inputs.releaseAllInputs()
        self.farmingDirection = "left"

        # only use the mousemat at the start of the farm
        if x == -150.700:
            Inputs.pressKey(self.squeakyMousematKeybind, random.uniform(0, 0.75))
            

            if not self.wait(random.uniform(1, 2)):
                return

            Inputs.leftMouseDown()
            Inputs.leftMouseUp()

            if not self.wait(random.uniform(0.5, 1.5)):
                return

            Inputs.pressKey(self.farmingToolKeybind)

            if not self.wait(random.uniform(0.5, 2)):
                return


        Inputs.leftMouseDown()

        if not self.wait(random.uniform(0.5, 1)):
            return


        self.onFarmLeftCooldown = True
        Inputs.pressKey("w")
        Inputs.pressKey("a")

    def warpBackToStart(self):
        Inputs.releaseAllInputs()

        self.onFarmLeftCooldown = False
        self.onFarmRightCooldown = False


        if not self.wait(random.uniform(1, 3)):
            return

        ms.execute("/warp garden")

        if not self.wait(random.uniform(1, 3)):
            return

    @override
    def runLogic(self):

        while self.running:

            with open(getBotJsonPath(__file__), 'r') as f:
                data = json.load(f)

            status, endTime = data[self.BOT_ID]

            if status == "stop" or time.time() >= endTime:
                print("Bot duration expired. Stopping...")
                self.stop(self.BOT_ID)
                break

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
                self.farmLeft(x)

            elif z == 238.700:
                self.farmRight()
                

bot = PumpkinBot(
    farmingToolKeybind="1",
    squeakyMousematKeybind="6"
)

bot.run(bot.BOT_ID, stopKey="space")