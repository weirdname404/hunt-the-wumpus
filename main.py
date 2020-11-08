from core.dungeon import generate_dungeon
from core.objects import player
from core.events import GAME_OVER
from text_lines import events_text, intro


def start_game_loop():
    rooms = generate_dungeon()
    current_room = rooms[1]
    while True:
        if player.dead:
            print(events_text[GAME_OVER])
            return
        print(f'\nYou are in the room {current_room.uid}')
        for event in current_room.events:
            print(events_text[event])
        action = ask_player_to_act()
        if action is 1:
            pass
        if action is 2:
            current_room = rooms[ask_player_to_move_from(current_room)]


def start_game():
    print(intro)
    while True:
        start_game_loop()
        if (answer := ask_player_to_restart()) is False:
            break


def ask_player_to_move_from(room):
    options = set(str(room.uid) for room in room.connected_rooms.values())
    while True:
        print(f'\nYou can go to the following rooms: {" ".join(options)} ')
        response = input("Where to? ")

        if response not in options:
            continue
        return int(response)


def ask_player_to_act():
    while True:
        response = input('Shoot or Move? [S/M] ').lower()
        if response == 's':
            return 1
        if response == 'm':
            return 2


def ask_player_to_restart():
    while True:
        response = input("\nRestart? [y/N] ")
        if response == 'N':
            return False
        elif response == 'y' or response == 'Y':
            return True


if __name__ == "__main__":
    start_game()
