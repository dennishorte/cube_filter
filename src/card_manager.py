from card import Card


class CardManager(object):
    def __init__(self, card_filename=None, card_list=None):
        if card_filename:
            self.cards = self._load_cards(card_filename)
        else:
            self.cards = card_list or []

    def get_by_name(self, name):
        return [c for c in self.cards if c.name == name]

    def remove_by_name(self, name):
        for i, card in enumerate(self.cards):
            if card.name == name:
                del self.cards[i]
                return

    def filter(self, func):
        filtered_cards = filter(func, self.cards)
        return CardManager(card_list=filtered_cards)

    def copy(self):
        return CardManager(card_list=self.cards)

    def _load_cards(self, card_filename):
        cards = []
        with open(card_filename, 'r') as fin:
            headers = fin.readline().split(',')

            cmc_index = headers.index('CMC')
            name_index = headers.index('Name')
            type_index = headers.index('Type')
            color_index = headers.index('Color')

            for line in fin:
                if not line.strip():
                    continue

                tokens = line.strip().split(',')

                types = tokens[type_index][1:-1]
                split_types = types.split(' - ')
                if len(split_types) != 2:
                    continue

                supertypes = split_types[0].split()
                subtypes = split_types[1].split()

                card = Card(
                    cmc=tokens[cmc_index],
                    name=tokens[name_index][1:-1],
                    color=tokens[color_index],
                    subtypes=subtypes,
                    supertypes=supertypes,
                )

                cards.append(card)
        return cards

