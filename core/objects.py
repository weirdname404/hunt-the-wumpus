from config import ARROWS


class Room:
    __slots__ = ('num', 'events', 'connected_rooms')

    def __init__(self, num):
        self.num = str(num)
        self.connected_rooms = {}
        self.events = set()

    def __repr__(self):
        return self.num


class Player:
    __slots__ = ('arrows', 'is_dead', 'gold', 'kills')

    def __init__(self):
        self.arrows = ARROWS
        self.is_dead = False
        self.gold = 0
        self.kills = 0


class BeastMap:
    __slots__ = ('beasts',)

    def __init__(self):
        self.beasts = {}

    def __getitem__(self, v):
        return self.beasts[v]

    def __setitem__(self, k, v):
        self.beasts[k] = v

    def clear(self):
        self.beasts.clear()


beast_map = BeastMap()
