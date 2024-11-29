import subprocess

output = subprocess.check_output("iwconfig wlan0 | grep Signal | cut -d'=' -f3 | cut -d' ' -f1", shell=True, text=True).strip()
print(output)
