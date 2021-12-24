import re
from pathlib import Path

DATA_DIR = Path("./data")
SCREENSHOTS_DIR = Path("./screenshots")

EVENTS_DIR = DATA_DIR / "strains" / "events"
EVENTS_DIR.mkdir(parents=True, exist_ok=True)

dT = 16  # Each epoch will lie [-dT, +dT] from a given timestamp

FPS = 4096  # Strain sampling rate

TIMESTAMP_PATTERN = re.compile(r"(\d+)-4096.hdf5$")
