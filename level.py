import random
import time

import pygame
import sys
from settings import *
from tile import Tile
from player import Player
from debug import debug
from suport import import_csv_layout, import_folder
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import *
from magic import MagicPlayer
from upgrade import  Upgrade
from Pause import Pause
from death_screen import Death_Screen
from winner_screen import Winner_Screen
import death_counter



class Level:
    def __init__(self):
        # achar o superfice de display
        self.display_surface = pygame.display.get_surface()
        # setup de grupo de sprites
        self.visible_sprites = YSortCameraGroup()
        self.attack_sprites = pygame.sprite.Group()
        self.hitable_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        # sprite setup
        self.create_map()

        #attack_sprite
        self.current_attack = None

        self.num_morte = 0

        #user_interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.pause = Pause(self.player)
        self.death_screen = Death_Screen(self.player)
        self.winner_screen = Winner_Screen(self.player)
        self.pause_info = True
        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        self.paused = True
        self.game_paused = False



    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])


    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])


    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                colission_sprite = pygame.sprite.spritecollide(attack_sprite, self.hitable_sprites, False)
                if colission_sprite:
                    for target_sprite in colission_sprite:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(70, 75)
                            for leaf in range(random.randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def create_map(self):
        layout = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'object': import_folder('graphics/objects')
        }
        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),
                                 [self.obstacle_sprites, self.visible_sprites, self.hitable_sprites],
                                 'grass',
                                 random_grass_image)
                        if style == 'object':
                            surf = graphics['object'][int(col)]
                            if int(col) == 0:
                                surf = pygame.transform.scale(surf, (150, 150))
                            if int(col) == 2:
                                surf = pygame.transform.scale(surf, (120, 120))
                            if int(col) == 7:
                                surf = pygame.transform.scale(surf, (60, 120))
                            if int(col) == 14:
                                surf = pygame.transform.scale(surf, (220, 240))
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                        if style == 'entities':
                            if col == '9':
                                self.player = Player((x, y),
                                                     [self.visible_sprites],
                                                     self.obstacle_sprites,
                                                     self.create_attack,
                                                     self.destroy_attack,
                                                     self.create_magic)
                            else:
                                if col == '4':
                                    monster_name = 'squid' #squid
                                elif col == '11':
                                    monster_name = 'spirit'
                                    y += 20
                                elif col == '5':
                                    monster_name = 'raccoon'
                                elif col == '3':
                                    monster_name = 'scorpion'
                                else:
                                    monster_name = 'bamboo' #bamboo
                                Enemy(monster_name, (x, y), [self.visible_sprites, self.hitable_sprites], self.obstacle_sprites, self.damage_player, self.trigger_death_particles, self.add_exp)
                                death_counter.monster_count += 1
        #         if col == 'x':
        #             Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':
        #             self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)


    def damage_player(self, amount, attack_type):
        if self.player.vulnarable:
            self.player.health -= amount
            self.player.vulnarable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particle(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particle(particle_type, pos, [self.visible_sprites])


    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def pause_menu(self):
        self.paused = not self.paused


    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)


        numero_ger = False
        if not numero_ger:
            num = random.randint(0, 1)
            numero_ger = True
        if self.player.status == 'winner':
            replay = self.winner_screen.display(death_counter.cont)
            if replay:
                death_counter.monster_count = 0
                death_counter.monster_dead = 0
                self.player.status = 'down'
                self.player.died = False
                replay = False
                self.death_screen.choice = None
                for sprite in self.visible_sprites:
                    sprite.kill()
                for sprite in self.obstacle_sprites:
                    sprite.kill()
                self.create_map()
                self.player.health = self.player.stats['health']
                self.player.energy = self.player.stats['energy']
                self.player.speed = self.player.stats['speed']
                self.player.exp = 100
                self.ui.display(self.player)
                self.upgrade = Upgrade(self.player)
                if self.game_paused:
                    self.upgrade.display()

        if self.game_paused:
            self.upgrade.display()
        elif self.paused:
            self.pause.display()
        else:
            self.visible_sprites.update()
            numero_ger = False
            if not numero_ger:
                num = random.randint(0, 13)
                numero_ger = True
            if self.player.status == 'dead':
                revive = self.death_screen.display(num, death_counter.cont)
                if revive:
                    death_counter.monster_count = 0
                    death_counter.monster_dead = 0
                    self.player.status = 'down'
                    self.player.died = False
                    revive = False
                    self.death_screen.choice = None
                    for sprite in self.visible_sprites:
                        sprite.kill()
                    for sprite in self.obstacle_sprites:
                        sprite.kill()
                    self.create_map()
                    self.player.health = self.player.stats['health']
                    self.player.energy = self.player.stats['energy']
                    self.player.speed = self.player.stats['speed']
                    self.player.exp = 100
                    self.ui.display(self.player)
                    self.upgrade = Upgrade(self.player)
                    if self.game_paused:
                        self.upgrade.display()




            else:
                self.visible_sprites.enemy_update(self.player)
                self.player_attack_logic()



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #criando chão
        image = pygame.image.load('graphics/tilemap/Floor.png').convert()
        image = pygame.transform.scale(image, (3850, 3900))
        self.floor_surface = image
        self.floor_rect = self.floor_surface.get_rect(topleft= (0, 0))

    def custom_draw(self, player):
        #offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos =self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
