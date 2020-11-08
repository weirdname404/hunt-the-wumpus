import random
import config
import logging as log
from core.actions import GET_DAMAGE, MOVE, AWAKE, DIE
from core.events import (
    WUMPUS_EVENT, WUMPUS_WOUNDED, ARROW_EVENT, LOST_ARROW_EVENT
)
from core.objects import beast_map
from core.utils import (
    get_random_close_room, uid_generator
)

if config.ISeeDeadPeople:
    log.basicConfig(format='%(message)s', level=log.INFO)
else:
    log.basicConfig(format='%(message)s')


class Wumpus:
    def __init__(self, current_room, uid):
        self.current_room = current_room
        self.uid = uid

    def listen(self):
        uid = self.uid
        dead = False
        while True:
            log.info(f"\nwumpus {uid} is in room {self.current_room.num}")
            action = yield
            if dead:
                break
            if action is GET_DAMAGE:
                log.info(f"wumpus {uid} gets damage")
                self.current_room.events.remove((uid, WUMPUS_EVENT))
                self.current_room.events.add((uid, WUMPUS_WOUNDED))
            elif action is MOVE:
                log.info(f"wumpus {uid} moves")
                self.move_randomly()
            elif action is AWAKE:
                log.info(f"wumpus {uid} is awaken")
                # if wumpus is awaken it is a chance that it will change room
                if random.randint(1, 100) <= 60:
                    self.move_randomly()
            elif action is DIE:
                self.current_room.events.remove((uid, WUMPUS_WOUNDED))
                dead = True

    def move_randomly(self):
        self.current_room.events.remove((self.uid, WUMPUS_EVENT))
        self.current_room = get_random_close_room(self.current_room)
        self.current_room.events.add((self.uid, WUMPUS_EVENT))


def shoot_arrow(start_room, route):
    """Arrow flies by a given route or randomly"""
    current_room = start_room
    arrow_uid = next(uid_generator)
    arrow_event = (arrow_uid, ARROW_EVENT)
    # flying path
    for room_num in route:
        # if player's room number is not valid, choose next room randomly
        if (next_room := current_room.connected_rooms.get(room_num)) is None:
            next_room = get_random_close_room(current_room)

        if current_room is not start_room:
            current_room.events.remove(arrow_event)

        # shooting or flying arrow might awake nearby beasts
        _awake_nearby_beasts(current_room)

        current_room = next_room
        current_room.events.add(arrow_event)
        # check if arrow hit Wumpus
        hit_wumpus = False
        for uid, event in current_room.events.copy():
            if event is WUMPUS_EVENT:
                hit_wumpus = True
                beast_map[uid].send(GET_DAMAGE)
        # if arrow hit wumpus it should stop flying
        if hit_wumpus:
            break
        yield None

    # arrow falls on the floor
    current_room.events.remove(arrow_event)
    current_room.events.add(
        (next(uid_generator), LOST_ARROW_EVENT)
    )
    _awake_nearby_beasts(current_room)


def _awake_nearby_beasts(current_room):
    for room in current_room.connected_rooms.values():
        for uid, event in room.events.copy():
            if event is WUMPUS_EVENT:
                beast_map[uid].send(AWAKE)
