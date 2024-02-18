import os

import pygame

from settings import *

class CucumberEnemy(pygame.sprite.Sprite):

        def __init__(self, char_type, x, y, scale, speed):
            pygame.sprite.Sprite.__init__(self)
            self.char_type = char_type
            self.speed = speed
            self.direction = 1
            self.flip = False
            self.jump = False
            self.double_jump = True
            self.in_air = True
            self.vel_y = 0
            self.attack = False
            self.health = 50
            self.collision_occurred = False

            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()

            animation_types = ['Idle','Run','Jump','Attack']

            for animation in animation_types:
                temp_list = []

                n_frames = len(os.listdir(f'assets/enemies/Cucumber/{animation}'))
                for i in range(n_frames):
                    img = pygame.image.load(f'assets/enemies/Cucumber/{animation}/{i}.png')
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                self.animation_list.append(temp_list)

            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.collision_rect = pygame.Rect(self.rect.centerx - self.rect.width / 4 , self.rect.centery - self.rect.height / 2, self.rect.width / 2, self.rect.height)

        def draw(self):
            from main import screen
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
            pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)

        def move(self, move_left, move_right):
            dx = 0
            dy = 0
            if move_left:
                dx -= self.speed
                self.flip = True
                self.direction = -1

            if move_right:
                dx += self.speed
                self.flip = False
                self.direction = 1

            if self.jump and not self.in_air:
                self.vel_y = -11
                self.jump = False
                self.in_air = True

            if self.double_jump and self.in_air:
                self.vel_y = -11
                self.double_jump = False

            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            return dx, dy

        def update_animation(self):
            ANIMATION_COOLDOWN = 75
            self.image = self.animation_list[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

        def update_action(self, new_action):
            if new_action != self.action:
                self.action = new_action
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def check_collision(self, tiles):
            col_tiles = pygame.sprite.spritecollide(self, tiles, False)
            if col_tiles:
                self.in_air = False
                self.double_jump = True
                self.rect.y = col_tiles[0].rect.y - self.rect.height
                self.vel_y = 0
                return True
            return False

        def update(self, move_left, move_right, tiles):
            dx, dy = self.move(move_left, move_right)
            self.rect.x += dx
            self.rect.y += dy
            if self.check_collision(tiles):
                self.in_air = False
                self.double_jump = True
            self.update_animation()
            self.draw()

    # Funcion de daño
        def get_Hit(self, damage):
            self.health -= damage
            print("Vida enemigo:"+self.health)

