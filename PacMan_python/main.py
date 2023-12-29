import pygame
from game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    game_sound = pygame.mixer.Sound("PacMan Original.mp3")
    game_sound.play()

    pygame.display.set_caption("PACMAN")
    done = False
    clock = pygame.time.Clock()
    game = Game()
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(30)

    pygame.quit()
if __name__ == '__main__':
    main()
