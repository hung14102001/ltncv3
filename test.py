from turtle import position
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

class Game(Entity):
    def __init__(self) -> None:
        can_continue = True

        while can_continue:
            self.n = Network(socket.gethostname(), 8000, {'username': 'manh', 'health': 20, 'damage': 1, 'ship': 1})
            self.n.settimeout(5)
            
            can_continue = False

            try:
                self.n.connect()
            except ConnectionRefusedError:
                print("\nConnection refused! This can be because server hasn't started or has reached it's self.player limit.")
                can_continue = True
            except socket.timeout:
                print("\nServer took too long to respond, please try again...")
                can_continue = True
            except socket.gaierror:
                print("\nThe IP address you entered is invalid, please try again with a valid address...")
                can_continue = True
            finally:
                self.n.settimeout(None)
        super().__init__(position=(0, 0))
        self.coin = Coin(self.n.coinPosition)
        self.player = Player(self.n.initPosition, self.n, self.coin)

        self.prev_pos = self.player.world_position
        self.prev_dir = self.player.world_rotation_z

        background = Sea(self.n.restrictor)

        plant = Plant()
        gameUI = GameUI(self.player)

        self.enemies = []
        self.scores = []

        msg_thread = threading.Thread(target=self.protocol, daemon=True)
        msg_thread.start()

    def input(self, key):
        # if key == 'esc':
        #     app.running = False
        # move left if hold arrow left

        if mouse.left and self.player.health > 0:
            # Audio('audios/shot.wav').play()
            if time.time() - self.player.reload > 1:
                self.player.reload = time.time()
                bullet = CannonBall(self.player, (self.player.x, self.player.y), mouse.x, mouse.y, 10, self.n)
                self.n.send_bullet(bullet)

    def protocol(self):

        while True:
            try:
                infor = self.n.receive_info()
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
                        self.enemies.append(new_enemy)
                        continue

                    enemy = None

                    for e in self.enemies:
                        if e.id == enemy_id:
                            enemy = e
                            break

                    if not enemy:
                        continue

                    if info["left"]:
                        self.enemies.remove(enemy)
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
                    for e in self.enemies:
                        if e.id == b_enemy_id:
                            enemy = e

                    CannonBall(self.player, b_pos, b_rediffX, b_rediffY, b_damage, self.n, enemy=enemy)


                elif info["object"] == "health_update":
                    enemy_id = info["id"]

                    enemy = None

                    if enemy_id == self.n.id:
                        enemy = self.player
                    else:
                        for e in self.enemies:
                            if e.id == enemy_id:
                                enemy = e
                                break

                    if not enemy:
                        continue

                    enemy.health = info["health"]

                elif info['object'] == 'score':
                    enemy_id = info["id"]

                    enemy = None

                    if enemy_id == self.n.id:
                        enemy = self.player
                    else:
                        for e in self.enemies:
                            if e.id == enemy_id:
                                enemy = e
                                break

                    if not enemy:
                        continue

                    self.scores.append((info['id'], info['score']))

                elif info['object'] == 'coin_update':
                    self.coin.destroy_coin(info['coin_id'])

                elif info['object'] == 'end_game':
                    if not self.player.game_ended:
                        self.player.game_ended = True
                        self.scores.append(('player', self.player.score))

                    self.n.close()

    def update(self):

        if self.player.health > 0:
            if self.prev_pos != self.player.world_position or self.prev_dir != self.player.world_rotation_z:
                self.n.send_player(self.player)

            self.prev_pos = self.player.world_position
            self.prev_dir = self.player.world_rotation_z

        elif not self.player.game_ended:
            self.n.send_player(self.player)
            self.n.send_score(self.player)
            self.player.game_ended = True
            self.scores.append(('player', self.player.score))
            print(self.scores)


# app.run()