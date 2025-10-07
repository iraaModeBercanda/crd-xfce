#!/usr/bin/env python3
import time
import psutil

while True:
    freq = psutil.cpu_freq()
    if freq:
        with open("diagnosa.txt", "a") as f:
            f.write(f"Waktu: {time.strftime('%Y-%m-%d %H:%M:%S')} | CPU: {freq.current:.2f} MHz\n")
    else:
        with open("diagnosa.txt", "a") as f:
            f.write(f"Waktu: {time.strftime('%Y-%m-%d %H:%M:%S')} | CPU: tidak ditemukan\n")
    time.sleep(60)
