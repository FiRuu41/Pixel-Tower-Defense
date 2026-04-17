import sys
import pygame
from game import Game

if __name__ == '__main__':
    if '--test' in sys.argv:
        import os
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
    game = Game()
    if '--test' in sys.argv:
        for _ in range(120):
            for event in pygame.event.get():
                pass
            game.update()
            game.draw()
        print('TEST_PASS')
        pygame.quit()
    else:
        game.run()
