import requests

def wiki_s(search_for):
    back = {}

    api_link = "https://wiki.termux.com/api.php"
    api_link += "?action=query"
    api_link += "&generator=search"
    api_link += f"&gsrsearch={search_for}"
    api_link += "&gsrwhat=text"
    api_link += "&prop=info"
    api_link += "&inprop=url"
    api_link += "&format=json"
    try:
        r = requests.get(api_link).json()
    except:
        return False

    if "query" in r:

        e = r["query"]["pages"]

        for x in e:
            if str(e[x]["title"]).lower() == str(search_for).lower():
                back[x] = {}
                back[x]["title"] = e[x]["title"]
                back[x]["url"] = e[x]["fullurl"]
                break
        else:
            for x in e:
                back[x] = {}
                back[x]["title"] = e[x]["title"]
                back[x]["url"] = e[x]["fullurl"]
        return back
    else:
        return False
