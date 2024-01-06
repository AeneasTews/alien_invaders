import os.path
import pygame as pg
import loading_tools as lt
import time
import random

main_dir = os.path.split(os.path.abspath(__file__))[0]
loader = lt.Loader(main_dir)


def check_win_condition():
    if len(enemies.sprites()) == 0:
        switch_state('win')


def switch_direction():
    global alien_direction
    alien_direction *= -1

    for enemy in enemies:
        enemy.move_down()


# TODO: add more aliens, add shots fired from aliens, fix the delta time on all aliens
class Alien(pg.sprite.Sprite):
    def __init__(self, images, position, animation_time, shot_time):
        pg.sprite.Sprite.__init__(self)
        self.area = screen.get_rect()

        self.images, self.rect = loader.load_images(names=images, colorkeys=[-1, -1, -1], scale=5)
        self.image_counter = 0
        self.image_timer = 0
        self.image = self.images[self.image_counter]
        self.animation_time = animation_time

        self.speed = 100

        top_offset = 10
        self.rect.center = position[0] + self.rect.width / 2, position[1] + self.rect.height / 2 + top_offset
        self.step_down = 50

        self.shot_timer = 0
        self.shot_time = shot_time
        self.shot_probability = 100

        enemies.add(self)

    def update(self):
        self._move()
        self._check_hit()
        self._animate()
        self._shoot()

    def _move(self):
        new_pos = self.rect.move(self.speed * dt * alien_direction, 0)

        if new_pos.right >= self.area.right or new_pos.left <= 0:
            switch_direction()
            new_pos = self.rect.move(self.speed * dt * alien_direction, 0)

        self.rect = new_pos

    def _check_hit(self):
        if pg.sprite.spritecollide(sprite=self, group=gun_shots, dokill=True):
            self.kill()

    def move_down(self):
        self.rect.y += self.step_down

    def _animate(self):
        self.image_timer += dt

        if self.image_timer >= self.animation_time:
            self.image_counter = self.image_counter + 1 if self.image_counter < len(self.images) - 1 else 0
            self.image_timer = 0

        self.image = self.images[self.image_counter]

    def _shoot(self):
        self.shot_timer += dt

        if self.shot_timer >= self.shot_time and random.randint(0, self.shot_probability) == 0:
            Shot(self.rect.midbottom, 500)
            self.shot_timer = 0


class Gun(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.area = screen.get_rect()

        self.image, self.rect = loader.load_image(name='gun.png', colorkey=(0, 0, 0), scale=4)
        self.speed = 300

        self.rect.midbottom = self.area.midbottom[0], self.area.midbottom[1]

        self.shot_delay = 0.2
        self.last_shot = 0

        gun.add(self)

    def update(self):
        self._check_input()
        self._check_collision()
        self._check_hit()

    def _move(self, direction, multiplier=1.0):
        if direction == 'right':
            new_pos = self.rect.move(self.speed * dt * multiplier, 0)

            if new_pos.right <= self.area.right:
                self.rect = new_pos

        if direction == 'left':
            new_pos = self.rect.move(-self.speed * dt, 0)

            if new_pos.left >= 0:
                self.rect = new_pos

    # add a variable that is set to true whenever the shoot button is pressed, this will be set to false if it is not
    # contained in the pg.get_pressed() on a frame. only then can the shoot button be pressed again
    def _check_input(self):
        self.last_shot -= dt

        if len(joysticks) == 0:
            keys_down = pg.key.get_pressed()

            if keys_down[pg.K_LEFT]:
                self._move('left')

            if keys_down[pg.K_RIGHT]:
                self._move('right')

            if keys_down[pg.K_SPACE] and self.last_shot <= 0:
                self._shoot()
                self.last_shot = self.shot_delay
        else:
            self._move('right', joysticks[joy_stick_id.get_instance_id()].get_axis(0))

            if joysticks[joy_stick_id.get_instance_id()].get_button(2) and self.last_shot <= 0:
                self._shoot()
                self.last_shot = self.shot_delay

    def _shoot(self):
        Shot(self.rect.midtop, -500)

    def _check_collision(self):
        if pg.sprite.spritecollide(self, group=enemies, dokill=True):
            print('Game Over!')
            pg.quit()
            exit()

    def _check_hit(self):
        if pg.sprite.spritecollide(self, group=enemies, dokill=True):
            print('Game Over!')
            pg.quit()
            exit()


class Shot(pg.sprite.Sprite):
    def __init__(self, midbottom, speed):
        pg.sprite.Sprite.__init__(self)

        self.image, self.rect = loader.load_image(name='shot.png', scale=4)
        self.speed = speed

        self.rect.midbottom = midbottom

        all_sprites.add(self)
        if self.speed < 0:
            gun_shots.add(self)
        else:
            enemy_shots.add(self)

    def update(self):
        self._move()

    def _move(self):
        self.rect = self.rect.move(0, self.speed * dt)

        if self.rect.bottom <= 0:
            self.kill()


class Button(pg.sprite.Sprite):
    """
    This class is used to represent a button. Besides its looks, the button can also handle a hover, and a click
    function which executes when the button is pressed.
    """

    # def __init__(self, image, center_x, center_y, on_press, colorkey=None, scale=1, mouse_button=0):
    #    """
    #    The constructor of the button class
    #    :param image: A single image of the button, this does not change if the button is hovered over or pressed
    #    :param center_x: Center x of button on screen
    #    :param center_y: Center y of button on screen
    #    :param on_press: A function that executes when the button is pressed
    #    :param colorkey: The colorkey to be passed to the load_image function that is used to load the buttons image
    #    :param scale: The scale of the buttons image and thus the button
    #    :param mouse_button: The mouse button that should be checked for clicks. 0, 1, 2
    #    """
    #    pg.sprite.Sprite.__init__(self)

    #    self.image, self.rect = loader.load_image(name=image, colorkey=colorkey, scale=scale)
    #    self.rect.center = center_x, center_y

    #    self.press_func = on_press
    #    self.mouse_button = mouse_button

    def __init__(self, images, center_x, center_y, on_press=None, on_hover=None, colorkeys=None, scale=1,
                 mouse_button=0):
        """
        The constructor of the button class
        :param images: Three images of the button in the neutral, hovered and clicked state. images[0] = neutral,
        images[1] = hovered, images[2] = clicked
        :param center_x: Center x of button on screen
        :param center_y: Center y of button on screen
        :param on_press: A function that executes when the button is pressed
        :param colorkey: The colorkey to be passed to the load_image function that is used to load the buttons images.
        This has to be the same on all three images
        :param scale: The scale of the buttons image and thus the button
        :param mouse_button: The mouse button that should be checked for clicks. 0, 1, 2
        """
        pg.sprite.Sprite.__init__(self)

        self.images, self.rect = loader.load_images(names=images, colorkeys=colorkeys, scale=scale)
        self.image = self.images[0]
        self.rect.center = center_x, center_y

        self.press_func = on_press if on_press is not None else lambda: 0
        self.hover_func = on_hover if on_hover is not None else lambda: 0
        self.mouse_button = mouse_button

    def update(self):
        self._check_input()

    def _check_input(self):
        if self._check_hover():
            self.image = self.images[1]
            self.hover_func()
            if self._check_click():
                self.image = self.images[2]
                self.press_func()
        else:
            self.image = self.images[0]

    def _check_hover(self):
        return self.rect.collidepoint(pg.mouse.get_pos())

    def _check_click(self):
        return pg.mouse.get_pressed()[self.mouse_button]


def draw_main_menu():
    all_sprites.update()
    screen.blit(background, background_rect)
    all_sprites.draw(screen)


def draw_game_scene():
    all_sprites.update()

    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    check_win_condition()


def draw_win_scene():
    screen.blit(background, background_rect)


def draw_game_over_scene():
    pass


def switch_state(new_state):
    global state, background, background_rect, state_function

    background, background_rect = loader.load_image('background.jpg')

    if new_state == 'game':
        state = GAME_SCREEN
        set_up_game_screen()

    elif new_state == 'win':
        state = WIN_SCREEN
        set_up_win_screen()

    elif new_state == 'gameover':
        state = GAME_SCREEN

    elif new_state == 'main':
        state = MAIN_MENU
        set_up_main_screen()

    state_function = state_functions[state]


def set_up_main_screen():
    # Font and text
    font = loader.load_font('space_invaders.ttf', 64)
    main_text = font.render('Alien Invasion', False, (255, 255, 255))
    text_pos = main_text.get_rect(centerx=size[0] / 2, y=10)
    background.blit(main_text, text_pos)

    # Initialize the buttons
    buttons = [Button(images=['play_button_neutral.png',
                              'play_button_hovered.png',
                              'play_button_clicked.png'],
                      center_x=size[0] / 2,
                      center_y=size[1] / 2,
                      on_press=lambda: switch_state('game'),
                      on_hover=None,
                      colorkeys=[-1, -1, -1],
                      scale=10,
                      mouse_button=0)]

    return buttons


def set_up_game_screen():
    # Clear main menu sprites
    kill_all_sprites()

    # Generate the alien sprites
    alien_grid = (10, 3)
    grid_width = 750
    grid_height = 250

    x_offset = grid_width // alien_grid[0]
    y_offset = grid_height // alien_grid[1]

    for col in range(alien_grid[0]):
        for row in range(alien_grid[1]):
            all_sprites.add(Alien(images=['alien_1_1.png', 'alien_1_2.png'],
                                  position=(x_offset * col, y_offset * row),
                                  animation_time=0.5,
                                  shot_time=5))

    # Generate the gun sprite
    all_sprites.add(Gun())


def set_up_win_screen():
    # Clear game sprites
    kill_all_sprites()

    # Font and win text
    font = loader.load_font('space_invaders.ttf', 128)
    win_text = font.render('You win!', False, (255, 255, 255))
    text_pos = win_text.get_rect(centerx=size[0] / 2, y=10)
    background.blit(win_text, text_pos)

    font = loader.load_font('space_invaders.ttf', 64)
    win_text = font.render(f'{time.time() - start_time:.2f}', False, (255, 255, 255))
    text_pos = win_text.get_rect(centerx=size[0] / 2, y=200)
    background.blit(win_text, text_pos)


def kill_all_sprites():
    for sprite in all_sprites.sprites():
        sprite.kill()
    all_sprites.empty()


if __name__ == "__main__":
    # Initialize the screen and pygame
    pg.init()
    size = (1280, 720)
    screen = pg.display.set_mode(size)
    pg.display.set_caption('Alien Invasion')

    # Start time
    start_time = time.time()

    # Set the background
    background, background_rect = loader.load_image('background.jpg')

    # Sprite group for all sprites
    all_sprites = pg.sprite.RenderPlain()

    # Sprite group for main screen items
    all_sprites.add(set_up_main_screen())

    # Sprite groups for shots
    gun_shots = pg.sprite.Group()
    enemy_shots = pg.sprite.Group()

    # Enemy count
    enemies = pg.sprite.Group()

    # Gun single group
    gun = pg.sprite.GroupSingle()

    # Limit framerate
    clock = pg.time.Clock()

    # Delta time for frame rate independent physics
    dt = 0

    # Direction for all aliens
    alien_direction = 1

    # Game states
    MAIN_MENU = 0
    GAME_SCREEN = 1
    WIN_SCREEN = 2
    GAME_OVER_SCREEN = 3

    # State functions
    state_functions = {
        MAIN_MENU: draw_main_menu,
        GAME_SCREEN: draw_game_scene,
        WIN_SCREEN: draw_win_scene,
        GAME_OVER_SCREEN: draw_game_over_scene
    }
    state = MAIN_MENU

    state_function = state_functions.get(state)

    # handle joystick input
    joysticks = {}
    joy_stick_id = 0

    while True:
        dt = clock.tick(60) / 1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            # handle hot plugging of joysticks
            if event.type == pg.JOYDEVICEADDED:
                joy_stick_id = pg.joystick.Joystick(event.device_index)
                joysticks[joy_stick_id.get_instance_id()] = joy_stick_id
                print(f"Joystick {joy_stick_id.get_instance_id()} connected")
                print(f"joysticks: {joysticks}")

            if event.type == pg.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")
                print(f"{joysticks}")

        state_function()

        pg.display.flip()
