"""
Server script for hosting games
"""

import socket
import json
import time
import random
import threading

# ADDR = "127."
PORT = 8000
MAX_MATCHES = 3
MAX_PLAYERS = 4
MSG_SIZE = 2048
COIN_AMOUNT = 10

# Setup server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(MAX_PLAYERS*MAX_MATCHES)

matches = {}


def generate_id(_list: dict, _max: int):
    """
    Generate a unique identifier
    Args:
        _list (dict): dictionary of existing players/matches
        _max (int): maximum number of players/matches allowed
    Returns:
        str: the unique identifier
    """

    while True:
        unique_id = str(random.randint(1, _max))
        if unique_id not in _list:
            return unique_id


def handle_messages(match_id: str, player_id: int):
    players = matches[match_id]['players']
    client_info = players[player_id]
    conn: socket.socket = client_info["socket"]

    while True:
        try:
            msg = conn.recv(MSG_SIZE)
        except ConnectionResetError:
            break

        if not msg:
            break

        msg_decoded = msg.decode("utf8")

        try:
            msg_json = json.loads(msg)
        except Exception as e:
            print(e)
            continue

        if msg_json["object"] == "player":
            players[player_id]["position"] = msg_json["position"]
            players[player_id]["direction"] = msg_json["direction"]
            players[player_id]["health"] = msg_json["health"]

        if msg_json['object'] == 'score':
            alives = len([0 for p in players if players[p]['health'] > 0])
            if (len(players) > 1 and alives < 2) or alives < 1:
                print(f'Game {match_id} has ended')
                matches[match_id]['ended'] = True


        if msg_json['object'] == 'coin_update':
            index = msg_json['coin_id']
            del matches[match_id]['coins'][index]

        # Tell other players about player moving
        for p_id in players:
            if not players[p_id]['left']:

                player_info = players[p_id]
                player_conn: socket.socket = player_info["socket"]

                if p_id != player_id:
                    try:
                        player_conn.sendall(msg_decoded.encode("utf8"))
                    except OSError:
                        pass
                if match_id not in matches or matches[match_id]['ended']:
                    player_conn.send(json.dumps(
                        {'object': 'end_game'}).encode('utf8'))

    players[player_id]['left'] = True
    # Tell other players about player leaving
    for p_id in players:
        if p_id != player_id and not players[p_id]['left']:
            player_info = players[p_id]
            player_conn: socket.socket = player_info["socket"]
            try:
                player_conn.send(json.dumps(
                    {"id": player_id, "object": "player", "joined": False, "left": True}).encode("utf8"))
            except OSError:
                pass

    print(
        f"Player with ID {player_id} has left the game {match_id}...")

    if players[player_id]['health'] > 0:
        del players[player_id]

    if match_id in matches:
        if len(matches[match_id]['players']) < 1:
            matches[match_id]['ended'] = True
        if len([0 for p in players if players[p]['health'] > 0]) <= 0:
            matches[match_id]['ended'] = True
        if matches[match_id]['ended']:
            del matches[match_id]
            print(f'Game {match_id} has ended')

    conn.close()


def initPlayerInfo(new_player_id, info: str):
    msg_json = {}
    try:
        msg_json = json.loads(info)
    except Exception as e:
        print(e)

    heath = msg_json["health"]
    damage = msg_json["damage"]
    ship = msg_json["ship"]

    x = random.randint(-19, 19)
    y = random.randint(-19, 19)

    position = (x, y)
    res = {
        'player_id': new_player_id,
        'position': position,
        'health': heath,
        'damage': damage,
        'ship': ship,
    }

    return res


def main():
    print("Server started, listening for new connections...")

    while True:
        # Accept new connection and assign match ID and unique ID
        conn, addr = s.accept()
        assigned = False
        new_match_id = -1

        for m in matches:
            if len(matches[m]['players']) < MAX_PLAYERS:
                new_match_id = m
                new_player_id = generate_id(matches[m]['players'], MAX_PLAYERS)
                assigned = True

        if not assigned:
            new_match_id = generate_id(matches, MAX_MATCHES)
            new_player_id = str(random.randint(1, MAX_PLAYERS))
            assigned = True

        recv_info = conn.recv(MSG_SIZE).decode("utf8")

        init_info = initPlayerInfo(new_player_id, recv_info)

        new_player_info = {
            "socket": conn,
            "position": init_info['position'],
            "direction": 0,
            "health": init_info['health'],
            "damage": init_info['damage'],
            "ship": init_info['ship'],
            'left': False
        }

        # Add new player to players list, effectively allowing it to receive messages from other players
        if new_match_id not in matches:
            coin_x = [random.randint(-19, 19) for i in range(COIN_AMOUNT)]
            coin_y = [random.randint(-19, 19) for i in range(COIN_AMOUNT)]
            coins_pos = [*zip(coin_x, coin_y)]
            coins_pos = {str(i): coins_pos[i] for i in range(COIN_AMOUNT)}

            matches[new_match_id] = {
                'ended': False,
                'restrictor': time.time(),
                'coins': coins_pos,
                'players': {}
            }

        matches[new_match_id]['players'][new_player_id] = new_player_info

        send_info = {
            'id': new_player_id,
            'position': new_player_info['position'],
            'coins': matches[new_match_id]['coins'],
            'restrictor': matches[new_match_id]['restrictor'],
        }
        conn.send(json.dumps(send_info).encode('utf8'))

        # Tell existing players about new player
        players = matches[new_match_id]['players']

        for player_id in players:
            if player_id != new_player_id:
                player_info = players[player_id]
                player_conn: socket.socket = player_info["socket"]

                try:
                    player_conn.sendall(json.dumps({
                        "id": new_player_id,
                        "object": "player",
                        "position": new_player_info["position"],
                        "health": new_player_info["health"],
                        "damage": new_player_info["damage"],
                        "ship": new_player_info['ship'],
                        "joined": True,
                        "left": new_player_info['left']
                    }).encode("utf8"))
                except OSError:
                    pass

        # Tell new player about coins_pos

        # Tell new player about existing players
        for player_id in players:
            if player_id != new_player_id:
                player_info = players[player_id]
                try:
                    conn.sendall(json.dumps({
                        "id": player_id,
                        "object": "player",
                        "position": player_info["position"],
                        "health": player_info["health"],
                        "damage": player_info["damage"],
                        "ship": player_info['ship'],
                        "joined": True,
                        "left": False
                    }).encode("utf8"))
                    time.sleep(.1)
                except OSError:
                    pass

        # Start thread to receive messages from client
        msg_thread = threading.Thread(target=handle_messages, args=(
            new_match_id, new_player_id,), daemon=True)
        msg_thread.start()

        print(
            f"New connection from {addr}, assigned ID: {new_match_id, new_player_id}...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
    finally:
        print("Exiting")
        s.close()
