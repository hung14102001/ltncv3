from gameUI import GameUI
from network import Network
import socket
import threading
import os
import time

from re import A, escape
from ursina import *
from random import randint
from cannonball import CannonBall
from player import Player
from sea import Sea, Plant, Coin
from minimap import MiniMap

from ursina.camera import Camera
from enemy import Enemy

def input(key):
    if key == 'esc':
        app.running = False
    # move left if hold arrow left

    if mouse.left and player.health > 0:
        # Audio('audios/shot.wav').play()
        if time.time() - player.reload > 1:
            player.reload = time.time()
            bullet = CannonBall(player, (player.x, player.y), mouse.x, mouse.y, 10, n)
            n.send_bullet(bullet)
    

# display the background
app = Ursina()


can_continue = True

while can_continue:
	n = Network(socket.gethostname(), 8000, {'username': 'manh', 'health': 20, 'damage': 1, 'ship': 1})
	n.settimeout(5)
    
	can_continue = False

	try:
		n.connect()
	except ConnectionRefusedError:
		print("\nConnection refused! This can be because server hasn't started or has reached it's player limit.")
		can_continue = True
	except socket.timeout:
		print("\nServer took too long to respond, please try again...")
		can_continue = True
	except socket.gaierror:
		print("\nThe IP address you entered is invalid, please try again with a valid address...")
		can_continue = True
	finally:
		n.settimeout(None)

enemies = []
scores = []

def protocol():

    while True:
        try:
            infor = n.receive_info()
        except Exception as e:
            print(e)
            continue

        if not infor:
            print("Server has stopped! Exiting...")
            sys.exit()

        for info in infor:
            if info["object"] == "player":
                enemy_id = info["id"]

                if info["joined"]:
                    new_enemy = Enemy(info)
                    enemies.append(new_enemy)
                    continue

                enemy = None

                for e in enemies:
                    if e.id == enemy_id:
                        enemy = e
                        break

                if not enemy:
                    continue

                if info["left"]:
                    enemies.remove(enemy)
                    destroy(enemy)
                    continue

                enemy.world_position = Vec2(*info["position"])
                enemy.rotation_z = info["direction"]

            elif info["object"] == "cannonball":
            	b_pos = Vec2(*info["position"])
            	b_rediffX = info["rediffX"]
            	b_rediffY = info["rediffY"]
            	b_damage = info["damage"]
            	b_enemy_id = info['player_id']
            	for e in enemies:
            		if e.id == b_enemy_id:
            			enemy = e

            	CannonBall(player, b_pos, b_rediffX, b_rediffY, b_damage, n, enemy=enemy)


            elif info["object"] == "health_update":
                enemy_id = info["id"]

                enemy = None

                if enemy_id == n.id:
                    enemy = player
                else:
                    for e in enemies:
                        if e.id == enemy_id:
                            enemy = e
                            break

                if not enemy:
                    continue

                enemy.health = info["health"]

            elif info['object'] == 'score':
                enemy_id = info["id"]

                enemy = None

                if enemy_id == n.id:
                    enemy = player
                else:
                    for e in enemies:
                        if e.id == enemy_id:
                            enemy = e
                            break

                if not enemy:
                    continue

                scores.append((info['id'], info['score']))

            elif info['object'] == 'coin_update':
                coin.destroy_coin(info['coin_id'])

            elif info['object'] == 'end_game':
                if not player.game_ended:
                    player.game_ended = True
                    scores.append(('player', player.score))
                    print(scores)
                n.close()

def update():

    if player.health > 0:
        global prev_pos, prev_dir

        if prev_pos != player.world_position or prev_dir != player.world_rotation_z:
            n.send_player(player)

        prev_pos = player.world_position
        prev_dir = player.world_rotation_z

    elif not player.game_ended:
        n.send_player(player)
        n.send_score(player)
        player.game_ended = True
        scores.append(('player', player.score))
        print(scores)

coin = Coin(n.coinPosition)
player = Player(n.initPosition, n, coin)

prev_pos = player.world_position
prev_dir = player.world_rotation_z

background = Sea(n.restrictor)

plant = Plant()
gameUI = GameUI(player)

msg_thread = threading.Thread(target=protocol, daemon=True)
msg_thread.start()

app.run()