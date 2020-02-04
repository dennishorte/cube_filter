from card import Card


class MetatribeManager(object):
    metatribe_names = [
        'jcc',
        'myth',
        'bs',
        'human',
        'animal',
    ]

    def __init__(self, type_to_tribe_filename, special_tribes_filename):
        self.special_tribes = {}
        self.tribe_to_type = {}
        self.type_to_tribe = {}

        self._load_special_tribes(special_tribes_filename)
        self._load_type_to_tribe(type_to_tribe_filename)

    def _load_special_tribes(self, filename):
        with open(filename, 'r') as fin:
            for line in fin:
                if not line.strip():
                    continue

                name, tribes = line.strip().split(':')
                self.special_tribes[name] = tribes.split(',')

    def _load_type_to_tribe(self, filename):
        with open(filename, 'r') as fin:
            for line in fin:
                if not line.strip():
                    continue
                typ, tribe = line.strip().split()
                self.tribe_to_type.setdefault(tribe, []).append(typ)
                self.type_to_tribe[typ] = tribe

    def is_jcc(self, card):
        return self.is_metatribe(card, 'jcc')

    def is_myth(self, card):
        return self.is_metatribe(card, 'myth')

    def is_bs(self, card):
        return self.is_metatribe(card, 'bs')

    def is_human(self, card):
        return self.is_metatribe(card, 'human')

    def is_animal(self, card):
        return self.is_metatribe(card, 'animal')

    def is_metatribe(self, card, tribe):
        return tribe in self.card_tribes(card)

    def split_by_tribe(self, card_list):
        tribes = {tribe: set() for tribe in MetatribeManager.metatribe_names}
        for tribe in tribes:
            for card in card_list:
                if self.is_metatribe(card, tribe):
                    tribes[tribe].add(card)
        return tribes
        

    def card_tribes(self, card):
        tribes = [self.type_to_tribe[x] for x in card.subtypes]
        tribes += self.special_tribes.get(card.name, [])
        tribes = filter(lambda x: x in MetatribeManager.metatribe_names, tribes)
        return list(set(list(tribes)))


if __name__ == "__main__":
    metatribe_manager = MetatribeManager('types.txt', 'special_tribes.txt')
