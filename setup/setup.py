import pathlib
from swinlnk.swinlnk import SWinLnk
import win32com.client
import os
import json

shortcut_name = 'scrape.lnk'
swl = SWinLnk()
startup = os.path.expandvars(
    r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')
shortcut_path = f"{startup}\\{shortcut_name}"

# def get_correct_path(relative_path):
#     import sys
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

def create_shortcut():
    shortcut_target = pathlib.Path(__file__).parent.parent.absolute()
    if not os.path.isfile(shortcut_path):
        # if shortcut does not exist create it in windows startup folder
        swl.create_lnk(f"{shortcut_target}\main.exe", shortcut_path)
        print('tar:', shortcut_target, 'pth', shortcut_path)


def change_working_dir():
    if os.path.isfile(shortcut_path):
        # if shortcut exists change working directory to shortcut target
        shell = win32com.client.Dispatch("WScript.Shell")
        target = shell.CreateShortcut(shortcut_path).TargetPath
        print('old dir: ', os.getcwd())
        os.chdir(pathlib.Path(target).parent.parent)
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
                "security_code": ""
            }
            json.dump(config, f, indent=4)


def setup():
    create_shortcut()
    change_working_dir()
    create_dir()


if __name__ == "__main__":
    create_dir()
