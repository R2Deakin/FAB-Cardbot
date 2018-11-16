from holocron.swdestiny import (
    Cards,
    Formats,
    Sets,
)

CARDS = None
FORMATS = None
SETS = None


def refresh():
    """
    Refresh the cache.
    """
    global CARDS
    global FORMATS
    global SETS

    print('Rebuilding cache...')

    try:
        formats_resp = Formats().all()['data']
        card_resp = Cards().all()['data']
        sets_resp = Sets().all()['data']
    except Exception:
        print('SWDestinyDB requests failed. Aborting cache refresh.')
        return

    CARDS = {c['name']: c for c in card_resp}
    FORMATS = {f['code']: f['name'] for f in formats_resp}
    SETS = {f['code']: f['name'] for f in sets_resp}

    print('Cache rebuilt')

refresh()
