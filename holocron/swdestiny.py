import requests


BASE_URI = 'https://swdestinydb.com/api/public'

class SWDBResource(object):
    """
    This object represents a resource in the SWDestinyDB API.
    """
    location = None

    def __init__(self):
        pass

    def all(self, **params):
        uri = BASE_URI + self.location
        return requests.get(uri, params=params).json()

    def fetch(self, key, **params):
        # Hack. Chop off last character to make instance uri.
        instance_location = self.location[:-1]
        uri = BASE_URI + instance_location + '/{}'.format(key)
        print('Fetching {}'.format(uri))
        return requests.get(uri, params=params).json()


class Cards(SWDBResource):
    location = '/cards'

class Formats(SWDBResource):
    location = '/formats'

class Sets(SWDBResource):
    location = '/sets'
