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
