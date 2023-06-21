from time import sleep
import subprocess

while True:
    with open("seatPlaner.py") as f:
        exec(f.read())
    cmd = ['python', 'main.py']  # the external command to run
    timeout_s = 30  # how many seconds to wait
    try:
        p = subprocess.run(cmd, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        print(f'Timeout for {cmd} ({timeout_s}s) expired')