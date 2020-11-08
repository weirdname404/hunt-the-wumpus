from config import ARROWS


class Room:
    def __init__(self, uid):
        self.uid = uid
        self.connected_rooms = {}
        self.events = []


class Arrow:
    def __init__(self, pos, flying_route):
        self.pos = pos


class Player:
    def __init__(self):
        self.arrows = ARROWS
        self.dead = False


player = Player()