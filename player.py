import os
import time

import pygame
from  settings import *
from suport import import_folder
from entity import Entity
import debug
from Pause import Die
import death_counter

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprite, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-20, HITBOX_OFFSET['player'])

        # movimento
        self.attacking = False
        self.attacking_cooldown = 400
        self.attack_time = False
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack

        self.obstacle_sprite = obstacle_sprite

        # setup de gráficos
        self.import_player_assets()
        self.status = 'down'

        # armas
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        #magicas
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None


        self.died = False
        self.die_animation = 1000
        self.death_time = None
        self.death_counter = 0

        self.win = False
        self.winning_animation = 2000
        self.win_time = None

        #stats
        self.stats = {"health": 100, "energy": 60, "attack": 30, "magic": 4, "speed": 6}
        self.max_stats = {"health": 300, "energy": 140, "attack": 80, "magic": 10, "speed": 10}
        self.upgrade_cost = {"health": 100, "energy": 100, "attack": 100, "magic": 100, "speed": 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 100
        self.speed = self.stats['speed']

        # dano timer
        self.vulnarable = True
        self.hurt_time = None
        self.invulnerability = 500

        #import sound
        self.weapon_atacck_sound = pygame.mixer.Sound('audio/sword.wav')
        self.weapon_atacck_sound.set_volume(0.2)
    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': [], 'died': [], 'win': []}


        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)


    def input(self):
        if self.status != 'died' and self.status != 'dead' and self.status != 'win' and self.status != 'winner':
            if not self.attacking:
                key = pygame.key.get_pressed()

                if key[pygame.K_UP]:
                    self.direction.y = -1
                    self.status = 'up'
                elif key[pygame.K_DOWN]:
                    self.direction.y = 1
                    self.status = 'down'
                else:
                    self.direction.y = 0


                if key[pygame.K_RIGHT]:
                    self.direction.x = 1
                    self.status = 'right'
                elif key[pygame.K_LEFT]:
                    self.direction.x = -1
                    self.status = 'left'
                else:
                    self.direction.x = 0

                #input ataque
                if key[pygame.K_SPACE]:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    self.create_attack()
                    self.weapon_atacck_sound.play()

                #input magica
                if key[pygame.K_LCTRL]:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    style = list(magic_data.keys())[self.magic_index]
                    strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                    cost = list(magic_data.values())[self.magic_index]['cost']
                    self.create_magic(style, strength, cost)

                if key[pygame.K_q] and self.can_switch_weapon:
                    self.can_switch_weapon = False
                    self.weapon_switch_time = pygame.time.get_ticks()
                    if self.weapon_index < len(list(weapon_data.keys())) - 1:
                        self.weapon_index += 1
                    else:
                        self.weapon_index = 0


                    self.weapon = list(weapon_data.keys())[self.weapon_index]


                if key[pygame.K_e] and self.can_switch_magic:
                    self.can_switch_magic = False
                    self.magic_switch_time = pygame.time.get_ticks()
                    if self.magic_index < len(list(magic_data.keys())) - 1:
                        self.magic_index += 1
                    else:
                        self.magic_index = 0


                    self.magic = list(magic_data.keys())[self.magic_index]
        else:
            pass


    def get_status(self):
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not '_idle' in self.status and not '_attack' in self.status and 'died' not in self.status and not 'dead' in self.status and not 'win' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not '_attack' in self.status and 'died' not in self.status and not 'dead' in self.status and not 'win' in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if '_attack' in self.status:
                self.status = self.status.replace('_attack', '')
    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.status == 'win':
            if current_time - self.win_time >= self.winning_animation:
                self.status = 'winner'
        if self.status == 'died':
            if current_time - self.death_time >= self.die_animation:
                self.status = 'dead'
        if not self.vulnarable:
            if current_time - self.hurt_time >= self.invulnerability:
                self.vulnarable = True

        if self.attacking:
            if current_time - self.attack_time >= self.attacking_cooldown + weapon_data[self.weapon]['cooldown']:

                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True



        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True


    def animate(self):
        if not self.status == 'dead' and not self.status == 'winner':
            animation = self.animations[self.status]
        else:
            animation = self.animations['died']
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # imagem
        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if not self.vulnarable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return  base_damage + spell_damage

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]


    def energy_recovery(self):
        if self.energy <= self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def die(self):
        if self.health <= 0:
            if self.died == False:
                self.status = 'died'
                self.died = True
                self.death_time = pygame.time.get_ticks()
                death_counter.cont += 1
                self.upgrade_cost = {"health": 100, "energy": 100, "attack": 100, "magic": 100, "speed": 100}
                self.health = self.stats['health']
                self.energy = self.stats['energy']
                self.exp = 100
                self.speed = self.stats['speed']
                # print(death_counter.cont)

    def winner(self):
        if death_counter.monster_dead == death_counter.monster_count:
            if self.win == False:
                self.status = 'win'
                self.win = True
                self.win_time = pygame.time.get_ticks()
                self.upgrade_cost = {"health": 100, "energy": 100, "attack": 100, "magic": 100, "speed": 100}
                self.health = self.stats['health']
                self.energy = self.stats['energy']
                self.exp = 100
                self.speed = self.stats['speed']






    def update(self):
        self.input()
        self.die()
        self.winner()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
