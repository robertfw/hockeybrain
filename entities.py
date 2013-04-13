class BaseEntity(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.__str__())


class Team(BaseEntity):
    def __str__(self):
        return self.abbrev


class Player(BaseEntity):
    def __str__(self):
        return '{number} {name}'.format(number=self.number, name=self.name)
