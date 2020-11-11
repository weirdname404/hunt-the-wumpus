# hunt-the-wumpus

This is a text adventure based on the original ["Hunt the Wumpus"](https://en.wikipedia.org/wiki/Hunt_the_Wumpus) game. This version of the game offers some new features and rule modifications. The game is turn based.

## How to run the game

- You need Python 3 installed on your system.
- To start the game just run `python3 main.py`

## Game

You are a hunter that decided to enter the dungeon to kill the horrendous lurking beast(s) known as Wumpus. You are not the first one who dared to challenge the great Wumpus. Dungeon consists of a 20 rooms where each room is connected to 3 other rooms (the dungeon is modeled after the vertices of a dodecahedron).

Take this [map](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Hunt_the_Wumpus_map.svg/1024px-Hunt_the_Wumpus_map.svg.png) to naviagate in the dungeon.

You can move between rooms, shoot arrows or wait. A real hunter is best at waiting.
Furthermore, there are some gold coins in the dungeon, try to find them all.

### Threats

You can sense threats in near rooms:
- you can smell Wumpus;
- hear bats;
- feel cold wind from the deadly pit;

If you enter the room with Wumpus, you will awake it. Awaken beast can attack you or regroup by moving to one of the nearest rooms. You've never met a hunter who survived the Wumpus attack.

You can meet huge bats in the dungeon that will pick you up and move to a random room.

It is pretty dark in the dungeon, so you will not notice deadly pits and probably fall in. Be careful.

### Movement

Yor are always aware in what room you are currently in and you always see tunnels that lead to connected rooms.

```
You are in the room 1
Tunnels lead to 8 2 5 
You have 3 arrow(s).
Shoot, Move or Wait? [s/m/w] m
Where to? 2
```

### Combat

There are 3 magic arrows in your quiver. 
You can adjust the number of rooms it will fly by choosing the power of the shot.
Moreover, you can enchant the flying arrow curve by listing the number of rooms through which it will fly. If you make a mistake while enchanting an arrow, the arrow will fly randomly.

 **BE CAREFULL FLYING ARROW CAN KILL YOU!**

```
You are in the room 1
You feel a slight draft
Tunnels lead to 2 8 5 
You have 3 arrow(s).
Shoot, Move or Wait? [s/m/w] s
How powerful your shot will be? [1-5] 5
List room numbers through which the arrow will fly? 2 3 4 5 1
```

It is very hard to kill Wumpus in a close combat. A good strategy might be to weaken it by shooting from a distance with your bow. Moreover, shooting is not enough and you have to find wounded beast and finish it.

If you are shooting from the next room where Wumpus lurks, there is a chance that beast will notice you shooting and change the room or attack you.
Moreover, if the arrow flew nearby the room with Wumpus, there is a chance it will awake the beast.

You can run out of arrows, but you can pick them up to continue the hunt.

### Additional info

You can modify `config.py` to experiment with the game by:
- spawning several beasts;
- making more threat rooms;
- setting more arrows;

You can even cheat by revealing beasts' location(s).
