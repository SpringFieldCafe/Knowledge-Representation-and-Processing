import sys
import time
from colorama import init

init()

RESET = "\033[0m"
GREEN = "\033[92m"
WHITE = "\033[97m"
GRAY = "\033[90m"
YELLOW = "\033[93m"
BLUE = "\033[94m"

def progress_bar(current, total, width=36):
    percent = current / total
    filled = int(width * percent)

    bar_done = GREEN + "━" * filled + RESET
    bar_left = GRAY + "━" * (width - filled) + RESET

    sys.stdout.write(
        f"\r{BLUE}Downloading{RESET} "
        f"{bar_done}{bar_left} "
        f"{YELLOW}{percent * 100:6.2f}%{RESET} "
        f"{WHITE}{current / 1024 / 1024:.1f} MB / {total / 1024 / 1024:.1f} MB{RESET}"
    )
    sys.stdout.flush()


total_size = int(122.9 * 1024 * 1024)
current_size = 0
chunk_size = int(1.2 * 1024 * 1024)

while current_size < total_size:
    time.sleep(0.06)
    current_size += chunk_size

    if current_size > total_size:
        current_size = total_size

    progress_bar(current_size, total_size)

print("\n完成")