import modules.Inputs as Inputs
import time
import random
import json

from modules.MacroBot import MacroBot
from typing_extensions import override
from BotJsonPath import botsJsonPath

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

        with open(botsJsonPath, 'r') as f:
            data = json.load(f)
            data[self.BOT_ID] = "running"

        with open(botsJsonPath, 'w') as f:
            json.dump(data, f, indent=4)
        

    def farmRight(self):

        if (self.onFarmRightCooldown): return

        self.onFarmLeftCooldown = False
        Inputs.leftMouseUp()
        time.sleep(random.uniform(1.5, 3.5))
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
        time.sleep(random.uniform(0, 2))
        Inputs.releaseAllInputs()
        self.farmingDirection = "left"

        Inputs.pressKey(self.squeakyMousematKeybind, random.uniform(0, 0.75))
        time.sleep(random.uniform(0.5, 1.5))
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

    @override
    def runLogic(self):
        while self.running:
            x, y, z = MacroBot.get_position()

            with open(botsJsonPath, 'r') as f:
                data = json.load(f)
                shouldStop = True if data[self.BOT_ID] == "stop" else False

            if (shouldStop):
                self.stop(self.BOT_ID)

            if z == -238.700:
                self.farmLeft()

            if z == 238.700:
                self.farmRight()
                

bot = PumpkinBot(
    farmingToolKeybind="1",
    squeakyMousematKeybind="6"
)

bot.run(bot.BOT_ID, stopKey="space")