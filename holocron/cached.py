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
        formats_resp = Formats().all()
        card_resp = Cards().all()
        sets_resp = Sets().all()
    except Exception as e:
        print('SWDestinyDB requests failed. Aborting cache refresh.')
        print(e)
        return

    CARDS = {c['label']: c['set_code'] c for c in card_resp}
    FORMATS = {f['code']: f['name'] for f in formats_resp}
    SETS = {f['code']: f['name'] for f in sets_resp}

    print('Cache rebuilt')

refresh()
