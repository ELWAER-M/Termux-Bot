import requests
import json

mirrors = json.load(open("mirrors.json", "r"))

def fetch(arch, repo):
    for mirror in mirrors:
        try:
            pkg_ls = requests.get(f"{mirrors[mirror][repo][0]}/dists/{mirrors[mirror][repo][1]}/{mirrors[mirror][repo][2]}/binary-{arch}/Packages", stream=True, timeout=10).content.decode("utf-8").splitlines()
            info = {"_host": {"host_name": mirror, "url": mirrors[mirror][repo][0]}}
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
