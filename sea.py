import os
from ursina import *
from random import randint
import time  

# self.collider = BoxCollider(self, size=Vec3(1, 2, 1))

class SeaPart(Entity):
    def __init__(self, parent,position):
        super().__init__(
            parent=parent,
            position=position,
            scale=(2,2,0),
            model="quad",
            texture=os.path.join("Tiles", "tile_73.png")
        )
        self.texture.filtering = None

class SoilPart(Entity):
    def __init__(self,parent,position):
        super().__init__(
            parent=parent,
            position=position,
            scale=2,
            model="quad",
            texture=os.path.join("Tiles", "tile_18.png"),
            collider="box"
        )
        self.texture.filtering = None

class IslandPart(Entity):
    def __init__(self,parent,position,img):
        super().__init__(
            parent=parent,
            position=position,
            scale=1,
            model="quad",
            texture=img,
            collider="box"
        )
        # self.texture.filtering = None

class Island2x2(Entity):
    tiles = [os.path.join("Tiles",f"tile_{x}") for x in range(0,96)]
    def __init__(self, parent, position_x, position_y):
        super().__init__(parent=parent)
        for j in range(0, 2):
            for i in range(0, 2):
                part = IslandPart(self,Vec3(position_x + i, position_y - j,0), self.tiles[16*j + i+4])


class Island4x4(Entity):
    tiles = [os.path.join("Tiles",f"tile_{x}") for x in range(0,96)]
    def __init__(self, parent, position_x, position_y):
        super().__init__(parent=parent)
        for j in range(0, 4):
            for i in range(0, 4):
                part = IslandPart(self,Vec3(position_x + i, position_y - j,0), self.tiles[16*((j+1)//2) + ((i+1)//2) + 1 ])
            
class Island6x6(Entity):
    tiles = [os.path.join("Tiles",f"tile_{x}") for x in range(0,96)]
    def __init__(self, parent, position_x, position_y):
        super().__init__(parent=parent)
        for j in range(0, 6):
                for i in range(0, 6):
                    part = IslandPart(self,Vec3(position_x + i, position_y - j,0), self.tiles[16*((j+1)//2) + ((i+1)//2) + 6])
            
class PlantPart(Entity):
    def __init__(self,position,img):
        super().__init__(
            position=position,
            scale=1,
            model="quad",
            texture=img,
            # collider="box"
        )

class CoinPart(Entity):
    def __init__(self,position,img):
        super().__init__(
            position=position,
            scale=1,
            model="quad",
            texture=img,
            collider="box"
        )
    def update(self):
        hitinfo = self.intersects()
        if hitinfo.hit:
            destroy(self)
            # self.player.score += 1
class Coin(Entity):
    coin = os.path.join("Coins", "coin.png")
    def __init__(self):
        for x in range(0,50):
            px = randint(-20, 20)
            py = randint(-20, 20)
            part = CoinPart(Vec3(px, py, 0), self.coin)
    # text = Text(text="Score: " +str(score), color=color.rgb(0,0,0), scale = 2.5, position=(-0.8,0.5,0))
    
class Plant(Entity):
    tiles = [os.path.join("Tiles",f"tile_{x}") for x in range(0,96)]
    coin = os.path.join("Coins", "coin.png")
    def __init__(self):
        for x in range(0,10):
            for i in range(0, 3):
                px = randint(-20, 20)
                py = randint(-20, 20)
                part = PlantPart(Vec3(px+i, py, 0), self.tiles[70+i])
        for x in range(0,10):
            for i in range(0, 2):
                px = randint(-20, 20)
                py = randint(-20, 20)
                part = PlantPart(Vec3(px+i, py, 0), self.tiles[87+i])

class Restrictor(Entity):
    def __init__(self,parent):
        super().__init__(
            parent=parent,
            model=Circle(resolution=50, mode='line'),
            scale=(30,30),
            color=color.rgb(0,0,0),
            text = Text(text="Time: ", parent=parent, color=color.rgb(0,0,0), scale = 2.5, position=(.3,0.5,0)),
        )
        self.countDown = time.time() + 5
        self.restricting = False

    def update(self):
        if self.restricting:
            self.scale_x -= time.dt
            self.scale_y -= time.dt

            if self.scale_x <= 0:
                destroy(self)

            elif time.time() > self.countDown:
                self.countDown += 5
                self.restricting = False

        elif time.time() > self.countDown:
            self.countDown += 15
            self.restricting = True


class Sea(Entity):
    tiles = [os.path.join("Tiles",f"tile_{x}") for x in range(0,96)]    
    def __init__(self):
        super().__init__(
            enabled=False
        )

        for x in range(-20, 20, 2):
            for y in range(-20, 20, 2):
                part = SeaPart(self,Vec3(x, y, 0.1))
        
        for x in range(-30, 30, 2):
            for y in range(-30, 30, 2):
                if x >= 20 or x <=-20 or y <= -20 or y >= 20:
                    part = SoilPart(self,Vec3(x, y, 0))
                   
        # dọc dưới
        island = Island2x2(self, -0.5, -15.5)
        island = Island2x2(self, -0.5, -17.5)
        island = Island2x2(self, -0.5, -13.5)
        island = Island2x2(self, -0.5, -11.5)
        # dọc trên
        island = Island2x2(self, -0.5, 18.5)
        island = Island2x2(self, -0.5, 16.5)
        island = Island2x2(self, -0.5, 14.5)
        island = Island2x2(self, -0.5, 12.5)

        # ngang trái
        island = Island2x2(self, -18.5, 0.5)
        island = Island2x2(self, -16.5, 0.5)
        island = Island2x2(self, -14.5, 0.5)
        island = Island2x2(self, -12.5, 0.5)

        # ngang phải
        island = Island2x2(self, 11.5, 0.5)
        island = Island2x2(self, 13.5, 0.5)
        island = Island2x2(self, 15.5, 0.5)
        island = Island2x2(self, 17.5, 0.5)

        # giữa
        island = Island6x6(self, -2.5,2.5)
        
        # 4 góc
        island = Island4x4(self, -8.5,-5.5)
        island = Island4x4(self, -8.5,8.5)
        island = Island4x4(self, 5.5,-5.5)
        island = Island4x4(self, 5.5,8.5)
       
        # đá 
        # island = IslandPart(Vec3(0,0,0), self.tiles[0])
        Restrictor(self)

