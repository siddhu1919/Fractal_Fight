import pygame as pg
import time


class Player:
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sfx):
        self.player = player
        self.size = data[0]
        self.scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_sprite_images(sprite_sheet, animation_steps)
        self.action = 0
        self.frameindex = 0
        self.image = self.animation_list[self.action][self.frameindex]
        self.update_time = pg.time.get_ticks()
        self.rect = pg.Rect((x, y, 80, 170))
        self.speed_y = 0
        self.running = False
        self.jump = 1
        self.attacking = 0
        self.action_type = 0  # Idle , Running , Attack1 , Attack2 , Death , TakeHit_white , TakeHit2, Fall , Jump
        self.attack_pause = 0
        self.attack_sound = sfx[0]
        self.jump_sfx = sfx[1]
        self.hit = 0
        self.health = 100  # Change to 100 after Testing
        self.alive = 1

    # ----------------------------------------------------------------------------------------#
    def load_sprite_images(self, sprite_sheet, animation_steps):
        # Extracting The Images From Spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x * self.size, y * self.size, self.size, self.size
                )
                temp_img_list.append(
                    pg.transform.scale(
                        temp_img, (self.scale * self.size, self.scale * self.size)
                    )
                )
            animation_list.append(temp_img_list)
        return animation_list

    # ----------------------------------------------------------------------------------------#
    def move(self, screen_width, screen_height, enemy, game_over):
        SPEED = 50
        GRAVITY = 5
        dx = 0
        dy = 0
        self.running = False
        self.action_type = 0

        # Registering Response From Keyboard
        key = pg.key.get_pressed()
        mouse_click = pg.mouse.get_pressed()

        # Attacking Code
        if self.attacking == 0 and self.alive == 1 and game_over == 0:
            # Controls For PLayer 1
            if self.player == 1:
                # moving the Player Right And Left
                if key[pg.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pg.K_d]:
                    dx = SPEED
                    self.running = True

                # Jump
                if key[pg.K_w] and self.jump == 0:
                    self.speed_y = -60
                    self.jump_sfx.play()
                    self.jump = 1

                # Attack 1 and Attack 2
                if mouse_click[0] or mouse_click[2]:
                    self.attack(enemy)
                    if mouse_click[0]:
                        self.action_type = 1
                    if mouse_click[2]:
                        self.action_type = 2

            # Controls For PLayer 2
            if self.player == 2 and self.alive == 1:
                # moving the Player
                if key[pg.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pg.K_RIGHT]:
                    dx = SPEED
                    self.running = True

                # Jump
                if key[pg.K_UP] and self.jump == 0:
                    self.jump_sfx.play()
                    self.speed_y = -60
                    self.jump = 1

                # Attack 1 and Attack 2
                if key[pg.K_KP1] or key[pg.K_KP2]:
                    self.attack(enemy)
                    if key[pg.K_KP1]:
                        self.action_type = 1
                    if key[pg.K_KP2]:
                        self.action_type = 2

        # Coding Gravity
        self.speed_y += GRAVITY
        dy += self.speed_y

        # Game Window Edge Detection
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 61:
            self.jump = 0
            self.speed_y = 0
            dy = screen_height - 61 - self.rect.bottom

        # To Make Players Always See each other
        if enemy.rect.centerx > self.rect.centerx and self.alive == 1:
            self.flip = False
        else:
            self.flip = True

        # implementing  Attack Cooldown
        if self.attack_pause > 0:
            self.attack_pause -= 1

        # Updating the Player Position
        self.rect.x += dx
        self.rect.y += dy

    # ----------------------------------------------------------------------------------------#
    # Character Animation Function
    def update_animation(self):
        # Alive or Death
        if self.health <= 0:
            self.health = 0
            self.alive = 0
            self.action_update(4)
        # Hitting Player Animation
        elif self.hit == 1:
            self.action_update(5)

        # Attacking Player animation
        elif self.attacking == 1:
            if self.action_type == 1:
                self.action_update(2)
            elif self.action_type == 2:
                self.action_update(3)

        # Jumping Player animation
        elif self.jump == 1:
            self.action_update(8)

        # Runnning Player animation
        elif self.running == True:
            self.action_update(1)
        else:
            self.action_update(0)

        # Animation Sleep Time
        animation_pause = 100  # 15ms
        self.image = self.animation_list[self.action][self.frameindex]
        if pg.time.get_ticks() - self.update_time > animation_pause:
            self.frameindex += 1
            self.update_time = pg.time.get_ticks()
        # Checking the animation has finished or not
        if self.frameindex >= len(self.animation_list[self.action]):
            # If Player Dies
            if self.alive == 0:
                self.frameindex = len(self.animation_list[self.action]) - 1
            else:
                self.frameindex = 0
                # if attack animation is finished
                if self.action == 2 or self.action == 3:
                    self.attacking = 0
                    self.attack_pause = 5  # 0.2 sec
                # If Players got hit
                if self.action == 5:
                    self.hit = 0
                    # WHen both Players Attack at the same time (Action Nullified)
                    self.attacking = False
                    self.attack_pause = 2

    # ----------------------------------------------------------------------------------------#
    # Attacks Method
    def attack(self, enemy):
        if self.attack_pause == 0:
            # Attack Sound
            self.attack_sound.play()
            self.attacking = 1
            attacking_rect = pg.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y,
                2.2 * self.rect.width,
                self.rect.height,
            )
            if attacking_rect.colliderect(enemy.rect):
                enemy.health -= 10
                print("TArget Hit", enemy.health)
                enemy.hit = 1

            # pg.draw.rect(surface, (0, 0, 255), attacking_rect) #

    # ----------------------------------------------------------------------------------------#
    # # Defense Method
    # def defense(self, surface):
    #     defense_rect = pg.Rect(
    #         self.rect.centerx, self.rect.y, 1.1 * self.rect.width, self.rect.height
    #     )
    #     pg.draw.rect(surface, (0, 255, 0), defense_rect)

    # ----------------------------------------------------------------------------------------#
    def action_update(self, nxt_action):
        if nxt_action != self.action:
            self.action = nxt_action
            # updating the Frame Index as well
            self.frameindex = 0
            self.update_time = pg.time.get_ticks()

    # ----------------------------------------------------------------------------------------#
    def draw(self, surface):
        img = pg.transform.flip(self.image, self.flip, False)
        # pg.draw.rect(surface, (255, 0, 0), self.rect) # For Debugging and Testing
        surface.blit(
            img,
            (
                self.rect.x - (self.offset[0] * self.scale),
                self.rect.y - (self.offset[1] * self.scale),
            ),
        )
