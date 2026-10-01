import arcade
import animate
from constants import *
import time

class Zombie(animate.Animate):
    def __init__(self, image, health, row, center_y, window):
        super().__init__(image, scale=0.8)
        self.health = health
        self.row = row
        self.set_position(SCREEN_WIDTH, center_y)
        self.change_x = 0.2
        self.eating = False
        self.window = window
        self.damage = 0.5
    def update(self):
        if not self.eating:
            self.center_x -= self.change_x
        if self.health <= 0:
            self.window.killed_zomdies += 1
            self.window.attack_time -= 1
            self.kill()
        self.eating = False
        food = arcade.check_for_collision_with_list(self, self.window.plants)
        for plant in food:
            if self.row == plant.row:
                self.eating = True
                plant.health -= self.damage
        if self.center_x < LAWNS_LEFT:
            self.window.game = False
        
class OrdinaryZombie(Zombie):
    def __init__(self, center_y, row, window):
        super().__init__('zombies/OrdinaryZombie/Zombie_0.png', 12, row, center_y, window)
        for i in range(22):
            self.append_texture(arcade.load_texture(f'zombies/OrdinaryZombie/Zombie_{i}.png'))

class ConeHeadZombie(Zombie):
    def __init__(self, center_y, row, window):
        super().__init__('zombies/ConeheadZombie/ConeheadZombie_0.png', 20, row, center_y, window)
        for i in range(21):
            self.append_texture(arcade.load_texture(f"zombies/ConeheadZombie/ConeheadZombie_{i}.png"))

class BuckHeadZombie(Zombie):
    def __init__(self, center_y, row, window):
        super().__init__("zombies/BucketheadZombie/BucketheadZombie_0.png", 32, row, center_y, window)
        for i in range(15):
            self.append_texture(arcade.load_texture(f"zombies/BucketheadZombie/BucketheadZombie_{i}.png"))

class FlagZombie(Zombie):
    def __init__(self, center_y, row, window):
        super().__init__("zombies/FlagZombie/FlagZombie_0.png", 36, row, center_y, window)
        self.change_x = 0.6
        self.damage = 2.0
        for i in range(12):
            self.append_texture(arcade.load_texture(f"zombies/FlagZombie/FlagZombie_{i}.png"))
        