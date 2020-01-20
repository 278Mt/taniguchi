import sys
import time
from client import api, connect, create_room, join_room, game_start, game_end, move

ENDPOINT = 'https://vendredi-noir.herokuapp.com'
# ENDPOINT = 'http://localhost:5000'

global started

def mock():
    """
    """
    return {
        "score": 120,
        "falling":  {
            "type": "O",
            "pos": [3, 5]
        },
        "next": "J",
        "board": [
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000000",
            "0000000001",
            "0000003301",
            "0000033201",
            "0011112221",
        ],
        "isDead": False
    }


def prettify_board(res):
    return res
    # t, pos = res['falling']['type'], res['falling']['pos']
    # # return '%s (%s, %s)\n%s' % (t, pos[0], pos[1], '\n'.join(res['board']))
    # return '%s (%s, %s)' % (t, pos[0], pos[1])


"""
Event Handlers
"""
@api('connected')
def connected():
    print('[Connected]')


@api('disconnected')
def disconnected():
    print("[Disconnected]")
    sys.exit()


@api('room_created')
def room_created(res):
    print('created')


@api('room_joined')
def room_joined(res):
    print('joined')


@api('updated')
def update(res):
    print(prettify_board(res))


@api('game_started')
def game_started(res):
    print('game started')
    global started
    started = True


@api('game_ended')
def game_ended(res):
    print('game ended')
    sys.exit()


"""
Usage:
# as host
python client_example.py
# as member
python client_example.py --join
"""
if __name__ == '__main__':
    connect(ENDPOINT)
    global started
    started = False
    room_name = 'AAA'
    is_host = not (len(sys.argv) >= 2 and sys.argv[1] == '--join')

    if is_host:
        create_room(room_name)
    else:
        join_room(room_name)

    if is_host:
        print('matching 10s ...')
        time.sleep(10)

        game_start(room_name)
    else:
        while not started:
            print('waiting start ... %s' % started)
            time.sleep(1)

    i = 5
    while i > 0:
        i -= 1
        move(input())

    if is_host:
        game_end(room_name)
