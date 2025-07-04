import subprocess
import re
def get_saved_ssids():
    result = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], shell=True, encoding='utf-8', errors='ignore')
    ssids = re.findall(r"All User Profile\s*:\s*(.*)", result)
    return [ssid.strip() for ssid in ssids]
def get_password_for_ssid(ssid):
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', ssid, 'key=clear'], shell=True, encoding='utf-8', errors='ignore')
        password_match = re.search(r"Key Content\s*:\s*(.*)", result)
        if password_match:
            return password_match.group(1)
        else:
            return None
    except subprocess.CalledProcessError:
        return None
def main():
    ssids = get_saved_ssids()
    if not ssids:
        print("No saved WiFi profiles found.")
        return

    for ssid in ssids:
        password = get_password_for_ssid(ssid)
        print(f"SSID: {ssid} | Password: {password if password else 'N/A'}")
if __name__ == "__main__":
    main()
