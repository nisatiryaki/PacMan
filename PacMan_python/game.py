from enemies import *
from player import Player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 102)

class Game(object):
    def __init__(self):
        self.lives = 2
        self.about = False
        self.game_over = True
        self.score = 0
        self.font = pygame.font.Font(None, 35)
        self.boyut = pygame.font.Font(None, 60)
        self.abut_font = pygame.font.Font(None, 35)
        self.menu = Menu(("Start", "About", "Exit"), font_color=WHITE, font_size=100)
        self.player = Player(32, 128, "player.png")
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        self.dots_group = pygame.sprite.Group()
        for i, row in enumerate(environment()):
            for j, item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Slime(288, 96, 0, 2))
        self.enemies.add(Slime(288, 320, 0, -2))
        self.enemies.add(Slime(544, 128, 0, 2))
        self.enemies.add(Slime(32, 224, 0, 2))
        self.enemies.add(Slime(160, 64, 2, 0))
        self.enemies.add(Slime(448, 64, -2, 0))
        self.enemies.add(Slime(640, 448, 2, 0))
        self.enemies.add(Slime(448, 320, 2, 0))
        for i, row in enumerate(environment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j * 32 + 12, i * 32 + 12, WHITE, 8, 8))

        self.pacman_sound = pygame.mixer.Sound("pacman_sound.mp3")
        self.game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")
        self.çarpma_sound = pygame.mixer.Sound("pacman_çarpma.mp3")

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            self.about = True
                        elif self.menu.state == 2:
                            return True

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()

                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False

        return False

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            if len(block_hit_list) > 0:
                self.pacman_sound.play()
                self.score += 10
            block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
            if len(block_hit_list) > 0:
                self.çarpma_sound.play()
                self.lives -= 1
                self.enemies = pygame.sprite.Group()
                self.enemies.add(Slime(288, 96, 0, 2))
                self.enemies.add(Slime(288, 320, 0, -2))
                self.enemies.add(Slime(544, 128, 0, 2))
                self.enemies.add(Slime(32, 224, 0, 2))
                self.enemies.add(Slime(160, 64, 2, 0))
                self.enemies.add(Slime(448, 64, -2, 0))
                self.enemies.add(Slime(640, 448, 2, 0))
                self.enemies.add(Slime(448, 320, 2, 0))
                self.player = Player(32, 128, "player.png")
                if self.lives == 0:
                    self.player.explosion = True
                    self.game_over_sound.play()
            self.game_over = self.player.game_over
            self.enemies.update(self.horizontal_blocks, self.vertical_blocks)

    def display_frame(self, screen):
        if self.game_over and not self.about:
            arkaplan = pygame.image.load("pacman.png")
            screen.blit(arkaplan, (0, 0))
        elif not self.game_over and not self.about:
            ARKAPLAN = pygame.image.load("boşekran.png")
            screen.blit(ARKAPLAN, (0, 0))
            can = pygame.image.load("küçükpacman.png.")
            screen.blit(can, (130, 38))
        elif self.about:
            arkaplan = pygame.image.load("hakkındaimg.png")
            screen.blit(arkaplan, (0, 0))

        if self.game_over:
            if self.about:
                hakkında1 = self.abut_font.render("It is a maze game with a PacMan and various ghosts.", True, YELLOW)
                screen.blit(hakkında1, [40, 200])
                hakkında2 = self.abut_font.render("The ghosts roam the maze, trying to kill Pac-Man.", True, YELLOW)
                screen.blit(hakkında2, [40, 250])
                hakkında3 = self.abut_font.render("He has two rights.These rights are reduced if he hits ghosts.", True, YELLOW)
                screen.blit(hakkında3, [40, 300])
                hakkında4 = self.abut_font.render("The score increases as you eat the dots.", True, YELLOW)
                screen.blit(hakkında4, [40, 350])
                hakkında5 = self.abut_font.render("The game is won when the dots run out.", True, YELLOW)
                screen.blit(hakkında5, [40, 400])
                hakkında6 = self.abut_font.render("You can exit all windows with the 'escape(esc)' key.", True, RED)
                screen.blit(hakkında6, [40, 450])
            else:
                self.menu.display_frame(screen)
        else:
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_environment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            text = self.font.render("Score: " + str(self.score), True, YELLOW)
            screen.blit(text, [120, 10])
            for i in range(self.lives):
                text = self.font.render(str(self.lives), True, YELLOW)
                screen.blit(text, [160, 40])
            if self.score == 1560:
                self.player.stop_move_right()
                self.player.stop_move_left()
                self.player.stop_move_up()
                self.player.stop_move_down()
                self.enemies = pygame.sprite.Group()
                self.enemies.add(Slime(800, 576, 0, 0))
                self.enemies.add(Slime(800, 576, 0, 0))
                self.enemies.add(Slime(800, 576, 0, 0))
                self.enemies.add(Slime(800, 576, 0, 0))
                self.enemies.add(Slime(800, 576, 0, 0))
                self.enemies.add(Slime(800, 576, 0, 0))
                self.enemies.add(Slime(800, 576, 0, 0))
                self.enemies.add(Slime(800, 576, 0, 0))
                kazanma = pygame.image.load("game won 1.png")
                screen.blit(kazanma, (0, 0))
                a1 = self.boyut.render(str(self.score), True, YELLOW)
                screen.blit(a1, [380, 385])

            if self.player.explosion == True:
                kaybetme = pygame.image.load("game.over.png")
                screen.blit(kaybetme, (0, 0))
                a2 = self.boyut.render(str(self.score), True, YELLOW)
                screen.blit(a2, [380, 385])

        pygame.display.flip()

    def display_message(self, screen, message, color=(255, 0, 0)):
        label = self.font.render(message, True, color)
        width = label.get_width()
        height = label.get_height()
        posX = (SCREEN_WIDTH / 2) - (width / 2)
        posY = (SCREEN_HEIGHT / 2) - (height / 2)
        screen.blit(label, (posX, posY))


class Menu(object):
    state = 0
    def __init__(self, items, font_color=(0, 0, 0), select_color=(255, 0, 0), ttf_font=None, font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item, True, self.font_color)

            width = label.get_width()
            height = label.get_height()

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 6) + (index * height)
            screen.blit(label, (posX, posY))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1
