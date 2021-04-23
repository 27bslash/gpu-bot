import pathlib
from swinlnk.swinlnk import SWinLnk
import win32com.client
import os
import json
import sys

shortcut_name = 'scrape.lnk'
swl = SWinLnk()
startup = os.path.expandvars(
    r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')
shortcut_path = f"{startup}\\{shortcut_name}"


def get_correct_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    print('argv', sys.argv[0])
    print('base path', base_path)
    print('abs path', os.path.abspath('.'))
    print('ret: ', os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)


def create_shortcut():
    shortcut_target = f"{os.path.abspath('.')}"
    if not os.path.isfile(shortcut_path):
        # if shortcut does not exist create it in windows startup folder
        swl.create_lnk(sys.argv[0], shortcut_path)


def change_working_dir():
    if os.path.isfile(shortcut_path):
        # if shortcut exists change working directory to shortcut target
        shell = win32com.client.Dispatch("WScript.Shell")
        target = shell.CreateShortcut(shortcut_path).TargetPath
        os.chdir(pathlib.Path(target).parent)
        print('working dir: ', os.getcwd())


def create_dir():
    if not os.path.isdir('user_details'):
        os.mkdir('user_details')
    file = os.path.isfile('user_details/config.json')
    if not file:
        with open('user_details/config.json', 'w') as f:
            config = {
                "currys_email": "",
                "currys_password": "",
                "card_number": "",
                "card_holder_name": "",
                "card_expiry_month": "",
                "card_expiry_year": "",
                "security_code": "",
                "max_price": "",
            }
            json.dump(config, f, indent=4)


def setup():
    create_shortcut()
    change_working_dir()
    create_dir()


if __name__ == "__main__":
    setup()
    pass
