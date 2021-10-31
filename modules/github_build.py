import requests


def last_build():
    r = requests.get("https://api.github.com/repos/termux/termux-app/actions/runs")

    j = r.json()
    n = j["workflow_runs"]
    
    for x in n:
        if x["name"] == "Build" and x["status"] == "completed":
            f = x["html_url"]
            break

    return f
