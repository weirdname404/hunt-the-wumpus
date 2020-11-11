import random
import config
from core.actions import DIE, MOVE
from core.objects import beast_map
from core.utils import get_random_room_num

# ids
WUMPUS_EVENT = 1
BATS_EVENT = 2
PIT_EVENT = 3
ARROW_EVENT = 4
GOLD_EVENT = 5
DEATH = 6
LOST_ARROW_EVENT = 7
NO_ADVENTURES = 8
SWEETROLL_EVENT = 9
WUMPUS_ATTACK_SUCCESS = 10
WUMPUS_ATTACK_FAIL = 11
WUMPUS_FLEE = 12
ITEM_EVENT = 13
GARBAGE = 14
WUMPUS_WOUNDED = 15

EVENT_IS_NEAR = {
    WUMPUS_EVENT: "You smell something disgusting. You'd better be careful.",
    PIT_EVENT: "You feel a slight draft",
    BATS_EVENT: "You hear a flapping sound. There may be bats nearby."
}
EVENT_OCCURS = {
    ITEM_EVENT: "You found something...",
    GARBAGE: "It's just a pile of bones.",
    NO_ADVENTURES: "Suddenly you don't feel like being an adventurer anymore...",
    DEATH: "You died...",
    WUMPUS_EVENT: "You see Wumpus... It is awaken...",
    WUMPUS_ATTACK_SUCCESS: "In one jump it gets you and blows your head off.",
    WUMPUS_ATTACK_FAIL: "It attacks you but you manage to evade the attack.",
    WUMPUS_FLEE: "It disappears in the darkness.",
    WUMPUS_WOUNDED: "You found heavy wounded Wumpus. You finish it with your dagger.",
    BATS_EVENT: "Huge bats lift you up in the air and carry you in an unknown direction.",
    PIT_EVENT: "You fall into a pit. You broke some bones and you can't get out...",
    ARROW_EVENT: "You hear a loud whistle and see a flying arrow. You took an arrow in the knee.",
    GOLD_EVENT: "What a luck! You've found a shiny gold coin.",
    SWEETROLL_EVENT: "You found a sweetroll.",
    LOST_ARROW_EVENT: "You found a magic arrow. It's hard to tell how long it's been there."
}

EVENTS = (
    (WUMPUS_EVENT, config.WUMPUSES),
    (BATS_EVENT, config.BAT_ROOMS),
    (PIT_EVENT, config.PIT_ROOMS),
    (LOST_ARROW_EVENT, config.LOST_ARROW_ROOMS),
    (ITEM_EVENT, config.ITEM_ROOMS)
)


def check_room_events(room, player):
    res = (False, None)
    # we are dynamically changing room events
    for uid, event in room.events.copy():
        print(EVENT_OCCURS[event])
        if event is LOST_ARROW_EVENT:
            player.arrows += 1
            room.events.remove((uid, event))
        # found something
        elif event is ITEM_EVENT:
            roll = random.randint(1, 100)
            room.events.remove((uid, event))
            if roll <= 3:
                print(EVENT_OCCURS[SWEETROLL_EVENT])
            elif 3 > roll <= 40:
                player.gold += 1
                print(EVENT_OCCURS[GOLD_EVENT])
            else:
                print(EVENT_OCCURS[GARBAGE])
        # wounded wunpus
        elif event is WUMPUS_WOUNDED:
            player.kills += 1
            beast_map[uid].send(DIE)
        # wumpus is healthy and ready to fight
        elif event is WUMPUS_EVENT:
            # there is a chance that wumpus will atack or flee
            if random.randint(1, 100) <= 75:
                # there is a chance that player can evade the attack
                if random.randint(1, 100) <= 10:
                    print(EVENT_OCCURS[WUMPUS_ATTACK_FAIL])
                else:
                    print(EVENT_OCCURS[WUMPUS_ATTACK_SUCCESS])
                    player.is_dead = True
            else:
                print(EVENT_OCCURS[WUMPUS_FLEE])
                beast_map[uid].send(MOVE)
        # other events
        elif event is PIT_EVENT:
            player.is_dead = True
            print(EVENT_OCCURS[DEATH])
        elif event is ARROW_EVENT:
            player.is_dead = True
            print(EVENT_OCCURS[NO_ADVENTURES])
        elif event is BATS_EVENT:
            res = (True, get_random_room_num())

    return res


def check_close_events(current_room):
    for room in current_room.connected_rooms.values():
        for _, event in room.events:
            if (text := EVENT_IS_NEAR.get(event)) is not None:
                print(text)
