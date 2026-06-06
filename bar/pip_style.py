import time
import random

total = 100
current = 0
spinner = "|/-\\"

while current <= total:
    bar_len = 40
    filled_len = int(bar_len * current / total)

    bar = "#" * filled_len + "." * (bar_len - filled_len)
    spin = spinner[current % len(spinner)]

    speed = random.uniform(1.2, 4.8)

    print(
        f"\r{spin} Downloading [{bar}] {current:3d}% {speed:.1f}MB/s",
        end="",
        flush=True
    )

    time.sleep(0.06)
    current += 1

print("\n完成！")