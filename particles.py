import pygame
from suport import import_folder
from random import choice


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),

            #attacks
            'claw': import_folder('graphics/particles/claw'),
            'slash': import_folder('graphics/particles/slash'),
            'sparkle': import_folder('graphics/particles/fire'),
            'leaf_attack': import_folder('graphics/particles/leaf_attack'),
            'thunder': import_folder('graphics/particles/thunder'),

            #monster deaths
            'squid': import_folder('graphics/particles/fire'),
            'raccoon': import_folder('graphics/particles/fire'),
            'spirit': import_folder('graphics/particles/smoke2'),
            'bamboo': import_folder('graphics/particles/fire'),
            'scorpion': import_folder('graphics/particles/nova'),

            #leafs
            'leafs': (
                import_folder('graphics/particles/rock1'),
                import_folder('graphics/particles/rock2'),
                self.reflect_images(import_folder('graphics/particles/rock1')),
                self.reflect_images(import_folder('graphics/particles/rock2')),
            )
        }
        self.player = None

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leafs'])
        ParticleEffect(pos, animation_frames, groups, 'rock')

    def create_particle(self, animation_type, pos, groups, player=None):
        animation_frames = self.frames[animation_type]
        if player:
            ParticleEffect(pos, animation_frames, groups, animation_type, player)
        else:
            ParticleEffect(pos, animation_frames, groups, animation_type)



class ParticleEffect(pygame.sprite.Sprite):

    def __init__(self, pos, animation_frames, groups, sprite_type, player=None):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.player = player

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
            if self.sprite_type == 'rock':
                self.image = pygame.transform.scale(self.image, (150, 150))
            if self.sprite_type == 'flame':
                if self.player:
                    self.image = pygame.transform.scale(self.image, (50, 50))
                    self.image.set_alpha(-255)
                    cont = 0
                    if 'left' in self.player.status and cont == 0 and self.player.attacking:
                        self.image.set_alpha(255)
                        self.image = pygame.transform.flip(self.image, True, False)

                    elif 'down' in self.player.status and cont == 0 and self.player.attacking:
                        self.image.set_alpha(255)
                        self.image = pygame.transform.rotate(self.image, 270)
                        cont += 1
                    elif 'up' in self.player.status and cont == 0 and self.player.attacking:
                        self.image.set_alpha(255)
                        self.image = pygame.transform.rotate(self.image, 90)
                        cont += 1
                    elif 'right' in self.player.status and cont == 0 and self.player.attacking:
                        self.image.set_alpha(255)
                        self.image = self.image
                        cont += 1
                    else:
                        pass

            if self.sprite_type == 'squid':
                self.image = pygame.transform.scale(self.image, (90, 90))
            if self.sprite_type == 'bamboo':
                self.image = pygame.transform.scale(self.image, (90, 90))
            if self.sprite_type == 'raccoon':
                self.image = pygame.transform.scale(self.image, (250, 250))
            if self.sprite_type == 'sparkle':
                self.image = pygame.transform.scale(self.image, (30, 30))


    def update(self):
        self.animate()
