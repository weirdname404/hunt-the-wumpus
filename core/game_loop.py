import random
from core.dungeon import generate_dungeon
from core.events import (
    EventLoop, shoot_arrow,
    check_room_events, check_close_events
)
from core.objects import player

ATACK_ACTION = 1
MOVE_ACTION = 2


def start_game_loop():
    """
    - Generates events in dungeon
    - Revives the player
    - Starts the game loop
    """
    rooms = generate_dungeon()
    player.is_dead = False
    current_room = rooms['1']
    event_loop = EventLoop()
    while True:
        # current_room = player.current_room
        print(f'\nYou are in the room {current_room.num}')
        # check room events
        room_changed, new_room_num = check_room_events(current_room, player)
        if room_changed:
            current_room = rooms[new_room_num]
            continue
        # game over
        if player.is_dead:
            return
        # check close events
        check_close_events(current_room)
        # player is still alive let's do something
        options = set(room.num for room in current_room.connected_rooms.values())
        print(f'Tunnels lead to {" ".join(options)} ')
        # player's action
        print(f'You have {player.arrows} arrow(s).')
        action = ask_to_act(player)
        if action is ATACK_ACTION:
            player.arrows -= 1
            shot_power = ask_shot_power()
            flying_curve = ask_flying_curve(shot_power)
            event_loop.add_event(shoot_arrow(current_room, flying_curve))
        elif action is MOVE_ACTION:
            current_room = rooms[ask_player_to_move_from(current_room, options)]

        # end player's turn
        event_loop.update_events()


def ask_flying_curve(shot_power):
    response = input("List room numbers through which the arrow will fly? ")
    return response.split()[:shot_power]


def ask_shot_power():
    while True:
        response = input("How powerful your shot will be? [1-5] ")
        try:
            power = int(response)
        except ValueError:
            continue
        if power < 1 or power > 5:
            continue
        return power

def ask_player_to_move_from(room, options):
    while True:
        response = input("Where to? ")

        if response not in options:
            continue

        return response


def ask_to_act(player):
    """Asks about next player's action"""
    while True:
        response = input('Shoot or Move? [S/M] ').lower()
        if response == 's':
            if player.arrows < 1:
                print("There are no more arrows left... You must move on.")
                return MOVE_ACTION
            return ATACK_ACTION

        if response == 'm':
            return MOVE_ACTION
        if response == 'w':
            return 3
