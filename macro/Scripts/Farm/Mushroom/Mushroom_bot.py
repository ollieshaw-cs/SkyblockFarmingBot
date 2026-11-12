import macro.setup as setup
import time
import random
import json
import modules.Utilities.ScoreboardHandler as ScoreboardHandler

import minescript as ms
import modules.Inputs as Inputs
import modules.MacroBot as MB
from modules.MacroBot import MacroBot
from typing_extensions import override
from modules.Utilities.BotJsonPath import getBotJsonPath

class MushroomBot(MacroBot):
    LEFT_Z = 238.700
    RIGHT_Z = -238.700
    WARP_X = 52.700

    def __init__(
            self,
            *, 
            farmingToolKeybind: str,
            farmingLeftMousematKeybind: str,
            farmingRightMousematKeybind: str 
            ):
        self.moving_backward = False
        self.farming_direction = "left"

        self.farmingToolKeybind = farmingToolKeybind
        self.farmingLeftMousematKeybind = farmingLeftMousematKeybind
        self.farmingRightMousematKeybind = farmingRightMousematKeybind

        # Prevent the same position trigger from repeating.
        self.farm_left_cooldown = False
        self.farm_right_cooldown = False
        self.warp_cooldown = False


        super().__init__(BOT_ID="mushroom")

        # with open(getBotJsonPath(__file__), 'r') as f:
        #     data = json.load(f)
        #     data[self.BOT_ID] = ["running", 0]

        # with open(getBotJsonPath(__file__), 'w') as f:
        #     json.dump(data, f, indent=4)
             
        

    def farm_in_direction(self):
        Inputs.leftMouseDown(delay=random.uniform(0, 3))
        Inputs.pressKey("w", 0)
        Inputs.pressKey(
            "a" if self.farming_direction == "left" else "d",
            0,
        )

    def farm_left(self):
        self.farming_direction = "left"
        Inputs.releaseAllInputs()

        time.sleep(1)
        Inputs.pressKey(self.farmingLeftMousematKeybind)
        time.sleep(random.uniform(1, 2))

        Inputs.leftMouseDown()
        Inputs.leftMouseUp()

        time.sleep(random.uniform(1, 3))
        Inputs.pressKey(self.farmingToolKeybind)

    def farm_right(self):
        self.farming_direction = "right"
        Inputs.releaseAllInputs()

        time.sleep(1)
        Inputs.pressKey(self.farmingRightMousematKeybind)
        time.sleep(random.uniform(1, 2))

        Inputs.leftMouseDown()
        Inputs.leftMouseUp()

        time.sleep(random.uniform(1, 3))
        Inputs.pressKey(self.farmingToolKeybind)

    def turn_around(self):
        if self.moving_backward:
            return

        self.moving_backward = True

        try:
            Inputs.releaseAllInputs()
            time.sleep(0.5)

            Inputs.pressKey("s", random.uniform(1, 3))
            time.sleep(1.7)
            Inputs.releaseKey("s")

            self.farm_right()

        finally:
            Inputs.releaseKey("s")
            self.moving_backward = False

    def check_positions(self, x, z):
        at_left = abs(z - self.LEFT_Z) < 0.01
        at_right = abs(z - self.RIGHT_Z) < 0.01
        at_warp = (
            abs(x - self.WARP_X) < 0.01
            and at_left
        )

        if not at_left:
            self.farm_left_cooldown = False

        if not at_right:
            self.farm_right_cooldown = False

        if not at_warp:
            self.warp_cooldown = False

        if at_warp and not self.warp_cooldown:
            self.warp_cooldown = True
            time.sleep(random.uniform(1, 5))
            ms.execute("/warp garden")
            time.sleep(random.uniform(1, 3))
            return

        if at_right and not self.farm_right_cooldown:
            self.farm_right_cooldown = True
            self.turn_around()

        elif at_left and not self.farm_left_cooldown:
            self.farm_left_cooldown = True
            self.farm_left()

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
                orientation = MacroBot.get_look_direction()

                if position is None or orientation is None:
                    time.sleep(1)
                    continue

                x, y, z = position
                yaw, pitch = orientation

            except Exception:
                # Wait while Minecraft is transitioning worlds
                time.sleep(1)
                continue

            isInGarden = ScoreboardHandler.isInGarden()

            if isInGarden is False:
                print("Transfering you back to the garden...")
                self.getBackIntoGarden()
                continue

            if round(yaw, 1) > -90.0:
                self.farming_direction = "right"
            else:
                self.farming_direction = "left"

            self.check_positions(x, z)

            if self.running:
                self.farm_in_direction()




bot = MushroomBot(
    farmingToolKeybind="1",
    farmingLeftMousematKeybind="7",
    farmingRightMousematKeybind="x"
)

bot.run(bot.BOT_ID, stopKey="space")