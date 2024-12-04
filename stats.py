import math
import subprocess
import icons
from gpiozero import CPUTemperature, LoadAverage
import socket


def get_wifi_strength():
    return int(subprocess.check_output(
        "iwconfig wlan0 | grep Signal | cut -d'=' -f3 | cut -d' ' -f1",
        shell=True,
        text=True
    ).strip())


def get_wifi_strength_icon(strength):
    if not strength:
        strength = get_wifi_strength()

    # print(f"Strength: {strength}")
    if strength > -67:
        return icons.WIFI_4
    elif strength > -70:
        return icons.WIFI_3
    elif strength > -80:
        return icons.WIFI_2
    elif strength > -90:
        return icons.WIFI_1
    else:
        return icons.WIFI_0

def get_cpu_temperature():
    return f"{math.floor(CPUTemperature().temperature)}°C"

def get_cpu_load_average():
    return f"{math.floor(LoadAverage().load_average*100)}%"

def get_hostname():
    return socket.gethostname()

def get_ip_address():
    return subprocess.check_output(
        "ifconfig wlan0 | grep inet | head -n 1 | awk '($1=$1)' | cut -d' ' -f 2",
        shell=True,
        text=True
    )
