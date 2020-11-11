from core.actions import ATACK, MOVE, WAIT
from core.coroutines import shoot_arrow
from core.dungeon import generate_dungeon, generate_events_and_beasts
from core.events import check_room_events, check_close_events
from core.event_loop import event_loop
from core.objects import Player, beast_map
from config import WUMPUSES


def start_game_loop():
    """
    - Removes garbage
    - Generates events in dungeon
    - Revives the player
    - Starts the game loop
    """
    # Removes garbage
    event_loop.clear()
    beast_map.clear()
    # generate events in rooms
    rooms = generate_dungeon()
    generate_events_and_beasts(rooms)
    player = Player()
    current_room = rooms['1']
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
        # WIN
        if player.kills == WUMPUSES:
            text = "You won! You have found {} gold coins and killed {} monster(s) known as Wumpus"
            print(text.format(player.gold, player.kills))
            return
        # check close events
        check_close_events(current_room)
        # player is still alive let's do something
        options = set(
            room.num for room in current_room.connected_rooms.values()
        )
        print(f'Tunnels lead to {" ".join(options)} ')
        # player's action
        print(f'You have {player.arrows} arrow(s).')
        action = ask_to_act(player)
        if action is ATACK:
            player.arrows -= 1
            shot_power = ask_shot_power()
            flying_curve = ask_flying_curve(shot_power)
            event_loop.add_event(shoot_arrow(current_room, flying_curve))
        elif action is MOVE:
            next_room_num = ask_player_to_move_from(current_room, options)
            current_room = rooms[next_room_num]

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
        response = input('Shoot, Move or Wait? [s/m/w] ').lower()
        if response == 's':
            if player.arrows < 1:
                print("There are no more arrows left... You must move on.")
                return MOVE
            return ATACK

        if response == 'm':
            return MOVE
        if response == 'w':
            return WAIT
