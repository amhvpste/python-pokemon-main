import requests

_move_cache = {}

class Move:
    def __init__(self, url):
        if url in _move_cache:
            data = _move_cache[url]
        else:
            response = requests.get(url)
            data = response.json()
            _move_cache[url] = data

        self.name = data['name']
        self.power = data['power']
        self.type = data['type']['name']
