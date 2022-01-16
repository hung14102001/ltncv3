import socket
import json

from player import Player
from enemy import Enemy
from cannonball import CannonBall


class Network:
    """
    A client class to abstract away socket functions and make communication with server less of a headache.

    Args:
        server_addr (str): IPv4 address of the server
        server_port (int): Port at which server is running
        username (str): Username of this client's player
    """

    def __init__(self, server_addr: str, server_port: int, info: dict):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = server_addr
        self.port = server_port
        self.info = info
        self.recv_size = 2048

    def settimeout(self, value):
        self.client.settimeout(value)

    def connect(self):
        """
        Connect to the server and get a unique identifier
        """

        self.client.connect((self.addr, self.port))

        self.client.send(json.dumps(self.info).encode("utf8"))

        info = self.client.recv(self.recv_size).decode("utf8")
        info = json.loads(info)

        self.id = info['id']
        self.initPosition = info['position']
        self.restrictor = info['restrictor']
        self.coinPosition = info['coins']

        # initPosition = self.client.recv(self.recv_size).decode("utf8")
        # self.initPosition = json.loads(initPosition)

        # coinPosition = self.client.recv(self.recv_size).decode('utf8')
        # self.coinPosition = json.loads(coinPosition)

    # def getInitPosition(self):
    #     x = float(self.initPosition[0])
    #     y = float(self.initPosition[1])
    #     return (x, y)

    def receive_info(self):
        try:

            msg = self.client.recv(self.recv_size)
        except socket.error as e:
            print(e)

        if not msg:
            return None

        msg_decoded = msg.decode("utf8")

        msg_json = [json.loads(e + '}') for e in msg_decoded.split('}')[:-1]]
        
        return msg_json

    def send_player(self, player: Player):
        player_info = {
            "object": "player",
            "id": self.id,
            "position": (player.world_x, player.world_y),
            "direction": player.rotation_z,
            "health": player.health,
            "joined": False,
            "left": False
        }
        player_info_encoded = json.dumps(player_info).encode("utf8")

        try:
            self.client.send(player_info_encoded)
        except socket.error as e:
            print(e)

    def send_bullet(self, cannon_ball: CannonBall):
        cannon_ball_info = {
            "object": "cannonball",
            "position": (cannon_ball.world_x, cannon_ball.world_y),
            "damage": cannon_ball.damage,
            'rediffX': cannon_ball.rediffX,
            'rediffY': cannon_ball.rediffY,
            'player_id': self.id,
        }

        cannon_ball_info_encoded = json.dumps(cannon_ball_info).encode("utf8")

        try:
            self.client.sendall(cannon_ball_info_encoded)
        except socket.error as e:
            print(e)

    def send_health(self, enemy: Enemy):
        health_info = {
            "object": "health_update",
            "id": enemy.id,
            "health": enemy.health
        }

        health_info_encoded = json.dumps(health_info).encode("utf8")

        try:
            self.client.sendall(health_info_encoded)
        except socket.error as e:
            print(e)

    def send_score(self, player: Player):
        score = {
            'object': 'score',
            'id': self.id,
            'score': player.score,
        }
        score_info_encoded = json.dumps(score).encode('utf8')

        try:
            self.client.send(score_info_encoded)
        except socket.error as e:
            print(e)

    def send_coin(self, coin_id):
        coin = {
            'object': 'coin_update',
            'coin_id': coin_id,
        }
        coin_info_encoded = json.dumps(coin).encode('utf8')

        try:
            self.client.send(coin_info_encoded)
        except socket.error as e:
            print(e)


    def close(self):
        self.client.close()
