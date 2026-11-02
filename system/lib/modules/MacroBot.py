import modules.Inputs as Inputs
import minescript as ms
import re
import json
from typing import Callable
from abc import ABC, abstractmethod
from BotJsonPath import botsJsonPath

class MacroBot:

    def __init__(self, *, BOT_ID: str):
        self.running = True
        self.BOT_ID = BOT_ID


    @abstractmethod
    def runLogic(): ...

    def stop(self, BOT_ID: str):

        with open(botsJsonPath, 'r') as f:
            data = json.load(f)
            data[BOT_ID] = "stop"

        with open(botsJsonPath, 'w') as f:
            json.dump(data, f, indent=4)

        self.running = False
        Inputs.releaseAllInputs()
        ms.echo("Stopping bot...")

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
            self.runLogic()
        finally:
            Inputs.releaseAllInputs()