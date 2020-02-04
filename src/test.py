from card_manager import CardManager
from metatribe_manager import MetatribeManager


class Culler(object):
    def __init__(self, cull_filename):
        self.card_names = self._load_culls(cull_filename)

    def _load_culls(self, filename):
        with open(filename, 'r') as fin:
            lines = fin.readlines()

        card_lines = [x.strip() for x in lines if len(x) > 50]
        card_names = [x[4:35].strip() for x in card_lines]
        return card_names

    def __call__(self, card):
        return card.name in self.card_names
        


def print_cards(card_list):
    for index, card in enumerate(card_list):
        print('{:2}. {:30} {:20} {:5} {:3}'.format(
            index,
            card.name,
            ', '.join(card.subtypes),
            card.color,
            card.cmc
        ))


def show_beasts(cm):
    beasts = cm.filter(lambda x: 'Beast' in x.subtypes)
    print_cards(beasts.cards)


def show_animals(cm, mm):
    animals = cm.filter(lambda x: mm.is_animal(x))
    animals.cards.sort(key=lambda x: x.cmc)
    print_cards(animals.cards)

    
def show_humans(cm, mm):
    humans = cm.filter(lambda x: mm.is_human(x))
    humans.cards.sort(key=lambda x: x.cmc)
    print_cards(humans.cards)


def show_bs(cm, mm):
    bs = cm.filter(lambda x: mm.is_bs(x))
    bs.cards.sort(key=lambda x: x.cmc)
    print_cards(bs.cards)
    

def run_test():
    cm = CardManager(card_filename='res/CubeLegacyClassic.csv')
    mm = MetatribeManager(
        type_to_tribe_filename='res/types.txt',
        special_tribes_filename='res/special_tribes.txt',
    )
    culler = Culler(cull_filename='res/culls_v2.txt')

    creatures = cm.filter(lambda x: 'Creature' in x.supertypes)
    culled = creatures.filter(lambda x: not culler(x))
    jcc = culled.filter(lambda x: mm.is_jcc(x))
    non_jcc = culled.filter(lambda x: not mm.is_jcc(x))


    print('creatures: {}'.format(len(creatures.cards)))
    print('non-jcc  : {}'.format(len(non_jcc.cards)))
    print('jcc      : {}'.format(len(jcc.cards)))
    print('culls    : {}'.format(len(culler.card_names)))
    print('-----')
    
    tribes = mm.split_by_tribe(non_jcc.cards)
    del tribes['jcc']
    for t, cs in tribes.items():
        print('{:6}: {}'.format(t, len(cs)))

    remaining = non_jcc.filter(lambda x: not mm.is_myth(x))
    remaining = remaining.filter(lambda x: not mm.is_animal(x))
    remaining = remaining.filter(lambda x: not mm.is_human(x))
        

if __name__ == "__main__":
    run_test()
