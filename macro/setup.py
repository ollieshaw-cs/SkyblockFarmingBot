import sys
from pathlib import Path

MACRO_DIR = Path(__file__).resolve().parent

if str(MACRO_DIR) not in sys.path:
    sys.path.insert(0, str(MACRO_DIR))