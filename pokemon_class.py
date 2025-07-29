import pygame
import math
import random
import time
from urllib.request import urlopen
import io
import requests
from move import Move

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, level, x, y):
        super().__init__()
        self.name = name
        self.level = level
        self.x = x
        self.y = y
        self.num_potions = 3
        self.size = 150

        # Запит до API покемона
        req = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name.lower()}')
        self.json = req.json()

        # Отримати базові стати
        for stat in self.json['stats']:
            stat_name = stat['stat']['name']
            base_stat = stat['base_stat']
            if stat_name == 'hp':
                self.max_hp = base_stat + self.level
                self.current_hp = self.max_hp
            elif stat_name == 'attack':
                self.attack = base_stat
            elif stat_name == 'defense':
                self.defense = base_stat
            elif stat_name == 'speed':
                self.speed = base_stat

        # Типи
        self.types = [t['type']['name'] for t in self.json['types']]

        self.set_sprite('front_default')

    def set_sprite(self, side):
        image_url = self.json['sprites'][side]
        image_stream = urlopen(image_url).read()
        image_file = io.BytesIO(image_stream)
        self.image = pygame.image.load(image_file).convert_alpha()
        scale = self.size / self.image.get_width()
        new_w = int(self.image.get_width() * scale)
        new_h = int(self.image.get_height() * scale)
        self.image = pygame.transform.scale(self.image, (new_w, new_h))

    def set_moves(self):
        self.moves = []
        for move_entry in self.json['moves']:
            versions = move_entry['version_group_details']
            for version in versions:
                if version['version_group']['name'] != 'red-blue':
                    continue
                if version['move_learn_method']['name'] != 'level-up':
                    continue
                if self.level >= version['level_learned_at']:
                    move = Move(move_entry['move']['url'])
                    if move.power is not None:
                        self.moves.append(move)
        if len(self.moves) > 4:
            self.moves = random.sample(self.moves, 4)

    def perform_attack(self, other, move):
        display_message(f'{self.name} used {move.name}!')
        time.sleep(2)
        damage = (2 * self.level + 10) / 250 * self.attack / other.defense * move.power
        if move.type in self.types:
            damage *= 1.5  # STAB
        if random.randint(1, 10000) <= 625:
            damage *= 1.5  # критичний удар
        damage = math.floor(damage)
        other.take_damage(damage)

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0

    def use_potion(self):
        if self.num_potions > 0:
            self.current_hp += 30
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp
            self.num_potions -= 1

    def draw(self, surface, alpha=255):
        sprite = self.image.copy()
        sprite.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        surface.blit(sprite, (self.x, self.y))

    def draw_hp(self, surface):
        bar_scale = 200 // self.max_hp
        for i in range(self.max_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(surface, (200, 0, 0), bar)
        for i in range(self.current_hp):
            bar = (self.hp_x + bar_scale * i, self.hp_y, bar_scale, 20)
            pygame.draw.rect(surface, (0, 200, 0), bar)
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'HP: {self.current_hp} / {self.max_hp}', True, (0,0,0))
        surface.blit(text, (self.hp_x, self.hp_y + 25))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

def display_message(message):
    # Тут просто placeholder. Цю функцію імпортуємо у main.py
    pass
