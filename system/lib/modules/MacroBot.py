import modules.Inputs as Inputs
import minescript as ms
import re
import json
import time
from abc import ABC, abstractmethod
from modules.Utilities.BotJsonPath import getBotJsonPath


class MacroBot:

    def __init__(self, *, BOT_ID: str):
        self.running = True
        self.BOT_ID = BOT_ID


    @abstractmethod
    def runLogic(): ...

    def stop(self, BOT_ID: str):

        with open(getBotJsonPath(__file__), 'r') as f:
            data = json.load(f)
            data[BOT_ID] = ["stop", 0]

        with open(getBotJsonPath(__file__), 'w') as f:
            json.dump(data, f, indent=4)

        self.running = False
        Inputs.releaseAllInputs()
        ms.echo("Stopping bot...")

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

    @staticmethod
    def get_position():
        x, y, z = ms.player_position()
        return round(x, 3), round(y, 5), round(z, 3)

    @staticmethod
    def get_look_direction():
        yaw, pitch = ms.player_orientation()
        return yaw, pitch

    @staticmethod
    def get_item_name(slot: int):
        inventory = ms.player_inventory()

        nbtData = inventory[slot].nbt

        match = re.search(
            r'"minecraft:custom_name":\{.*?text:"(.*?)"',
            nbtData
        )

        if match:
            return match.group(1)
        else:
            print("No match was found (MacroBot.getItemName)")
            return None



    
    def run(self, BOD_ID, *, stopKey: str = "space"):
        Inputs.onKeyPress(BOD_ID, stopKey, self.stop)

        try:
            # Register world listener event so minescript doesn't terminate the process when transfering worlds
            with ms.EventQueue() as event_queue:
                event_queue.register_world_listener()
                self.runLogic()
        finally:
            Inputs.releaseAllInputs()