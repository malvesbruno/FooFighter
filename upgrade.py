import pygame
from settings import *

class Upgrade:
    def __init__(self, player):
        #setup geral
        self.item_list = []
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # sistema de seleção
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

        # criação dos items
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()


    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.attribute_number - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)


    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_items(self):
        for item, index in enumerate(range(self.attribute_number)):
            #posição horizontal
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2

            #posição vertical
            top = self.display_surface.get_size()[1] * 0.1

            #criando item
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()
        for index, item in enumerate(self.item_list):

            # pegando atributos
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)


            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


class Item:
    def __init__(self, left, t, w, h, index, font):
        self.rect = pygame.Rect(left, t, w, h)
        self.index = index
        self.font = font

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR


        #titulo
        title_surf = self.font.render(name, False, color)
        tile_rect = title_surf.get_rect(midtop= self.rect.midtop + pygame.math.Vector2(0, 20))


        #custo
        cost_surf = self.font.render(str(cost), False, color)
        cost_rect = cost_surf.get_rect(midtop=self.rect.midbottom - pygame.math.Vector2(0, 40))

        #draw
        surface.blit(title_surf, tile_rect)
        surface.blit(cost_surf, cost_rect)

    def display_bar(self, surface, value, max_value, selected):
        # setup drawing
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        #setup da barra
        full_height = bottom[1] - top[1]
        relative_number = (value/max_value) * full_height
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        # desenhar elemento
        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)


    def trigger(self, player):
        upgrade_atribute = list(player.stats.keys())[self.index]
        print(player.exp, player.upgrade_cost[upgrade_atribute])
        if player.exp >= player.upgrade_cost[upgrade_atribute] and player.stats[upgrade_atribute] < player.max_stats[upgrade_atribute]:
            player.exp -= player.upgrade_cost[upgrade_atribute]
            player.stats[upgrade_atribute] *= 1.2
            player.upgrade_cost[upgrade_atribute] *= 1.4
            player.upgrade_cost[upgrade_atribute] = int(player.upgrade_cost[upgrade_atribute])
        if player.stats[upgrade_atribute] > player.max_stats[upgrade_atribute]:
            player.stats[upgrade_atribute] = player.max_stats[upgrade_atribute]


    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_names(surface, name, cost, self.index == selection_num)
        self.display_bar(surface, value, max_value, self.index == selection_num)