from ursina import *
import socket
import threading
import time

from network import Network
from gameUI import GameUI
from cannonball import CannonBall
from player import Player
from sea import Sea, Plant, Coin
from endgame import GameOver
from enemy import Enemy


class Game(Entity):
    def __init__(self, character, sound) -> None:
        can_continue = True

        while can_continue:
            self.network = Network(
                socket.gethostname(),
                8000,
                {
                    'health': character['hp'],
                    'damage': character['dmg'],
                    'ship': character['type']
                }
            )
            self.network.settimeout(5)

            can_continue = False

            try:
                self.network.connect()
            except ConnectionRefusedError:
                print(
                    "\nConnection refused! This can be because server hasn't started or has reached it's self.player limit.")
                can_continue = True
            except socket.timeout:
                print("\nServer took too long to respond, please try again...")
                can_continue = True
            except socket.gaierror:
                print(
                    "\nThe IP address you entered is invalid, please try again with a valid address...")
                can_continue = True
            finally:
                self.network.settimeout(None)

        super().__init__(position=(0, 0))
        self.a = sound
        self.coin = Coin(self.network.coinPosition)
        self.player = Player(self.network.initPosition,
                             character, self.network, self.coin, self.a)
        self.player.id = self.network.id

        self.prev_pos = self.player.world_position
        self.prev_dir = self.player.world_rotation_z

        self.background = Sea(self.network.restrictor)

        self.plants = Plant()
        self.ui = GameUI(self.player, self.background.restrictor)
        camera.z = -30

        self.enemies = []
        self.scores = []

        self.game_ended = False
        self.msg_thread = threading.Thread(target=self.protocol, daemon=True)
        self.msg_thread.start()

    def input(self, key):
        # if key == 'esc':
        #     app.running = False
        # move left if hold arrow left

        if mouse.left and self.player.health > 0:
            # Audio('audios/shot.wav').play()
            if time.time() - self.player.reload > 1:
                if self.a.volume == 1:
                    Audio('shot', loop=False, autoPlay=True)
                else:
                    Audio('shot', volume=0)
                self.player.reload = time.time()
                bullet = CannonBall(
                    self.player,
                    (self.player.x, self.player.y),
                    mouse.x,
                    mouse.y,
                    self.player.damage,
                    self.network
                )
                self.network.send_bullet(bullet)

    def protocol(self):
        while True:
            if self.game_ended:
                return
            try:
                infor = self.network.receive_info()
            except Exception as e:
                continue

            if not infor:
                print("Server has stopped! Exiting...")
                self.game_ended = True
                return

            for info in infor:

                if info["object"] == "player":
                    enemy_id = info["id"]

                    if info["joined"]:
                        new_enemy = Enemy(info)
                        print(info)
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

                    CannonBall(self.player, b_pos, b_rediffX,
                               b_rediffY, b_damage, self.network, enemy=enemy)

                elif info["object"] == "health_update":
                    enemy_id = info["id"]

                    enemy = None

                    if enemy_id == self.network.id:
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

                    if enemy_id == self.network.id:
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
                    if not self.player.death_shown:
                        GameOver(self, self.a)
                        self.player.death_shown = True
                        self.scores.append(('player', self.player.score))

                    self.game_ended = True
                    self.network.close()

    def update(self):
        if not hasattr(self, 'player'):
            return
        if self.player.health > 0 and not self.player.death_shown:
            if self.prev_pos != self.player.world_position or self.prev_dir != self.player.world_rotation_z:
                self.network.send_player(self.player)

                self.prev_pos = self.player.world_position
                self.prev_dir = self.player.world_rotation_z

            if self.background.restrictor:
                if self.player.x**2 + self.player.y**2 > self.background.restrictor.scale_x**2/4 and time.time() > self.background.restrictor.burn_time:
                    self.background.restrictor.burn_time = time.time() + 1
                    self.player.health -= self.player.maxHealth*.05
                    self.network.send_health(self.player)

        elif not self.player.death_shown:
            GameOver(self, self.a)
            self.network.send_player(self.player)
            self.network.send_score(self.player)
            self.player.death_shown = True
            self.scores.append(('player', self.player.score))
            print(self.scores)

    def destroyGame(self):
        self.network.client.close()
        del self.msg_thread
        self.ui.destroySelf()
        self.plants.destroySelf()
        self.background.destroySelf()
        self.coin.destroySelf()

        destroy(self.player)
        for e in self.enemies:
            destroy(e)
            del e
        destroy(self)
        del self

# app.run()
