import subprocess
import platform

def is_reachable(ip: str) -> bool:
    param = "-n" if platform.system().lower() == "windows" else "-c"
    result = subprocess.run(["ping", param, "1", ip], stdout=subprocess.DEVNULL)
    return result.returncode == 0
