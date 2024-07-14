import time

import pygame
from settings import *
from math import sin
from time import sleep
import death_counter


class Pause:
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
        self.history_font = pygame.font.Font(UI_FONT, 10)

        # sistema de seleção
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

        self.history = ['',
                        'Era uma vez, em um distante mundo,',
                        'uma bandeira que cobria uma corja seleta de guerreiros',
                        'A ordem dos Guerreiros de foo',
                        'nascidos e treinados para proteger os inocentes...',
                        'Sua crença de um pós vida de fartura',
                        'É o que os motivava à lutar',
                        'lutar para um mundo melhor',
                        'para se encontrarem em um mundo melhor',
                        'o nirvana',
                        'Porém, para ter essa honra',
                        'os guerreiros deveriam servir e viver pela justiça',
                        'se privando do si e de seus anseios naturais',
                        'nenhum guerreiro ousava desobedecer isso',
                        'o temor da ira dos deuses',
                        'era maior que qualquer paixão na terra...',
                        'Isso foi por muito tempo',
                        'mas o destino virá a mudar',
                        'Um dia o capitão do exército principal',
                        'se viu apaixonado pela esposa de um dos demônios de jade,',
                        'um grupo de ladrões que não possuiam mais salvação',
                        'e por sorte, ela também se apaixonara por ele',
                        'a pressão sobre o casal de amantes era grande',
                        'a irá dos deuses, a irá dos guerreiros e demônios',
                        'ainda assim, o romance perdurou por muito tempo',
                        'até que o marido dela, demônio de jade,',
                        'perecebe o sumiço de sua esposa',
                        'e a encontra com o capitão em uma fonte longe da cidade',
                        'ela demonstrava tanto amor por um de seus inimigos',
                        'que o demônio de jade, com ódio e amargor em seu coração,',
                        'relata a blasfêmia aos deueses',
                        'E recebe a ordem de executá-los para que a justiça seja feita',
                        'ele sabia que não conseguiria matar o seu amor',
                        'ele decide se livrar somente do capitão',
                        'arma uma emboscada no local onde o capitão encontrava sua esposa',
                        'o capitão morre lutando',
                        'os deuses o convocam para destinir o seu destino',
                        'ele clama pro piedade',
                        'os deuses o oferecem um desafio',
                        'o sofrimento eterno ou a vida e o amor de sua amada',
                        'mas ele precisaria andar pelo o caminho do inverno',
                        'ele enfrentar, o Dinre, o demônio primordial',
                        'o único ser, que é capaz de enfrentá-los',
                        'o unico ser que nem eles conseguiam exterminar...',
                        'Presione Enter Para Jogar']
        self.cont = 0

        # criação dos items
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        self.option = ['start', 'controls', 'quit']

        self.choice = None


        self.can_switch = True
        self.switch_time = None
        self.time_switch = 200

        self.move = []


    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_DOWN] and self.selection_index < self.attribute_number - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
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


    def display(self):
        choice = self.input()
        self.selection_cooldown()
        if choice:
            self.choice = choice
        if self.choice:
            if self.choice == 'start':
                self.display_surface.fill('#393939')

                pos = (WIDTH // 2 - 300, HEIGTH // 2 - 20)
                if 'Jogar' in self.history[self.cont]:
                    text = self.game_font.render(self.history[self.cont], False, '#393939')
                else:
                    text = self.game_font.render(self.history[self.cont], False, TEXT_COLOR)
                rect_text = text.get_rect(topleft=pos)
                rect_text2 = rect_text
                rect_text2 = rect_text2.inflate(200, 200)

                pos = (WIDTH // 2 - 140, HEIGTH // 2 + 100)
                text_surf = self.game_font.render('Press Enter to skip...', False, '#393939')
                text_surf_rect = text_surf.get_rect(topleft=pos)
                rect = text_surf_rect
                rect.center = text_surf_rect.center
                rect = rect.inflate(50, 50)
                rect2 = rect
                pygame.draw.rect(self.display_surface, '#000000', rect_text, 0, 3)
                pygame.draw.rect(self.display_surface, '#393939', rect_text2, 0, 3)
                if 'Jogar' in self.history[self.cont]:
                    pygame.draw.rect(self.display_surface, '#FFFFFF', rect_text2, 0, 3)
                else:
                    pygame.draw.rect(self.display_surface, '#FFFFFF', rect_text2, 2, 3)
                self.display_surface.blit(text, rect_text)

                if 'Jogar' not in self.history[self.cont]:
                    pygame.draw.rect(self.display_surface, '#000000', text_surf_rect, 0, 3)
                    pygame.draw.rect(self.display_surface, '#393939', rect, 0, 3)
                    pygame.draw.rect(self.display_surface, '#FFFFFF', rect, 0, 3)
                    self.display_surface.blit(text_surf, text_surf_rect)


                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.choice = None
                    self.cont = 0
                if keys[pygame.K_BACKSPACE]:
                    self.choice = None
                    self.cont = 0
                if keys[pygame.K_SPACE]:
                    if len(self.move) == 0 and self.cont < len(self.history) - 1:
                        self.switch_time = pygame.time.get_ticks()
                        self.cont += 1
                        self.move.append('')

                    current_time = pygame.time.get_ticks()
                    if current_time - self.switch_time >= self.time_switch:
                        self.move.clear()


            if self.choice == 'control':
                self.display_surface.fill('#393939')
                pos = (WIDTH // 2 - 300, HEIGTH // 2 - 250)
                image = pygame.image.load('graphics/controls/controls.png').convert_alpha()
                image = pygame.transform.scale(image, (600, 400))
                text_surf_rect = image.get_rect(topleft=pos)
                rect = text_surf_rect
                rect.center = text_surf_rect.center
                rect = rect.inflate(200, 200)
                rect2 = rect
                pygame.draw.rect(self.display_surface, '#000000', text_surf_rect, 0, 3)
                pygame.draw.rect(self.display_surface, '#393939', rect, 0, 3)
                pygame.draw.rect(self.display_surface, '#FFFFFF', rect, 2, 3)
                self.display_surface.blit(image, text_surf_rect)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_BACKSPACE]:
                    self.choice = None
            if self.choice == 'quit':
                pygame.quit()



        else:
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGTH))
            self.display_surface.blit(self.bg, (0, 0))

            pos = (WIDTH // 2 - 100, HEIGTH // 4)
            text_surf = self.font.render('NIGHT IN HELL', False, TEXT_COLOR)
            text_surf_rect = text_surf.get_rect(topleft=pos)
            text_surf_rect = text_surf_rect.inflate(300, 2000)
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_surf_rect, 0, 3)

            self.display_surface.blit(text_surf, text_surf_rect)

            for index, item in enumerate(self.item_list):
                item.display(self.display_surface, self.selection_index, self.option[index], text_surf_rect),
        if self.choice == 'start':
            pos = (self.display_surface.get_size()[0] - 20, self.display_surface.get_size()[1] -20)
            image = pygame.image.load('graphics/controls/100 Sem Título_20230824173415.png').convert_alpha()
            image = pygame.transform.scale(image, (130, 80))
            text_surf_rect = image.get_rect(bottomright=pos)
            text = self.game_font.render('To Return', False, TEXT_COLOR)
            rect = text_surf_rect
            rect.center = text_surf_rect.center
            rect = rect.inflate(20, 20)
            rect2 = rect
            pygame.draw.rect(self.display_surface, '#000000', text_surf_rect, 0, 3)
            pygame.draw.rect(self.display_surface, '#393939', rect, 0, 3)
            pygame.draw.rect(self.display_surface, '#FFFFFF', rect, 2, 3)
            self.display_surface.blit(image, text_surf_rect)
            self.display_surface.blit(text, rect)



            pos = (self.display_surface.get_size()[0] - 20 - rect.width - 20, self.display_surface.get_size()[1] - 30)
            image = pygame.image.load('graphics/controls/controls - Copia.png').convert_alpha()
            image = pygame.transform.scale(image, (160, 60))
            text_surf_rect = image.get_rect(bottomright=pos)
            text = self.game_font.render('To next page', False, TEXT_COLOR)
            rect = text_surf_rect
            rect.center = text_surf_rect.center
            rect = rect.inflate(2, 40)
            rect2 = rect
            pygame.draw.rect(self.display_surface, '#000000', text_surf_rect, 0, 3)
            pygame.draw.rect(self.display_surface, '#393939', rect, 0, 3)
            pygame.draw.rect(self.display_surface, '#FFFFFF', rect, 2, 3)
            self.display_surface.blit(image, text_surf_rect)
            self.display_surface.blit(text, rect)
        else:
            pos = (self.display_surface.get_size()[0] - 20, self.display_surface.get_size()[1] - 20)
            image = pygame.image.load('graphics/controls/100 Sem Título_20230824173415.png').convert_alpha()
            image = pygame.transform.scale(image, (130, 80))
            text_surf_rect = image.get_rect(bottomright=pos)
            text = self.game_font.render('To Return', False, TEXT_COLOR)
            rect = text_surf_rect
            rect.center = text_surf_rect.center
            rect = rect.inflate(2, 20)
            rect2 = rect
            pygame.draw.rect(self.display_surface, '#000000', text_surf_rect, 0, 3)
            pygame.draw.rect(self.display_surface, '#393939', rect, 0, 3)
            pygame.draw.rect(self.display_surface, '#FFFFFF', rect, 2, 3)
            self.display_surface.blit(image, text_surf_rect)
            self.display_surface.blit(text, rect)

            pos = (self.display_surface.get_size()[0] - 20 - rect.width - 20, self.display_surface.get_size()[1] - 30)
            image = pygame.image.load('graphics/controls/controls - Copia.png').convert_alpha()
            image = pygame.transform.scale(image, (130, 60))
            text_surf_rect = image.get_rect(bottomright=pos)
            text = self.game_font.render('To enter', False, TEXT_COLOR)
            rect = text_surf_rect
            rect.center = text_surf_rect.center
            rect = rect.inflate(2, 40)
            rect2 = rect
            pygame.draw.rect(self.display_surface, '#000000', text_surf_rect, 0, 3)
            pygame.draw.rect(self.display_surface, '#393939', rect, 0, 3)
            pygame.draw.rect(self.display_surface, '#FFFFFF', rect, 2, 3)
            self.display_surface.blit(image, text_surf_rect)
            self.display_surface.blit(text, rect)

    def create_items(self):
        for item, index in enumerate(range(3)):
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

    def display_names(self, surface, name, selected, rect):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR


        #titulo
        title_surf = self.font.render(name, False, color)
        tile_rect = title_surf.get_rect(center=rect.center)

        #draw
        surface.blit(title_surf, tile_rect)


    def trigger(self, option, surface):
        if option[self.selection_number] == 'start':
            return 'start'
        elif option[self.selection_number] == 'controls':
            return 'control'
        else:
            return 'quit'







    def display(self, surface, selection_num, name, rect):
        self.selection_number = selection_num
        x = rect.centerx - 150
        y = (rect.centery + 130) + (150 * self.index) // 2
        rect_use = pygame.Rect(x, y, 300, 50)
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, rect_use)
            pygame.draw.rect(surface, "#FFFFFF", rect_use, 4)

        else:
            pygame.draw.rect(surface, UI_BG_COLOR, rect_use)
            pygame.draw.rect(surface, "#FFFFFF", rect_use, 4)
        self.display_names(surface, name, self.index == selection_num, rect_use)


        pos = (x + 65, rect.centery + 20)
        text = self.game_font.render('Foo Fighter', False, "#FFFFFF")
        text_rect = text.get_rect(topleft=pos)
        rect_bg = text_rect
        rect_bg.center = text_rect.center
        rect_bg = rect_bg.inflate(100, 20)
        pygame.draw.rect(surface, '#FFFFFF', rect_bg, 2, 3)
        surface.blit(text, text_rect)


class Die:
    def __init__(self):
        #setup geral
        self.item_list = []
        self.bg = pygame.image.load('graphics/pause/bg.png').convert_alpha()
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(PAUSE_FONT, PAUSE_FONT_SIZE)
        self.game_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # sistema de seleção
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

        # criação dos items
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.die()

        self.option = ['start', 'controls', 'quit']

        self.choice = None

    def die(self):
        self.display_surface.fill('#393939')

        pos = (WIDTH // 2 - 140, HEIGTH // 2 - 20)
        text_surf = self.game_font.render('You Died...', False, TEXT_COLOR)
        text_surf_rect = text_surf.get_rect(topleft=pos)
        rect = text_surf_rect
        rect.center = text_surf_rect.center
        rect = rect.inflate(200, 200)
        rect2 = rect
        pygame.draw.rect(self.display_surface, '#000000', text_surf_rect, 0, 3)
        pygame.draw.rect(self.display_surface, '#393939', rect, 0, 3)
        pygame.draw.rect(self.display_surface, '#FFFFFF', rect, 2, 3)
        self.display_surface.blit(text_surf, text_surf_rect)
        keys = pygame.key.get_pressed()
        time.sleep(5)