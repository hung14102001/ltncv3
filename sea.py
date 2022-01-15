import os
import ursina
from random import randint
import time

from ursina import collider    

# self.collider = BoxCollider(self, size=Vec3(1, 2, 1))

class SeaPart(ursina.Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            scale=2,
            model="quad",
            texture=os.path.join("Tiles", "tile_73.png")
        )
        self.texture.filtering = None

class SoilPart(ursina.Entity):
    def __init__(self, position):
        super().__init__(
            position=position,
            scale=2,
            model="quad",
            texture=os.path.join("Tiles", "tile_18.png"),
            collider="box"
        )
        self.texture.filtering = None

class IslandPart(ursina.Entity):
    def __init__(self, position,img):
        super().__init__(
            position=position,
            scale=1,
            model="quad",
            texture=img,
            collider="box"
        )
        # self.texture.filtering = None

class Island2x2:
    tiles = [os.path.join("Tiles",f"tile_{x}") for x in range(0,96)]
    def __init__(self, position_x, position_y):
        for j in range(0, 2):
            for i in range(0, 2):
                part = IslandPart(ursina.Vec3(position_x + i, position_y - j,0), self.tiles[16*j + i+4])


class Island4x4:
    tiles = [os.path.join("Tiles",f"tile_{x}") for x in range(0,96)]
    def __init__(self, position_x, position_y):
        for j in range(0, 4):
            for i in range(0, 4):
                part = IslandPart(ursina.Vec3(position_x + i, position_y - j,0), self.tiles[16*((j+1)//2) + ((i+1)//2) + 1 ])
            
class Island6x6:
    tiles = [os.path.join("Tiles",f"tile_{x}") for x in range(0,96)]
    def __init__(self, position_x, position_y):
        for j in range(0, 6):
                for i in range(0, 6):
                    part = IslandPart(ursina.Vec3(position_x + i, position_y - j,0), self.tiles[16*((j+1)//2) + ((i+1)//2) + 6])
            
class PlantPart(ursina.Entity):
    def __init__(self, position,img):
        super().__init__(
            position=position,
            scale=1,
            model="quad",
            texture=img,
            # collider="box"
        )

class CoinPart(ursina.Entity):
    def __init__(self, index, position):
        coin = os.path.join("Coins", "coin.png")
        super().__init__(
            position=position,
            scale=1,
            model="quad",
            texture=coin,
            collider="box"
        )
        self.index = index
class Coin:
    def __init__(self, position_list):
        self.coin_list = {}
        for i in position_list:
            self.coin_list[i] = CoinPart(i, ursina.Vec2(*position_list[i]))
        
    def destroy_coin(self, index):
        coin = self.coin_list[index]
        ursina.destroy(coin)
        del self.coin_list[index]
    
class Plant:
    tiles = [os.path.join("Tiles",f"tile_{x}") for x in range(0,96)]
    coin = os.path.join("Coins", "coin.png")
    def __init__(self):
        for x in range(0,10):
            for i in range(0, 3):
                px = randint(-20, 20)
                py = randint(-20, 20)
                part = PlantPart(ursina.Vec3(px+i, py, 0), self.tiles[70+i])
        for x in range(0,10):
            for i in range(0, 2):
                px = randint(-20, 20)
                py = randint(-20, 20)
                part = PlantPart(ursina.Vec3(px+i, py, 0), self.tiles[87+i])

class Restrictor(ursina.Entity):
    def __init__(self, init_time):
        super().__init__(
            model=ursina.Circle(resolution=50, mode='line'),
            scale=(40*2**.5,40*2**.5),
            color=ursina.color.rgb(0,0,0),
        )
        period = time.time() - init_time
        period_times = period//20
        current_time = period - period_times*20

        self.scale -= period_times*15
        if current_time > 5:
            self.restricting = True
            self.countDown = time.time() + 20 - current_time
            self.scale -= current_time - 5
        else:
            self.restricting = False
            self.countDown = time.time() + 5 - current_time

    def update(self):
        if self.restricting:
            self.scale -= ursina.time.dt

            if self.scale_x <= 0:
                ursina.destroy(self)

            elif time.time() > self.countDown:
                self.countDown += 5
                self.restricting = False

        elif time.time() > self.countDown:
            self.countDown += 15
            self.restricting = True


class Sea:
    tiles = [os.path.join("Tiles",f"tile_{x}") for x in range(0,96)]    
    def __init__(self, init_time):
        for x in range(-20, 20, 2):
            for y in range(-20, 20, 2):
                part = SeaPart(ursina.Vec3(x, y, 0.1))
        for x in range(-30, 30, 2):
            for y in range(-30, 30, 2):
                if x >= 20 or x <=-20 or y <= -20 or y >= 20:
                    part = SoilPart(ursina.Vec3(x, y, 0))
        # dọc dưới
        island = Island2x2(-0.5, -15.5)
        island = Island2x2(-0.5, -17.5)
        island = Island2x2(-0.5, -13.5)
        island = Island2x2(-0.5, -11.5)
        # dọc trên
        island = Island2x2(-0.5, 18.5)
        island = Island2x2(-0.5, 16.5)
        island = Island2x2(-0.5, 14.5)
        island = Island2x2(-0.5, 12.5)

        # ngang trái
        island = Island2x2(-18.5, 0.5)
        island = Island2x2(-16.5, 0.5)
        island = Island2x2(-14.5, 0.5)
        island = Island2x2(-12.5, 0.5)

        # ngang phải
        island = Island2x2(11.5, 0.5)
        island = Island2x2(13.5, 0.5)
        island = Island2x2(15.5, 0.5)
        island = Island2x2(17.5, 0.5)

        # giữa
        island = Island6x6(-2.5,2.5)
        
        # 4 góc
        island = Island4x4(-8.5,-5.5)
        island = Island4x4(-8.5,8.5)
        island = Island4x4(5.5,-5.5)
        island = Island4x4(5.5,8.5)

        # đá 
        # island = IslandPart(ursina.Vec3(0,0,0), self.tiles[0])
        Restrictor(init_time)
