from card_manager import CardManager
from metatribe_manager import MetatribeManager


def run_test():
    cm = CardManager(card_filename='res/CubeLegacyClassic.csv')
    mm = MetatribeManager(
        type_to_tribe_filename='res/types.txt',
        special_tribes_filename='res/special_tribes.txt',
    )

    creatures = cm.filter(lambda x: 'Creature' in x.supertypes)
    jcc = creatures.filter(lambda x: mm.is_jcc(x))

    print('creatures: {}'.format(len(creatures.cards)))
    print('jcc      : {}'.format(len(jcc.cards)))


if __name__ == "__main__":
    run_test()
