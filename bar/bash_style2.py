import time

total = 100
spinner = "|/-\\"

for i in range(total + 1):
    percent = i / total
    bar_len = 30
    filled_len = int(bar_len * percent)

    bar = "#" * filled_len + "-" * (bar_len - filled_len)
    spin = spinner[i % len(spinner)]

    print(f"\r{spin} [{bar}] {i}%", end="", flush=True)
    time.sleep(0.05)

print()