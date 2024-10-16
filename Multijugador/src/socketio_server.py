from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
from flask_session import Session
from nanoid import generate
from src.controllers.game_controller import GameController

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CC3S2 -  Grupo 3'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False)
games = {}  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/<id>/<player>')
def game_room(id, player):
    return render_template('gameRoom.html', id=id, player=player)

@socketio.on('connect')
def handle_connect():
    pass  

@socketio.on('new_game')
def create_game():
    id = generate(size=5)  
    games[id] = {
        "game": GameController('player1', 'player2'),
        "players_ready": 0
    }
    join_room(id)
    emit('juego_actual', {'id': id, 'room': id, 'player': 'player1'}, broadcast=False)

@socketio.on('place_ships')
def handle_place_ships(d):
    if 'room_id' in d:
        room_id = d['room_id']
    else:
        return

    if room_id not in games:
        return

    game = games[room_id]["game"]
    player = d['player']

    game.place_ships(player, d['board'])

    games[room_id]["players_ready"] += 1
    if games[room_id]["players_ready"] > 1:
        emit('start_game', {'room_id': room_id})

@socketio.on('attack')
def handle_attack(data):
    room_id = data['room_id']
    if room_id not in games:
        return  

    game = games[room_id]["game"]
    player = data['player']
    otherPlayer = 'player2' if player == 'player1' else 'player1'

    result, winner = game.fire(player, int(data['x']), int(data['y']))
    emit('attack_result', {'result': result, 'x': data['x'], 'y': data['y'], 'player': player, 'room': room_id})

    emit('recieve_Attack', {'result': result, 'x': data['x'], 'y': data['y'], 'room': room_id, 'player': player}, broadcast=True, include_self=False)

    if winner:
        emit('game_over', {'winner': winner, 'room': room_id})

@socketio.on('connect_game')
def join_game(data):
    room_id = data.get('room_id')

    if room_id in games:
        join_room(room_id)
        emit('juego_actual', {'id': room_id, 'room': room_id, 'player': 'player2'}, broadcast=False)
    else:
        socketio.emit('error', 'La sala no existe')
