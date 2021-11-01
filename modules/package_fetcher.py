import requests
import json

repos = json.load(open("modules/repos.json", "r"))
main = repos["termux-packages"]
root = repos["termux-root-packages"]
science = repos["science-packages"]
game = repos["game-packages"]
x11 = repos["x11-packages"]

def fetch(pkg_name, arch, repo):
    try:
        pkg_ls = requests.get(f"{repo['repo_url']}/dists/{repo['distribution']}/{repo['component']}/binary-{arch}/Packages").text.splitlines()
    except:
        return False
    info = {}
    for idx, i in enumerate(pkg_ls):
        if i == f'Package: {pkg_name}':
            x = 0
            while True:
                info[pkg_ls[idx + x].split(': ')[0]] = pkg_ls[idx + x].split(': ')[1]
                x = x+1
                if pkg_ls[idx + x] == "":
                    break
            break
    else:
        return False
    return info
