from core.events import generate_events
from core.objects import Room


def generate_dungeon():
    """
    Dungeon has a form of dodecahedron with 20 rooms.
    Every room in a dungeon has only 3 tunnels or connections with other rooms.
    Dungeon structure is following:
    - Center circle has 5 connected rooms;
    - Middle circle has 10 connected rooms. Every room with even number is connected with
      the room from center circle;
    - Outer circle has 5 connected rooms. Every room is connected with a room from middle circle
      with odd number.
    """
    center_circle = _generate_circle_rooms(1, 5)
    middle_circle = _generate_circle_rooms(6, 15, center_circle)
    outer_circle = _generate_circle_rooms(16, 20, middle_circle)

    rooms =  {
        room.num: room
        for room in (*center_circle, *middle_circle, *outer_circle)
    }

    for room_num, event in generate_events():
        rooms[room_num].events.add(event)

    return rooms


def _generate_circle_rooms(first_room, last_room, inner_circle=None):
    circle = []
    prev_room = None
    if inner_circle is not None:
        inner_circle_l = len(inner_circle)
        inner_i = inner_circle_l - 1

    for num in range(first_room, last_room + 1):
        room = Room(num)
        # connects center and middle circles
        if num > 5 and num < 16 and num % 2 == 0:
            _link_rooms(inner_circle[inner_i % inner_circle_l], room)
            inner_i += 1
        # connects middle and outer circle
        elif num > 15:
            _link_rooms(inner_circle[inner_i % inner_circle_l], room)
            inner_i += 2
        if prev_room is not None:
            _link_rooms(prev_room, room)
        circle.append(room)
        prev_room = room

    _link_rooms(circle[0], circle[-1])
    return circle


def _link_rooms(room_a, room_b):
    room_a.connected_rooms[room_b.num] = room_b
    room_b.connected_rooms[room_a.num] = room_a
