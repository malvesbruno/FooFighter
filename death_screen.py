import time

import pygame
from settings import *
from math import sin
from time import sleep
import random


class Death_Screen:
    def __init__(self, player):
        #setup geral
        self.item_list = []
        self.bg = pygame.image.load('graphics/pause/bg.png').convert_alpha()
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(PAUSE_FONT, PAUSE_FONT_SIZE)
        self.game_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # sistema de seleção
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

        # criação dos items
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        self.option = ['press R to try again']

        self.choice = None

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:

            if keys[pygame.K_r]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                choice = self.item_list[self.selection_index].trigger(self.option, self.display_surface)
                return choice



    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True


    def display(self, num, n_death):
        choice = self.input()
        self.selection_cooldown()
        if choice:
            self.choice = choice
        if self.choice:
            if self.choice == 'quit':
                self.choice = None
                return True



        else:
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGTH))
            self.display_surface.blit(self.bg, (0, 0))

            pos = (WIDTH // 2 - 100, HEIGTH // 4)
            text_surf = self.font.render('RED JAM', False, '#880808')
            text_surf_rect = text_surf.get_rect(topleft=pos)
            text_surf_rect = text_surf_rect.inflate(600, 2000)
            pygame.draw.rect(self.display_surface, '#880808', text_surf_rect, 0, 3)

            # self.display_surface.blit(text_surf, text_surf_rect)

            for index, item in enumerate(self.item_list):
                item.display(self.display_surface, self.selection_index, self.option[index], text_surf_rect, num, n_death),


    def create_items(self):
        for item, index in enumerate(range(1)):
            # posição horizontal

            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2

            # posição vertical
            top = self.display_surface.get_size()[1] * 0.1

            # criando item
            item = Item(left, top, self.width, self.height, index, self.game_font )
            self.item_list.append(item)



class Item:
    def __init__(self, left, t, w, h, index, font):
        self.rect = pygame.Rect(left, t, w, h)
        self.left = left
        self.top = t
        self.width = w
        self.height = h
        self.index = index
        self.font = font
        self.game_font = pygame.font.Font(PAUSE_FONT, 40)
        self.selection_number = 0
        self.frase_select = False
        self.frase = None

        self.title_death = None
        self.list_deaths = []

        self.frases = ['foi de arrasta pra cima...',
                       'foi de americanas...',
                       'foi de comes e bebes...',
                       'foi de base...',
                       'foi jogar no vasco...',
                       'foi de gigante da colina...',
                       'foi de arthur morgan...',
                       'foi de john marston...',
                       'foi de drake e josh...',
                       'foi de achados e perdidos...',
                       'foi de parte 2...',
                       'foi de berço...',
                       'foi mimir...',
                       'foi de camera em 3º pessoa...']
        self.media = 0
        self.num = 0

    def trigger(self, option, surface):
        if option[self.selection_number] == 'start':
            return 'start'
        elif option[self.selection_number] == 'controls':
            return 'control'
        else:
            return 'quit'



    def display_names(self, surface, name, selected, rect, pos):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR


        #titulo
        title_surf = self.font.render(name, False, '#FFFFFF')
        tile_rect = title_surf.get_rect(center=rect.center)

        #draw
        surface.blit(title_surf, tile_rect)






    def display(self, surface, selection_num, name, rect, num, n_death):
        self.num = num
        if n_death not in self.list_deaths:
            self.list_deaths.append(n_death)
            self.frase_select = False
        if not self.frase_select:
            self.frase = self.frases[int(self.num)]
            self.frase_select = True


        self.selection_number = selection_num
        x = surface.get_size()[0] // 2
        y = (rect.centery + 130) + (150 * self.index) // 2
        rect_use = pygame.Rect(x - 200, y, 400, 50)
        if self.index == selection_num:
            pygame.draw.rect(surface, '#CC5500', rect_use)
            pygame.draw.rect(surface, "#FFFFFF", rect_use, 4)

        else:
            pygame.draw.rect(surface, '#CC5500', rect_use)
            pygame.draw.rect(surface, "#FFFFFF", rect_use, 4)
        self.display_names(surface, name, self.index == selection_num, rect_use, (x, y))

        if self.frase_select:
            soma = 0
            for c in self.frases:
                soma += len(c)
            self.media = soma//len(self.frase)


        pos = (x, rect.centery + 20)
        if self.frase_select:
            text = self.game_font.render(self.frase, False, "#CC5500")
            text_rect = text.get_rect(center=pos)
            rect_bg = text_rect
            rect_bg.center = text_rect.center
            rect_bg = rect_bg.inflate(10, 20)
            pygame.draw.rect(surface, '#880808', rect_bg, 1, 1)
            surface.blit(text, text_rect)

