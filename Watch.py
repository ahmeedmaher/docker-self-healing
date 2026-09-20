
#!/usr/bin/env python3

import subprocess
import time
from datetime import datetime

CONTAINERS = [
    list of your container Name
]

CHECK_INTERVAL = 60


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def get_container_status(container):
    result = subprocess.run(
        [
            "docker",
            "inspect",
            "--format",
            "{{.State.Status}}",
            container,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return "NOT_FOUND"

    return result.stdout.strip()


def restart_container(container):
    log(f"[WARNING] {container} is stopped. Restarting...")

    result = subprocess.run(
        ["docker", "restart", container],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        log(f"[OK] {container} restarted successfully")
    else:
        log(f"[ERROR] Failed to restart {container}")
        log(result.stderr.strip())


def check_containers():

    log("Checking Docker containers...")

    for container in CONTAINERS:

        status = get_container_status(container)

        log(f"{container}: {status}")

        if status in ["exited", "dead"]:
            restart_container(container)

        elif status == "running":
            log(f"[OK] {container} is running")

        elif status == "NOT_FOUND":
            log(f"[ERROR] {container} does not exist")

        else:
            log(f"[INFO] {container} status: {status}")


def main():

    log("Eldib Docker Watchdog started")
    log(f"Check interval: {CHECK_INTERVAL} seconds")

    while True:

        try:
            check_containers()

        except Exception as e:
            log(f"[ERROR] {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()

