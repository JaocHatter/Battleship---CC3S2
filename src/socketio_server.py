from flask import Flask, render_template, Blueprint, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from nanoid import generate
from src.models.game import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CC3S2 -  Grupo 3'

socketio = SocketIO(app)
games = {}  # Diccionario para almacenar las instancias de juego

roomBp = Blueprint('sala', __name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game/<id>')
def game_room(id):
    print('id: ', id)
    return render_template('gameRoom.html', id=id)    

@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Lado del servidor

# Primer jugador
@socketio.on('new_game')
def create_game(data):
    player_name = data['player_name']
    id= generate(size=5)
    join_room(id)
    games[id] = Game(room_id=id)
    # Añadimos al primer jugador
    games[id].add_player(request.sid, player_name)
    print(player_name +' se ha unido al juego')
    print('El juego ha sido generado con el id: '+id)
    socketio.emit('juego_actual', id, room=id)
    print(games[id].players)

# Segundo jugador
@socketio.on('connect_game')
def join_game(data):
    room_id = data['room_id']  # Obtén el ID de la sala del cliente
    player_name = data['player_name']
    join_room(room_id)  
    if room_id not in games:
        print("JUEGO NO EXISTENTE")
        return
    games[room_id].add_player(request.sid, player_name)
    print(player_name +' se ha unido al juego')
    print(f'Usuario unido a la sala {room_id}')
    if len(games[room_id].players) == 2:
        socketio.emit('juego_actual', room_id, room=room_id)
        print(games[room_id].players)

    



