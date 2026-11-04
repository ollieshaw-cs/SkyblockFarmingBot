from pathlib import Path

def getBotJsonPath(source):
    current = Path(source).resolve().parent

    while current != current.parent:
        botsJsonPath = current / "bots.json"

        if botsJsonPath.exists():
            return botsJsonPath

        current = current.parent

    raise FileNotFoundError("Could not find bots.json in parent directories.")