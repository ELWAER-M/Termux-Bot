import requests
import json

repos = json.load(open("modules/repos.json", "r"))
main = repos["termux-packages"]
root = repos["termux-root-packages"]
x11 = repos["x11-packages"]
hosts = ["packages.termux.org", "packages-cf.termux.org", "termux.librehat.com", "termux.mentality.rip"]

def fetch(arch, repo):
    for host in hosts:
        try:
            pkg_ls = requests.get(f"https://{host}{repo['repo_url']}/dists/{repo['distribution']}/{repo['component']}/binary-{arch}/Packages", stream=True, timeout=10).content.decode("utf-8").splitlines()
            info = {"_host": {"host": host}}
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
            pass
    return False
