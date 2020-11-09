from text_lines import intro
from core.game_loop import start_game_loop


def start_game():
    print(intro)
    while True:
        start_game_loop()
        if (answer := ask_player_to_restart()) is False:
            break


def ask_player_to_restart():
    while True:
        response = input("\nRestart? [y/N] ")
        if response == 'N':
            return False
        elif response == 'y' or response == 'Y':
            return True


if __name__ == "__main__":
    start_game()
