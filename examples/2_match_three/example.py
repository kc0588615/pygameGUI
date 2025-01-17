import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.assets.fonts import M5X7
from common.managers.managers import font_manager
from common.match3.frontend_puzzle import FrontendPuzzle
from common.file_helpers import get_sounds_directory
from common.managers.managers import audio_manager

SCREEN_WIDTH = int(240)
SCREEN_HEIGHT = int(270)


def game_loop() -> None:
    pygame.init()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        flags=pygame.RESIZABLE | pygame.SCALED,
    )

    game_clock = pygame.time.Clock()

    font_manager.load_font("main_font", M5X7, 16)

    frontend_grid = FrontendPuzzle(
        position=pygame.Vector2(15, 15),
        grid_width=7,
        grid_height=8,
        initial_state="full",
    )

    # Load required audio
    for i in range(3):
        audio_manager.load_sound(f"glass_clink_{i}", os.path.join(get_sounds_directory(), f"glass_clink_{i}.wav"))

    event_handling_functions = [
        frontend_grid.handle_event,
    ]

    running = True
    while True:

        screen.fill("black")

        delta_ms = game_clock.tick(144)
        delta = delta_ms / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            for event_handler in event_handling_functions:
                event_consumed = event_handler(event)
                if event_consumed:
                    break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    frontend_grid.toggle_frontend_puzzle_state()

        # Process everything
        frontend_grid.process(delta)

        # Render everything
        frontend_grid.render(screen)

        pygame.display.flip()

        if not running:
            break

    pygame.quit()


if __name__ == "__main__":
    game_loop()
