import requests


def get(lien):
    """get text of uri"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'
    }
    reponse = requests.get(lien, headers=headers)
    reponse.encoding="utf-8"
    if reponse.status_code == 200:
        return 200, reponse.text

    return reponse.status_code, ""
