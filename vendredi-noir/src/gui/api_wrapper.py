"""
Socket Rooming API
@author: wakame-tech
"""

from socketio import Client

import os
import time
import sys
import json
import numpy as np
from functools import wraps


sio = Client()
handlers = {}

# decorator


def event(key):
    def _register(function):
        @wraps(function)
        def __register(*args, **kwargs):
            return function(*args, **kwargs)
        handlers[key] = function

    return _register


class Api:
    def __init__(self):
        @sio.event
        def on_connect():
            if 'connected' in handlers:
                handlers['connected'](self)

        @sio.event
        def on_disconnect():
            if 'disconnected' in handlers:
                handlers['disconnected'](self)

        @sio.on('response_create_room')
        def on_create_room(res):
            if 'room_created' in handlers:
                handlers['room_created'](self, res)

        @sio.on('response_join_room')
        def on_join_room(res):
            if 'room_joined' in handlers:
                handlers['room_joined'](self, res)

        @sio.on('response_game_start')
        def on_game_start(res):
            if 'game_started' in handlers:
                handlers['game_started'](self, res)

        @sio.on('response_game_end')
        def on_game_end(res):
            if 'game_ended' in handlers:
                handlers['game_ended'](self, res)

        @sio.on('response_board')
        def on_board(res):
            if 'updated' in handlers:
                payload = json.loads(res)
                handlers['updated'](self, payload)

    @property
    def socketid(self):
        return sio.sid

    def connect(self, endpoint):
        sio.connect(endpoint)

    def create_room(self, room_name):
        print(f'[Create] {room_name}')
        sio.emit('request_create_room', {"room_name": room_name})

    def join_room(self, room_name):
        """
        """
        print(f'[Join] to {room_name}')
        sio.emit('request_join_room', {"room_name": room_name})

    def game_start(self, room_name):
        """
        """
        print('[Game Start]')
        sio.emit('request_game_start', {"room_name": room_name})

    def game_end(self, room_name):
        """
        """
        print('[Game End]')
        sio.emit('request_game_end', {"room_name": room_name})

    def send_state(self, req):
        """
        """
        print('[Update]')
        payload = json.dumps(req)
        sio.emit('request_move', payload)
