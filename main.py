import pygame
import sys
from settings import *
from debug import debug
from  level import  Level
from tile import Tile
from player import  Player
import death_counter

class Game:
    def __init__(self):

        #setup geral
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        icon = pygame.image.load('graphics/player/down_attack/attack_down.png').convert_alpha()
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Foo Fighter')
        self.clock = pygame.time.Clock()
        self.cont = 0

        self.level = Level()
        self.main_music = pygame.mixer.Sound('audio/Rearviewmirror.mp3')
        self.main_music.play(loops=-1)
        self.cont = 0
        self.win_music = pygame.mixer.Sound('audio/Times Like These.mp3')
        self.loss_music = pygame.mixer.Sound('audio/Love, Hate, Love .mp3')
        self.running = True

        self.playing = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        self.level.pause_menu()
                        if self.cont % 2 == 0 and self.cont == 0:
                            self.main_music.stop()
                            self.main_music.play(loops=-1)
                            print(self.cont)
                        elif self.cont % 2 == 0:
                            self.main_music.set_volume(1)
                            print(self.cont)
                        elif self.cont % 2 == 1:
                            self.main_music.set_volume(0.05)
                        else:
                            self.main_music.play(loops= -1)
                            print(self.cont)
                        self.cont += 1
            if death_counter.monster_count == death_counter.monster_dead:
                if not self.playing:
                    self.main_music.set_volume(0.001)
                    self.win_music.play(loops=-1)
                    self.playing = True
            elif self.level.player.status == 'dead':
                if not self.playing:
                    self.main_music.set_volume(0.001)
                    self.loss_music.play(loops=-1)
                    self.playing = True
            elif self.level.player.status != 'dead' and death_counter.monster_count != death_counter.monster_dead:
                try:
                    self.win_music.stop()
                    self.loss_music.stop()
                    self.main_music.set_volume(1)
                except:
                    pass
                self.playing = False
            try:
                self.screen.fill("#FFFF00")
            except:
                pass
            running = self.level.run()
            if running == 'restart':
                running = self.level.run()
            pygame.display.update()
            self.clock.tick((FPS))





if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except:
        pass