import subprocess
import icons


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

