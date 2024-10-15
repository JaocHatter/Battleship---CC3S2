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
    socketio.emit('juego_actual', id)
    session['room'] = id
    session['player_name'] = player_name
    #DEBUG
    print(games[id].players)

# Segundo jugador
@socketio.on('connect_game')
def join_game(data):
    room_id = data['room_id']  # Obtén el ID de la sala del cliente
    player_name = data['player_name']
    if room_id not in games:
        print("JUEGO NO EXISTENTE")
        emit('error', {'message': 'La sala no existe.'}, room=request.sid) #Enviamos mensaje de error
        return
    join_room(room_id)  
    games[room_id].add_player(request.sid, player_name)
    print(player_name +' se ha unido al juego')
    print(f'Usuario unido a la sala {room_id}')
    session['room'] = room_id
    session['player_name'] = player_name
    if len(games[room_id].players) == 2:
        socketio.emit('both_ready',room=room_id)
        socketio.emit('start_turn', room=games[room_id].turn)
        #DEBUG
        print(games[room_id].players)

@socketio.on('place_ship')
def on_place_ship(data):
    room_id = data['room_id']
    x, y = data['x'], data['y']
    game = games[room_id]
    player_board = game.players[request.sid]
    success = player_board.place_ship(x, y)
    emit('ship_placed', {'success': success, 'x': x, 'y': y})
    # Verificar si ambos jugadores han colocado sus barcos
    if all(player.remaining_ships == 0 for player in game.players.values()):
        socketio.emit('both_ready', room=room_id)

@socketio.on('ships_ready')
def on_ships_ready(data):
    room_id = data['room_id']
    # Aquí podrías implementar lógica adicional si es necesario
    pass

@socketio.on('make_move')
def on_make_move(data):
    room_id = data['room_id']
    x, y = data['x'], data['y']
    game = games[room_id]
    result = game.make_move(request.sid, x, y)
    if result['status'] == 'error':
        emit('error', {'message': result['message']})
    else:
        # Enviar el resultado al jugador que hizo el movimiento
        emit('move_result', {'hit': result['hit'], 'x': x, 'y': y})
        # Informar al oponente del disparo recibido
        opponent_sid = game.get_opponent_sid(request.sid)
        socketio.emit('opponent_moved', {'x': x, 'y': y, 'hit': result['hit']}, room=opponent_sid)
        if result['status'] == 'win':
            winner_name = game.players[request.sid].player_name
            socketio.emit('game_over', {'winner': winner_name}, room=room_id)
            del games[room_id]
        else:
            # Cambiar el turno al oponente
            socketio.emit('start_turn', room=opponent_sid)
