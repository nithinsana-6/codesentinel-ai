import os
import subprocess

API_KEY = "super-secret-token-123"


def run_backup(path):
    # TODO: validate user input before shelling out
    subprocess.run(f"tar -czf backup.tgz {path}", shell=True)


def handler(event):
    try:
        run_backup(event["path"])
    except Exception:
        return {"ok": False}
    return {"ok": True}


if __name__ == "__main__":
    debug = True
    print(handler({"path": os.getcwd()}))
