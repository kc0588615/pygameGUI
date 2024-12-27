import pygame
import sys
import os

# Add root project directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from enum import Enum, auto
from pygame import Vector2

from common.file_helpers import get_sounds_directory, get_cards_directory
from common.assets.fonts import M5X7
from common.managers.managers import font_manager, audio_manager
from common.match3.frontend_puzzle import FrontendPuzzle
from common.cards import Card, CardController, AnimatedBackground

SCREEN_WIDTH = int(600)  
SCREEN_HEIGHT = int(270)

class GameState(Enum):
    MATCH3 = auto()
    CARDS = auto()

def game_loop() -> None:
    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        flags=pygame.RESIZABLE | pygame.SCALED,
    )
    game_clock = pygame.time.Clock()
    font_manager.load_font("main_font", M5X7, 16)

    # Load card sounds using correct path
    audio_manager.load_sound(
        "card_sound_4",
        os.path.join(get_sounds_directory(), "card_sounds", "card_sound_4.wav"),
    )
    audio_manager.load_sound(
        "card_sound_5",
        os.path.join(get_sounds_directory(), "card_sounds", "card_sound_5.wav"),
    )
    audio_manager.set_sound_volume("card_sound_4", 0.5)
    audio_manager.set_sound_volume("card_sound_5", 0.5)

    # Load card background
    card_background = pygame.image.load(
        os.path.join(get_cards_directory(), "card_1.png")
    )

    # Game state
    current_state = GameState.MATCH3
    
    # Initialize match-3
    frontend_grid = FrontendPuzzle(
        position=pygame.Vector2(15, 15),
        grid_width=7,
        grid_height=8,
        initial_state="full",
    )
    
    # Then in the game_loop function where you create the animated background:
    # Initialize cards using the common package implementations
    
    animated_background = AnimatedBackground((60, 90))
    card_controller = CardController(screen)
    card = Card(
        position=pygame.Vector2(400, 50),
        card_size=pygame.Vector2(60, 90),
        background_surface=card_background
    )
    card_controller.add_card(card)

    # Event handlers
    event_handlers = {
        GameState.MATCH3: [frontend_grid.handle_event],
        GameState.CARDS: [card_controller.process_event]
    }

    running = True
    while running:
        screen.fill("black")
        delta_ms = game_clock.tick(144)
        delta = delta_ms / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_state == GameState.MATCH3:
                        frontend_grid.toggle_frontend_puzzle_state()
                elif event.key == pygame.K_TAB:
                    # Toggle between games
                    current_state = (
                        GameState.CARDS if current_state == GameState.MATCH3 
                        else GameState.MATCH3
                    )
                    continue

            # Handle current state events
            for handler in event_handlers[current_state]:
                if handler(event):
                    break

        # Update and render current state
        if current_state == GameState.MATCH3:
            frontend_grid.process(delta)
            frontend_grid.render(screen)
        else:  # CARDS state
            card_controller.render(screen, delta)

        pygame.display.flip()

        if not running:
            break

    pygame.quit()

if __name__ == "__main__":
    game_loop()