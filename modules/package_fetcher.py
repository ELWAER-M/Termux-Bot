import requests
import json

repos = json.load(open("modules/repos.json", "r"))
main = repos["termux-packages"]
root = repos["termux-root-packages"]
science = repos["science-packages"]
game = repos["game-packages"]
x11 = repos["x11-packages"]

def req(arch, repo):
    try:
        pkg_ls = requests.get(f"{repo['repo_url']}/dists/{repo['distribution']}/{repo['component']}/binary-{arch}/Packages").text.splitlines()
    except:
        return "err1"
    info = {}
    try:
        for idx, i in enumerate(pkg_ls):
            if "Package:" in i:
                info[i.split(": ")[1]] = {}
                x = 0
                while True:
                    info[i.split(": ")[1]].update({pkg_ls[idx+x].split(": ")[0]: pkg_ls[idx+x].split(": ")[1]})
                    x = x+1
                    if pkg_ls[idx+x] == "":
                        break
        return info
    except:
        return "err2"

def fetch(pkg_n, arch, repo):
    r = req(arch, repo)
    if r == "err1":
        return "err1"
    elif r == "err2":
        return "err2"
    else:
        if pkg_n in r:
            return r[pkg_n]
        else:
            return "err3"

def search(sfor, arch, repo):
    r = req(arch, repo)
    if r == "err1":
        return "err1"
    elif r == "err2":
        return "err2"
    else:
        info = {}
        for x in r:
            if sfor in r[x]["Description"] or sfor in r[x]["Package"]:
                info[x] = {}
                info[x].update(r[x])
        else:
            if info:
                return info
            else:
                return "err3"
