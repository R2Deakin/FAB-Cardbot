import re

from discord import Embed

from holocron.cached import (
    FORMATS,
    SETS,
)


CARD_VIEW_TEMPLATE = 'http://swdestinydb.com/card/{code}'


class CardEmbed(object):
    """
    Represents an embed for a single card, to be rendered and returned.
    as a response to a search query.

    Crucially, and perhaps somewhat awkwardly, this class overrides
    `__getattr__` to forward missing attribute access to its card object. This
    little bit of magic makes card attribute accesses shorter and cleaner.  """

    def __init__(self, card):
        self.card = card

        if card['subtitle'] is None:
            card['subtitle'] = ''
            pass

        # This is a discord.py Embed object, and is the thing we
        # will be building.
        self.embed = Embed(
            type='rich',
            title=card['name'] + ' - ' + card['subtitle'],
            url=self.url(card),
        )

    def image(self, card):
        return card.get(
            'imagesrc'
        )

    def url(self, card):
        return CARD_VIEW_TEMPLATE.format(code=self.code)

    def __getattr__(self, attr):
        """
        This allows code like `f = self.faction_cost` instead of
        `f = self.card['faction_cost']`.
        """
        return self.card[attr]

    def has(self, name):
        return name in self.card


class CardImage(CardEmbed):
    """
    Returns an embed with a full size card image.
    """
    def render(self):
        self.embed.set_image(url=self.image(self.card))
        return self.embed


class CardText(CardEmbed):
    """
    This is the default embed.

    This returns an embed with a textual representation of the card's text. It
    also includes a link to the card on NetrunnerDB as well as a thumbnail of
    the card image.
    """
    def type_line(self):
        """
        Constructs a card's type line that contains both the card's
        type and subtypes, as well as costs to play it.

        Example:

        `Ice: Sentry - Tracer - Observer • Rez: 4 • Strength: 4 • Influence: 2`
        """
        parts = [self.card['type_code'].title()]
        if self.has('keywords'):
            parts.append(f': {self.card["keywords"]}')

        type_code = self.type_code

        lines = {
            'character': ['Faction: {faction_name}', 'Affiliation: {affiliation_name}', 'Health: {health}', 'Points: {points}'],
            'upgrade': ['Faction: {faction_name}', 'Affiliation: {affiliation_name}', 'Cost: {cost}'],
            'downgrade': ['Faction: {faction_name}', 'Affiliation: {affiliation_name}', 'Cost: {cost}'],
            'support': ['Faction: {faction_name}', 'Affiliation: {affiliation_name}', 'Cost: {cost}'],
            'event': ['Faction: {faction_name}', 'Affiliation: {affiliation_name}', 'Cost: {cost}'],
            'battlefield': ['Faction: {faction_name}', 'Affiliation: {affiliation_name}'],
            'plot': ['Faction: {faction_name}', 'Affiliation: {affiliation_name}', 'Points: {points}'],
        }

        parts.extend((' • ' + s).format(**self.card) for s in lines[type_code])
        return ''.join(parts)


    def text_line(self):
        result = self.text if self.has('text') else '(no text)'
        clean = re.compile('<.*?>')
        return re.sub(clean, '', result)

    def footer_line(self):
        """
        This constructs the footer which contains faction membership, cycle
        membership and position, cycle rotations, and the latest MWL entry.

        Example:

        `Neutral • Meg Owenson • Data and Destiny 26 • Restricted (MWL 2.1)`
        """

        footer = self.illustrator;
        return footer

    def render(self):
        """
        Builds and returns self.embed.

        A call to self.embed.render() will serialize all of the content
        into a dict suitable to sending to Discord's API.
        """
        self.embed.add_field(
            name=self.type_line(),
            value=self.text_line(),
        )
        self.embed.set_thumbnail(url=self.image(self.card))
        self.embed.set_footer(text=self.footer_line())
        return self.embed
