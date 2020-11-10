import random


def get_random_close_room(room):
    connected_rooms = room.connected_rooms
    connected_rooms_keys = list(connected_rooms.keys())
    return connected_rooms[random.choice(connected_rooms_keys)]


def get_random_room_num():
    return str(random.randint(1, 21))


def get_random_room_num_iter():
    return iter(map(str, random.sample(range(1, 21), 19)))


def get_uid_generator():
    uid = 0
    while True:
        yield uid
        uid += 1


uid_generator = get_uid_generator()
