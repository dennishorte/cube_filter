import sys

class Card(object):
    def __init__(self, name, supertypes, subtypes, color, cmc):
        self.name = name
        self.supertypes = supertypes
        self.subtypes = subtypes
        self.color = color
        self.cmc = cmc

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


metatribe_names = [
    'jcc',
    'myth',
    'bs',
    'human',
    'animal',
]


def load_metatribes(filename):
    tribe_to_type = {}
    type_to_tribe = {}
    
    with open(filename, 'r') as fin:
        for line in fin:
            if not line.strip():
                continue
            typ, tribe = line.strip().split()
            tribe_to_type.setdefault(tribe, []).append(typ)
            type_to_tribe[typ] = tribe

    return tribe_to_type, type_to_tribe


def load_cardfile():
    cards = []
    with open('CubeLegacyClassic.csv', 'r') as fin:
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


def get_card_by_name(card_list, name):
    for card in card_list:
        if card.name == name:
            return card

    raise RuntimeError('Card not found: {}'.format(name))


def remove_card_by_name(card_list, name):
    for i, card in enumerate(card_list):
        if card.name == name:
            del card_list[i]
            return


def add_special_types(creatures, tribe_to_creatures):
    with open('special_tribes.txt', 'r') as fin:
        for line in fin:
            if line.strip():
                name, tribes = line.strip().split(':')
                tribes = tribes.split(',')
                for tribe in tribes:
                    tribe_to_creatures[tribe].add(get_card_by_name(creatures, name))


def sort_creatures_by_metatribe(creatures, type_to_tribe):
    tribe_to_creatures = {}
    for c in creatures:
        for subtype in c.subtypes:
            tribe = type_to_tribe[subtype]
            if tribe in metatribe_names:
                tribe_to_creatures.setdefault(tribe, set()).add(c)

    add_special_types(creatures, tribe_to_creatures)
    
    return tribe_to_creatures


def load_culls():
    culls = []
    with open('culls.txt', 'r') as fin:
        for line in fin:
            if line.strip():
                card_name = line.split('#')[0].strip()
                culls.append(card_name)

    return culls


def remove_culls(card_list, culls):
    for card_name in culls:
        remove_card_by_name(card_list, card_name)


def analyze_cards():
    cards = load_cardfile()
    culls = load_culls()
    tribe_to_type, type_to_tribe = load_metatribes('types.txt')

    creatures = [c for c in cards if 'Creature' in c.supertypes]
    remove_culls(creatures, culls)

    tribe_to_creatures = sort_creatures_by_metatribe(creatures, type_to_tribe)

    # Check if we're accidentally culling JCC creatures
    for card_name in culls:
        for jcc_card in tribe_to_creatures['jcc']:
            if card_name == jcc_card.name:
                print("Culling JCC creature: {}".format(card_name))


    for tribe, creatures in tribe_to_creatures.items():
        print('{}: {}'.format(tribe, len(creatures)))


def print_metatribe(tribe_to_creatures, tribe):
    tribe_creatures = tribe_creatures[tribe]


if __name__ == "__main__":
    analyze_cards()
