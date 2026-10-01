'''
    Цель: Продолжить создавать игру Plants vs Zombies, добавить игровую валюту, пули и зомби.
    + Вспомнить команды из прошлых уроков;
    + Добавить игровую валюту (солнышки);
    + Научить подсолнухи производить солнышки;
    + Добавить в игру Горохострел;
    + Научить Горохострел стрелять горошинами;
    + Создать базовый класс для зомби;
    + Добавить в игру обычного зомби;
    + Настроить выстрелы по зомби;
    + Получить домашнее задание.
'''
import arcade
import plants
import sun
import time
from constants import *
import zombies
import random

def lawn_x(x):
    right_x = 248 + CELL_WIDTH
    column = 1
    while right_x <= x:
        right_x += CELL_WIDTH
        column += 1
    center_x = right_x - CELL_WIDTH / 2
    return (center_x, column)

def lawn_y(y):
    top_y = 24 + CELL_HEIGHT
    line = 1
    while top_y <= y:
        top_y += CELL_HEIGHT
        line += 1
    center_y = top_y - CELL_HEIGHT / 2 
    return center_y, line

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        #Текстуры
        self.background = arcade.load_texture("textures/background.jpg")
        self.menu = arcade.load_texture("textures/menu_vertical.png")
        self.end_game = arcade.load_texture("textures/end.png")
        #спрайтлист
        self.plants = arcade.SpriteList()
        self.spawn_suns = arcade.SpriteList()
        self.peas = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        #поля
        self.seed = None
        self.lawns = []
        self.sun = 3000
        self.zombie_spawn_time = time.time()
        self.game = True
        self.killed_zomdies = 0
        self.attack_time = 25
        #Звуки
        self.seeding_sound = arcade.load_sound('sounds/seed.mp3')
        self.music = arcade.load_sound("sounds/grasswalk.mp3")
        self.music.play(volume=0.2, loop = True)
        self.hit_sound = arcade.load_sound("sounds/hit.mp3")
        
        #Позиционирование объектов при старте
        self.setup()


    def setup(self):
        pass

    def on_draw(self):
        self.clear((255,255,255))
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_texture_rectangle(67, SCREEN_HEIGHT / 2, 134, SCREEN_HEIGHT, self.menu)
        self.plants.draw()
        if self.seed != None:
            self.seed.draw()
        arcade.draw_text(f"{self.sun}", 33, 490, (165, 42, 42), 33)
        self.spawn_suns.draw()
        self.peas.draw()
        self.zombie_list.draw()
        if not self.game:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 500, 400, self.end_game)


    def update(self, delta_time):
        if self.game:
            self.plants.update_animation(delta_time)
            self.plants.update()
            self.peas.update()
            self.zombie_list.update()
            self.zombie_list.update_animation(delta_time)
            
            if time.time() - self.zombie_spawn_time > self.attack_time and self.killed_zomdies < 20:
                center_y, line = lawn_y(random.randint(24, 524))
                zombie_type = random.randint(1, 4)
                if zombie_type == 1:
                    self.zombie_list.append(zombies.OrdinaryZombie(center_y, line, self))
                elif zombie_type == 2:
                    self.zombie_list.append(zombies.ConeHeadZombie(center_y, line, self))
                elif zombie_type == 3:
                    self.zombie_list.append(zombies.BuckHeadZombie(center_y, line, self))
                else:
                    self.zombie_list.append(zombies.FlagZombie(center_y, line, self))
                
                    
                self.zombie_spawn_time = time.time()
            if self.killed_zomdies > 20 and len(self.zombie_list) == 0:
                self.game = False
                self.end_game = arcade.load_texture("textures/logo.png")


    def on_mouse_press(self, x, y, button, modifiers):
        if 16 <= x <= 116:
            if 370 <= y <= 480:
                self.seed = plants.SunFlower(self)
            if 255 <= y <= 365:
                self.seed = plants.PeaShooter(self)
            if 140 <= y <= 250:
                self.seed = plants.WallNut(self)
            if 25 <= y <= 135:
                self.seed = plants.TorchWood(self)
        if self.seed != None:
            self.seed.center_x = x
            self.seed.center_y = y
            self.seed.alpha = 150
        for sun in self.spawn_suns:
            if sun.left <= x <= sun.right and sun.bottom <= y <= sun.top:
                sun.kill()
                self.sun += 25
    def on_mouse_motion(self, x, y, dx, dy):
        if self.seed != None:
            self.seed.center_x = x
            self.seed.center_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        if 248 <= x <= 950 and 24 <= y <= 524 and self.seed != None:
            center_x, column = lawn_x(x)
            center_y, row = lawn_y(y)
            if (row, column) in self.lawns or self.sun < self.seed.cost:
                self.seed = None
                return
            self.sun -= self.seed.cost
            self.lawns.append((row, column))
            self.seed.planting(center_x, center_y, row, column)
            self.seed.alpha = 255
            self.plants.append(self.seed)
            self.seed = None
            arcade.play_sound(self.seeding_sound, 0.2)
        else:
            self.seed = None


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
