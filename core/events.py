from random import sample
from config import (
    WUMPUSES, BAT_ROOMS, PIT_ROOMS,
    LOST_ARROW_ROOMS, GOLD_ROOMS
)

# ids
WUMPUS_EVENT = 1
BATS_EVENT = 2
PIT_EVENT = 3
ARROW_EVENT = 4
GOLD_EVENT = 5
GAME_OVER = 6


def generate_events():
    # events can happen in any room except start room
    room_uid_iter = iter(sample(range(2, 21), 19))
    events = (
        (WUMPUS_EVENT, WUMPUSES),
        (BATS_EVENT, BAT_ROOMS),
        (PIT_EVENT, PIT_ROOMS),
        (ARROW_EVENT, LOST_ARROW_ROOMS),
        (GOLD_EVENT, GOLD_ROOMS)
    )
    for event, events_number in events:
        for _ in range(events_number):
            yield (next(room_uid_iter), event)
