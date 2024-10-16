from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, join_room
from nanoid import generate
from src.controllers.game_controller import GameController

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CC3S2 -  Grupo 3'

socketio = SocketIO(app)
games = {}  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/<id>')
def game_room(id):
    print(f'id de la sala: {id}')
    return render_template('gameRoom.html', id=id)

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('new_game')
def create_game():
    id = generate(size=5)  
    games[id] = {
        "game": GameController('player1', 'player2'),
        "players_ready": 0
    }
    join_room(id)
    session['room_id'] = id 
    session['player'] = 'player1'
    print(f'El juego ha sido generado con el id: {id}')
    socketio.emit('juego_actual', id, room=id)

@socketio.on('place_ships')
def handle_place_ships(data):
    room_id = session.get('room_id')
    if room_id not in games:
        return

    game = games[room_id]["game"]
    player = session['player']
    game.place_ships(player, data['board'])

    games[room_id]["players_ready"] += 1
    if games[room_id]["players_ready"] == 2:
        socketio.emit('start_game', room=room_id) 

@socketio.on('attack')
def handle_attack(data):
    room_id = session.get('room_id')
    if room_id not in games:
        return  

    game = games[room_id]["game"]
    player = session['player']

    result, winner = game.fire(player, data['x'], data['y'])
    socketio.emit('attack_result', {'result': result, 'x': data['x'], 'y': data['y'], 'player': player}, room=room_id)

    if winner:
        socketio.emit('game_over', {'winner': winner}, room=room_id)

@socketio.on('connect_game')
def join_game(data):
    room_id = data.get('room_id')
    print(f'Intentando unir al usuario a la sala con ID: {room_id}')

    if room_id in games:
        join_room(room_id)
        session['room_id'] = room_id
        session['player'] = 'player2'
        print(f'Usuario unido a la sala {room_id}')
        socketio.emit('juego_actual', room_id, room=room_id)
    else:
        print(f'La sala con ID {room_id} no existe')
        socketio.emit('error', 'La sala no existe')
