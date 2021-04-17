import requests
from pathlib import Path
from pkg_resources import packaging

owner = '27bslash'
repo = 'gpu-bot'

def download_latest_release():
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/releases/latest")
    data = response.json()
    new_version = data['tag_name']
    file = Path('version.txt')
    curr_version = '0'
    if not file.is_file():
        f = open(file, 'w').write(data['tag_name'])
    else:
        curr_version = open(file, 'r').read()
    if not compare_versions(curr_version, new_version):
        return
    open(file, 'w').write(new_version)
    for i in data['assets']:
        print(i['browser_download_url'])
        dl = requests.get(i['browser_download_url'])
        open('main.exe', 'wb').write(dl.content)


def compare_versions(curr, new):
    return packaging.version.parse(curr) < packaging.version.parse(new)

if __name__ == '__main__':
    download_latest_release()

