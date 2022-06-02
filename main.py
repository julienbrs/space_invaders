# pylint: disable=no-member
""""
Space invaders
"""""
import os
import pygame
pygame.font.init()

#TOdo: transparent color for the menu


FPS = 120

VELOCITY_PLAYER             = 7
MAX_LASER_PLAYER            = 15
VELOCITY_LASER_PLAYER       = 9
LASER_SIZE = LASER_WIDTH, LASER_HEIGHT = 18,6
pygame.display.set_caption("Space Invaders")

WHITE   = (255, 255, 255)
GREY    = (125, 125, 125)
LIGHT_GREY = (175, 175, 175)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

FONT_MENU_WELCOME = pygame.font.SysFont("comicsans", 120)
FONT_MENU_START = pygame.font.SysFont("comicsans", 55)

MAIN_WIN_SIZE = WIDTH, HEIGHT = 1200, 800
MAIN_WIN = pygame.display.set_mode(MAIN_WIN_SIZE)

LIST_DIFFICULTY = ["Easy", "Medium", "Hard"]
DIFFICULTY_NUMBER = 0
text_menu_welcome       = FONT_MENU_WELCOME.render("Space Invaders Retro", 1, LIGHT_GREY)
text_menu_start_game    = FONT_MENU_START.render("Start the game", 1, GREY)
text_menu_difficulty    = FONT_MENU_START.render(
                            f"Difficulty: {LIST_DIFFICULTY[DIFFICULTY_NUMBER]}", 1, GREY)
text_menu_leaderboard   = FONT_MENU_START.render("Leaderboard", 1, GREY)


IMG_MENU_BACKGROUND = pygame.image.load(
    os.path.join('Assets', 'parallax-space-backgound.png'))
IMG_GAME_BACKGROUND = pygame.image.load(
    os.path.join('Assets', 'background-black.png'))
IMG_SPACESHIP_DEFAULT = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))


RED_LASER = pygame.image.load(os.path.join("Assets", "pixel_laser_red.png"))

IMG_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    IMG_SPACESHIP_DEFAULT, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

def move_lasers(shooter, velocity):
    for laser in shooter.lasers:
        if not laser.off_screen(HEIGHT):
            shooter.lasers.remove(laser)
        else:
            laser.move(velocity)

class LinkedText():
    "Class to link text for a menu"

    def __init__(self, x, y, selected, next_text, prev_text):
        self.x = x
        self.y = y
        self.selected = selected
        self.next_text = next_text
        self.prev_text = prev_text


    def draw(self, surface, text):
        "draw the text with line or not if selected"
        if self == MENU_SELECTED:
            new_size = (text.get_width() *1.8, text.get_height()*1.8)
            new_text = pygame.transform.scale(text, new_size)
            surface.blit(new_text, (self.x - new_text.get_width()/2,
                     self.y - new_text.get_height()/2))

            start_pos   = (self.x - new_text.get_width()/2, self.y + new_text.get_height() /2 )
            end_pos     = (self.x + new_text.get_width()/2, self.y + new_text.get_height() /2 )
            pygame.draw.line(MAIN_WIN, GREY,
                             start_pos, end_pos, width = int(text.get_height() * 0.08))

        else:
            surface.blit(text, (self.x - text.get_width()/2,
                     self.y - text.get_height()/2))

def collide(item1, item2):
    "check if there is a collision"
    offset_x = item1.x - item2.x
    offset_y = item1.x - item2.y
    return item1.mask.overlap(item2.mask, (offset_x, offset_y)) is not None

class Laser():
    "Class of lasers, x and y: where it starts"
    def __init__(self, x, y, direction, img):
        self.x          = x
        self.y          = y
        self.direction  = direction
        self.img        = img
        self.mask       = pygame.mask.from_surface(self.img)

    def draw(self):
        "draw item"
        MAIN_WIN.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        "move the item, velocity can also change the direction + or -"
        self.y += velocity

    def off_screen(self, height):
        "check if item isn't off the screen"
        return self.y >= 0 and self.y <= height

    def collision(self, obj):
        "check a collision"
        return collide(self, obj)


class Player():
    "class of the player"

    def __init__(self, x, y, width, height, img):
        self.x          = x
        self.y          = y
        self.width      = width
        self.height     = height
        self.img        = img
        self.laser_img  = None
        self.lasers     = []

    def draw(self):
        "draw item"
        MAIN_WIN.blit(self.img, (self. x, self.y))
        for laser in self.lasers:
            laser.draw()

    def shoot(self):
        "shoot"
        laser = Laser(self.x - self.width/2, self.y - self.height, None, RED_LASER)
        self.lasers.append(laser)

    def collision(self, other):
        "collision"
        return collide(self, other)

    def move(self, keys):
        "move the player"
        if keys[pygame.K_LEFT] and player.x > 0:    #Left
            player.x -= VELOCITY_PLAYER
        if keys[pygame.K_RIGHT] and player.x < WIDTH:    #Right
            player.x += VELOCITY_PLAYER
        if keys[pygame.K_UP] and player.y > 0:    #Top
            player.y -= VELOCITY_PLAYER
        if keys[pygame.K_DOWN] and player.y < HEIGHT:    #Left
            player.y += VELOCITY_PLAYER
        move_lasers(self, -VELOCITY_LASER_PLAYER)





start_game  = LinkedText(WIDTH /2, HEIGHT /2, True, None, None)
difficulty  = LinkedText(WIDTH /2, HEIGHT /1.5, False, None, start_game)
leaderboard = LinkedText(WIDTH /2, HEIGHT / 1.3, False, start_game, difficulty)
difficulty.next_text = leaderboard
start_game.next_text, start_game.prev_text = difficulty, leaderboard
MENU_SELECTED = start_game


player = Player((WIDTH- SPACESHIP_WIDTH)/2, HEIGHT * 0.75,
                 SPACESHIP_WIDTH, SPACESHIP_HEIGHT, IMG_SPACESHIP)

def draw_menu(text_blink, text_scroll):
    "draw the start menu, text_scroll can be up, down or none"

    MAIN_WIN.blit(pygame.transform.scale(IMG_MENU_BACKGROUND, MAIN_WIN_SIZE), (0,0))

    text_blink = (text_blink + 1) % 100
    if text_blink <= 50 :
        MAIN_WIN.blit(text_menu_welcome,((WIDTH - text_menu_welcome.get_width())/2,
                    (HEIGHT/3 - text_menu_welcome.get_height())/2))

    start_game.draw(MAIN_WIN, text_menu_start_game)
    difficulty.draw(MAIN_WIN, text_menu_difficulty)
    leaderboard.draw(MAIN_WIN, text_menu_leaderboard)
    global MENU_SELECTED
    if text_scroll == "DOWN":
        MENU_SELECTED = MENU_SELECTED.next_text
        text_scroll = None

    elif text_scroll == "UP":
        MENU_SELECTED = MENU_SELECTED.prev_text
        text_scroll = None

    pygame.display.update()
    return text_blink, text_scroll

def draw_game():
    "Draw the game"
    MAIN_WIN.blit(pygame.transform.scale(IMG_GAME_BACKGROUND, MAIN_WIN_SIZE), (0,0))

    player.draw()
    pygame.display.update()

def main():
    "main loop"
    clock = pygame.time.Clock()
    text_blink = 0
    text_scroll = None
    global DIFFICULTY_NUMBER
    global text_menu_difficulty
    app_run  = True
    run_menu = True
    run_game = False

    while app_run:

        while run_menu:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_menu, app_run = False, False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        text_scroll = "UP"
                        text_blink, text_scroll = draw_menu(text_blink - 1, text_scroll)

                    if event.key == pygame.K_DOWN:
                        text_scroll = "DOWN"
                        text_blink, text_scroll = draw_menu(text_blink - 1, text_scroll)

                    if event.key == pygame.K_RIGHT and MENU_SELECTED == difficulty:
                        DIFFICULTY_NUMBER = (DIFFICULTY_NUMBER + 1 ) %3
                        text_menu_difficulty = FONT_MENU_START.render(
                                    f"Difficulty: {LIST_DIFFICULTY[DIFFICULTY_NUMBER]}", 1, GREY)

                    if event.key == pygame.K_LEFT and MENU_SELECTED == difficulty:
                        DIFFICULTY_NUMBER = (DIFFICULTY_NUMBER - 1 ) %3
                        text_menu_difficulty = FONT_MENU_START.render(
                                    f"Difficulty: {LIST_DIFFICULTY[DIFFICULTY_NUMBER]}", 1, GREY)



                    if event.key == pygame.K_RETURN and MENU_SELECTED == start_game:
                        run_menu = False
                        run_game = True
            text_blink, text_scroll = draw_menu(text_blink, text_scroll)

        while run_game:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game, app_run = False, False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and len(player.lasers) < MAX_LASER_PLAYER:
                        player.shoot()
            keys = pygame.key.get_pressed()
            player.move(keys)



            draw_game()

    pygame.quit()



if __name__ == "__main__":
    main()
