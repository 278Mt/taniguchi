from threading import Lock
from flask import Flask, session, request, copy_current_request_context, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from logger import logger

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None, cors_allowed_origins='*')
thread_lock = Lock()


@app.route('/')
def index():
    return "Server is Running"


def room_of(sid):
    """return sid belonging room
    """
    for r in rooms(sid):
        if r != sid:
            return r
    return '<Not Found>'


@socketio.on('connect')
def on_connect():
    logger.info('connected %s' % request.sid)
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         pass
    # thread
    # socketio.start_background_task(background_thread)


@socketio.on('request_create_room')
def on_create_room(req):
    room_name = req['room_name']
    join_room(room_name)
    logger.info('create room %s' % room_of(request.sid))
    emit('response_create_room', {
         'room_name': room_name, 'id': request.sid}, room=room_name)


@socketio.on('request_join_room')
def on_join_room(req):
    room_name = req['room_name']
    join_room(room_name)
    logger.info('join %s to %s' % (request.sid, room_of(request.sid)))
    emit('response_join_room', {
         'room_name': room_name, 'id': request.sid}, room=room_name)


@socketio.on('request_game_start')
def on_game_start(req):
    room_name = room_of(request.sid)
    logger.info('%s game start' % room_name)
    emit('response_game_start', {}, room=room_name)


@socketio.on('request_game_end')
def on_game_end(req):
    room_name = room_of(request.sid)
    logger.info('%s game end' % room_name)
    emit('response_game_end', {}, room=room_name)


@socketio.on('request_move')
def on_move(req):
    room_name = room_of(request.sid)
    # print_board(req)
    emit('response_board', req, room=room_name)


@socketio.on('disconnect')
def on_disconnect():
    pass
    # logger.info('Client disconnected', request.sid)
