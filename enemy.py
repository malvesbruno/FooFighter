import pygame

import death_counter
from settings import *
from entity import Entity
from suport import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, add_exp):

        #setup geral
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # setup graficos
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)


        #movimentação
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprite = obstacle_sprites

        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        #player interação
        self.can_attack = True
        self.attack_cooldown = 400
        self.attack_time = None
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        #timer de vencibilidade
        self.vulnerable = True
        self.hit_time = None
        self.invicibility_duration = 300

        #sessão de sons
        self.death_sound = pygame.mixer.Sound('audio/death.wav')
        self.hitsound = pygame.mixer.Sound('audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.2)
        self.hitsound.set_volume(0.2)
        self.attack_sound.set_volume(0.3)
    def import_graphics(self, monster_name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'graphics/monsters/{monster_name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2((0,0))

        return distance, direction

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'


    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()


    def animate(self):
        animation  = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        if self.monster_name == 'bamboo':
            self.image = pygame.transform.scale(self.image, (60, 60))
        elif self.monster_name == 'raccoon':
            self.image = pygame.transform.scale(self.image, (300, 300))
        elif self.monster_name == 'scorpion':
            self.image = pygame.transform.scale(self.image, (100, 100))
        else:
            self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
           alpha = self.wave_value()
           self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invicibility_duration:
                self.vulnerable = True

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def get_damage(self, player, attack_type):
        self.hitsound.play()
        self.direction = self.get_player_distance_direction(player)[1]
        if self.vulnerable:
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
               self.health -= player.get_full_magic_damage()

        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            if self.monster_name == 'spirit' or self.monster_name == 'scorpion':
                self.trigger_death_particles(self.rect.center, self.monster_name)
            elif self.monster_name == 'raccoon':
                self.trigger_death_particles(self.rect.center - pygame.math.Vector2(80, 65), self.monster_name)
            else:
                self.trigger_death_particles(self.rect.center - pygame.math.Vector2(60, 35), self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()
            death_counter.monster_dead += 1


    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance


    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.cooldown()
        self.actions(player)
