import os
import ursina
from random import randint
import time


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
    def __init__(self, position, img):
        super().__init__(
            position=position,
            scale=1,
            model="quad",
            texture=img,
            collider="box"
        )
        # self.texture.filtering = None


class Island2x2:
    tiles = [os.path.join("Tiles", f"tile_{x}") for x in range(0, 96)]

    def __init__(self, position_x, position_y):
        self.entities = []
        for j in range(0, 2):
            for i in range(0, 2):
                part = IslandPart(ursina.Vec3(
                    position_x + i, position_y - j, 0), self.tiles[16*j + i+4])
                self.entities.append(part)

    def destroySelf(self):
        for e in self.entities:
            ursina.destroy(e)


class Island4x4:
    tiles = [os.path.join("Tiles", f"tile_{x}") for x in range(0, 96)]

    def __init__(self, position_x, position_y):
        self.entities = []
        for j in range(0, 4):
            for i in range(0, 4):
                part = IslandPart(ursina.Vec3(
                    position_x + i, position_y - j, 0), self.tiles[16*((j+1)//2) + ((i+1)//2) + 1])
                self.entities.append(part)

    def destroySelf(self):
        for e in self.entities:
            ursina.destroy(e)


class Island6x6:
    tiles = [os.path.join("Tiles", f"tile_{x}") for x in range(0, 96)]

    def __init__(self, position_x, position_y):
        self.entities = []
        for j in range(0, 6):
            for i in range(0, 6):
                part = IslandPart(ursina.Vec3(
                    position_x + i, position_y - j, 0), self.tiles[16*((j+1)//2) + ((i+1)//2) + 6])
                self.entities.append(part)

    def destroySelf(self):
        for e in self.entities:
            ursina.destroy(e)


class PlantPart(ursina.Entity):
    def __init__(self, position, img):
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

    def destroySelf(self):
        for c in self.coin_list:
            ursina.destroy(self.coin_list[c])
        del self


class Plant:
    tiles = [os.path.join("Tiles", f"tile_{x}") for x in range(0, 96)]

    def __init__(self):
        self.entities = []
        for x in range(0, 10):
            for i in range(0, 3):
                px = randint(-20, 20)
                py = randint(-20, 20)
                part = PlantPart(ursina.Vec3(px+i, py, 0), self.tiles[70+i])
                self.entities.append(part)
        for x in range(0, 10):
            for i in range(0, 2):
                px = randint(-20, 20)
                py = randint(-20, 20)
                part = PlantPart(ursina.Vec3(px+i, py, 0), self.tiles[87+i])
                self.entities.append(part)

    def destroySelf(self):
        for e in self.entities:
            ursina.destroy(e)


class Restrictor(ursina.Entity):

    def __init__(self, init_time):
        super().__init__(
            model=ursina.Circle(resolution=50, mode='line'),
            scale=(40*2**.5, 40*2**.5),
            color=ursina.color.rgb(0, 0, 0),
        )
        self.burn_time = time.time()
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
            if self.scale_x <= 0:
                return

            self.scale -= ursina.time.dt

            if time.time() > self.countDown:
                self.countDown += 5
                self.restricting = False

        elif time.time() > self.countDown:
            self.countDown += 15
            self.restricting = True


class Sea:
    tiles = [os.path.join("Tiles", f"tile_{x}") for x in range(0, 96)]

    def __init__(self, init_time):
        self.entities_destroyable = []
        self.entities = []
        for x in range(-20, 20, 2):
            for y in range(-20, 20, 2):
                part = SeaPart(ursina.Vec3(x, y, 0.1))
                self.entities_destroyable.append(part)
        for x in range(-30, 30, 2):
            for y in range(-30, 30, 2):
                if x >= 20 or x <= -20 or y <= -20 or y >= 20:
                    part = SoilPart(ursina.Vec3(x, y, 0))
                    self.entities_destroyable.append(part)
        # dọc dưới
        island = Island2x2(-0.5, -15.5)
        self.entities.append(island)
        island = Island2x2(-0.5, -17.5)
        self.entities.append(island)
        island = Island2x2(-0.5, -13.5)
        self.entities.append(island)
        island = Island2x2(-0.5, -11.5)
        # dọc trên
        self.entities.append(island)
        island = Island2x2(-0.5, 18.5)
        self.entities.append(island)
        island = Island2x2(-0.5, 16.5)
        self.entities.append(island)
        island = Island2x2(-0.5, 14.5)
        self.entities.append(island)
        island = Island2x2(-0.5, 12.5)
        self.entities.append(island)

        # ngang trái
        self.entities.append(island)
        island = Island2x2(-18.5, 0.5)
        self.entities.append(island)
        island = Island2x2(-16.5, 0.5)
        self.entities.append(island)
        island = Island2x2(-14.5, 0.5)
        self.entities.append(island)
        island = Island2x2(-12.5, 0.5)
        self.entities.append(island)

        # ngang phải
        island = Island2x2(11.5, 0.5)
        self.entities.append(island)
        island = Island2x2(13.5, 0.5)
        self.entities.append(island)
        island = Island2x2(15.5, 0.5)
        self.entities.append(island)
        island = Island2x2(17.5, 0.5)
        self.entities.append(island)

        # giữa
        island = Island6x6(-2.5, 2.5)
        self.entities.append(island)

        # 4 góc
        self.entities.append(island)
        island = Island4x4(-8.5, -5.5)
        self.entities.append(island)
        island = Island4x4(-8.5, 8.5)
        self.entities.append(island)
        island = Island4x4(5.5, -5.5)
        self.entities.append(island)
        island = Island4x4(5.5, 8.5)
        self.entities.append(island)

        # đá
        # island = IslandPart(ursina.Vec3(0,0,0), self.tiles[0])
        self.restrictor = Restrictor(init_time)
        self.entities_destroyable.append(self.restrictor)

    def destroySelf(self):
        for e in self.entities_destroyable:
            ursina.destroy(e)

        for e in self.entities:
            e.destroySelf()
