import time
import subprocess
import argparse
import requests
from sys import platform
import os

TGREEN = '\033[32;1m'
TRED = '\033[31;1m'
TCYAN = '\033[36;1m'
TPURPLE = '\033[35;1m'
TYELLOW = '\033[33;1m'
TBLUE = '\033[34;1m'
ENDC = '\033[m'  # reset to the defaults


def equalizer(list):
    ele = []
    for i in list:
        i = i.replace("\n", " ")
        ele.append(i)
    maxart = len(max(ele, key=len))

    for i in range(len(ele)):

        if len(ele[i]) < maxart:
            ele[i] += " " * (maxart - len(ele[i]))

    return ele


# traverse the info
class WinSystem:
    def __init__(self):
        Id = subprocess.check_output(
            ['systeminfo']).decode('utf-8').split('\n')
        Id = Id[1:-1]
        new = []

        # arrange the string into clear info
        for item in Id:
            pair = item.split("\r")[:-1][0]
            new.append(pair)
        # for i in range(len(new)):
        #     print(i, new[i])
        self.info = new
        self.ignore = []

    def sysinfo(self):

        self.ignore = [4, 5, 7, 8, 9, 10, 11, 16, 17, 18, 19, 21, 25, 26, 27]
        artcounter = 0
        pos = logo_pos["win"]
        win = content[pos[0]:pos[1]]
        for i in range(27):

            if i not in self.ignore:
                data = self.info[i].split(":", 1)
                line = TBLUE + data[0] + " : " + TGREEN + data[-1] + ENDC
                if artcounter < len(win):
                    artl = win[artcounter].replace("#\n", " ")
                    artline = TCYAN + (" " * 5) + artl + ENDC + (" " * 5)
                    line = artline + line
                    artcounter += 1
                else:
                    line = (" " * len(win[3])) + (" " * 5) + line
                print(line)

    def sysinfo_extra(self):

        addmore = [25, 26, 27]
        self.sysinfo()
        print(ENDC + "\n_________ More Info _________\n")
        for i in range(25, len(self.info)):
            if i in addmore:
                data = self.info[i].split(":", 1)
                print(TPURPLE + data[0] + " : " + TYELLOW + data[-1] + ENDC)
                time.sleep(.3)

        netindex = -1
        for i in range(30, len(self.info)):
            title = self.info[i].split(":")
            if "Network Card(s)" in title[0]:
                netindex = i
                break

        if netindex != -1:
            for i in range(netindex, netindex + 8):
                data = self.info[i].split(":", 1)
                if len(data) != 1:
                    print(TCYAN + data[0].strip() + " : " + ENDC + data[-1])
                else:
                    print(TCYAN + data[0].strip() + ENDC)
                time.sleep(.3)
        print("\n \n")


class lnx_info:
    def __init__(self):
        osinfo = subprocess.check_output(
            ['hostnamectl']).decode('utf-8').split("\n")
        osinfo = osinfo[:-1]
        infodic = {}

        host = osinfo[0].split(": ")
        osname = osinfo[5].split(": ")
        kernal = osinfo[6].split(": ")
        architecture = osinfo[7].split(": ")

        infodic["Host"] = host[1].strip()
        infodic["OS"] = osname[1].strip()
        infodic["Kernal"] = kernal[1].strip()
        infodic["Architecture"] = architecture[1].strip()

        uptime = subprocess.check_output(
            ['uptime']).decode('utf-8').split(",", 1)[0]
        uptime = uptime.split("up")[-1]
        uptime = uptime.replace("min", "")
        uptime = uptime.strip()
        uptime = uptime.split(":")
        up = uptime[-1] + " Min"
        if len(uptime) > 1:
            up = uptime[0] + " Hour, " + up

        infodic["Uptime"] = up

        try:
            f = open("/sys/devices/virtual/dmi/id/product_name", "r")
            infodic["Device name"] = f.read().strip()
            f.close()
        except:
            pass

        shell = subprocess.check_output(
            ['bash', "--version"]).decode('utf-8').split("\n")[0]
        shell = shell.split("-", 1)[0]
        shell = shell.split(", ")
        infodic["Shell"] = shell[0] + " V" + shell[1].split()[-1]

        try:
            result = os.statvfs('/')
            block_size = result.f_frsize
            total_blocks = result.f_blocks
            free_blocks = result.f_bfree
            giga = 1000 * 1000 * 1000
            total_size = total_blocks * block_size / giga
            free_size = free_blocks * block_size / giga
            used_size = total_size - free_size
            infodic["Disk space"] = str(round(used_size, 2)) + \
                                    " GiB /" + str(round(total_size, 2)) + " GiB"
        except:
            pass

        cpu = subprocess.check_output(['lscpu']).decode('utf-8').split("\n")
        core = cpu[3].split(": ")[1].strip()
        clock = float(cpu[15].split(": ")[1].strip()) / 1000
        for row in cpu:
            if "Model name" in row:
                val = row.split(": ")
                infodic["Processor"] = val[1].strip().split(
                    "with")[0] + "(core " + core + ") @ " + str(clock) + " GHz"
                break

        gpu = subprocess.check_output(['lspci']).decode('utf-8').split("\n")
        gpu = gpu[1].split(": ")
        infodic["GPU"] = gpu[1].strip()

        desktop_enviroment = os.environ.get('DESKTOP_SESSION')
        infodic["DE"] = desktop_enviroment.strip()

        screen = subprocess.check_output(
            ['xrandr']).decode('utf-8').split("\n")[0]
        screen = screen.split(",")[1].strip().split(" ", 1)
        infodic["Screen "] = screen[-1]

        self.info = infodic

    def display(self):
        print()
        keys = list(self.info.keys())
        target = True
        if "elementary" in self.info["OS"]:
            pos = logo_pos["elementary"]
            art = equalizer(content[pos[0]:pos[1]])
        elif "mint" in self.info["OS"].lower():
            pos = logo_pos["mint"]
            mint = equalizer(content[pos[0]:pos[1]])
            mint = "".join(mint)
            mint = mint.replace("${c2}", "\033[32;1m")
            mint = mint.replace("${c1}", "\033[m")
            art = mint.split("/n")

        else:
            art = ["", ""]

        print(art[0] + (" " * 4) + TRED + self.info["Host"] + ENDC)
        print(art[1] + (" " * 4) + TCYAN + ("-" * 20) + ENDC)

        height = max(len(art), len(self.info.keys()))
        for i in range(1, height):
            if i < len(art):
                print(art[i + 1] + ENDC + (" " * 5), end="")
            else:
                print(" " * len(art[0]) + (" " * 5), end="")

            if i < len(keys):
                print(TBLUE + keys[i] + ENDC, ":", TCYAN +
                      self.info[keys[i]] + ENDC, end="")
            print()

        print("\n\n")


class Weather:
    def __init__(self):
        self.baseurl = "http://api.openweathermap.org/data/2.5/weather?q="
        self.weatherapi = "8e44efb0ae84f237a5d93f5f4d629433"

    def fetchweather(self):
        place = input("Enter location : ")
        url = self.baseurl + place + "&appid=" + \
              str(self.weatherapi) + "&units=metric"
        res = requests.get(url)
        data = res.json()
        if data["cod"] == 200:
            print(TYELLOW + "city found" + ENDC)
            print("------------------------\n")

            city = data["name"]
            country = data["sys"]["country"]
            windspeed = data["wind"]["speed"]
            pressure = data["main"]["pressure"]
            temp = data["main"]["temp"]
            hum = data["main"]["humidity"]
            visi = data["visibility"]
            des = data["weather"][0]["description"]
            time.sleep(.5)
            print(TPURPLE + "city : " + ENDC + str(city) + "," + str(country))
            time.sleep(.5)
            print(TPURPLE + "Temperature : " +
                  ENDC + str(temp), "degree celcius")
            time.sleep(.5)
            print(TPURPLE + "Humidity : " + ENDC + str(hum), "%")
            time.sleep(.5)
            print(TPURPLE + "Visibility : " + ENDC + str(visi), "meteres")
            time.sleep(.5)
            print(TPURPLE + "Wind speed : " + ENDC + str(windspeed), "miles/h")
            time.sleep(.5)
            print(TPURPLE + "Pressure : " + ENDC + str(pressure), "hPa")
            time.sleep(.5)
            print(TYELLOW + "Overall : " + ENDC + str(des))
            print("\n......... Data from https://openweathermap.org/\n")


def recognize_os(e=False):
    if platform == "linux" or platform == "linux2":
        lnx_info().display()
    elif platform == "darwin":
        print("sorry currently this feature doesn't effective on any other system than Windows")
    elif platform == "win32":
        if e:
            WinSystem().sysinfo_extra()
        else:
            WinSystem().sysinfo()


# Windows...

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--system", action="store_true",
                        help="find your system info")
    parser.add_argument("-e", "--extra", action="store_true",
                        help="find extra system info")
    parser.add_argument("-w", "--weather", action="store_true",
                        help="Fetch weather report")
    args = parser.parse_args()
    if args.system or args.extra:
        f = open("ascii_art.txt", "r")
        content = f.readlines()

    logo_pos = {
        "win": [1, 14],
        "elementary": [16, 33],
        "mint": [35, 52]
    }
    if args.system:
        recognize_os()
    elif args.extra:
        recognize_os(e=True)
    elif args.weather:
        Weather().fetchweather()
    else:
        print("No instruction found,\nTry 'dodge.exe -h' for more info.")
