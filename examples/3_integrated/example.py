# examples/integrated/example.py
import os
import sys
import pygame
from enum import Enum, auto
from common.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from pygame import Vector2
from common.managers.managers import audio_manager
from common.game_states.gui_state import GUIState

class GameState(Enum):
    GUI = auto()
    MATCH3 = auto()
    HORAE = auto()

def main():
    pygame.init()
    print("Initialized pygame")
    
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        flags=pygame.RESIZABLE | pygame.SCALED,
    )
    print("Created display")
    
    # Add Horae's directory to Python path
    horae_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
    'project_horae', 'project-horae-main')
    if horae_path not in sys.path:
        sys.path.append(horae_path)
        print(f"Added Horae path: {horae_path}")
    
    # Initialize game states
    current_state = GameState.HORAE
    
    # Import game components
    from common.match3.frontend_puzzle import FrontendPuzzle
    from main import Test as HoraeGame  # Horae import after path is set

    # Initialize game instances
    gui_state = None
    match3_game = None

    # Save original directory and change to Horae's directory
    original_dir = os.getcwd()
    os.chdir(horae_path)  # Change to Horae's directory
    try:
        horae = HoraeGame(screen)  # Pass screen to Horae
        print("Successfully created HoraeGame instance")
    except Exception as e:
        print("\nError creating HoraeGame:")
        print(f"  {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return
    finally:
        os.chdir(original_dir)  # Restore original directory
        
    clock = pygame.time.Clock()
    running = True
    
    while running:
        delta = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB:
                    # Cycle through states
                    if current_state == GameState.GUI:
                        current_state = GameState.MATCH3
                        if match3_game is None:
                            match3_game = FrontendPuzzle(
                                position=Vector2(15, 15),
                                grid_width=7,
                                grid_height=8,
                                initial_state="full"
                            )
                    elif current_state == GameState.MATCH3:
                        current_state = GameState.HORAE
                    else:
                        current_state = GameState.GUI
                        if gui_state is None:
                            gui_state = GUIState(screen)
            
            # Handle events for current game
            if current_state == GameState.GUI and gui_state is not None:
                gui_state.handle_event(event)
            elif current_state == GameState.MATCH3 and match3_game is not None:
                match3_game.handle_event(event)
            elif current_state == GameState.HORAE:
                horae.handle_event(event)
        
        screen.fill((0, 0, 0))  # Clear screen
        
        try:
            # Update and render current game state
            if current_state == GameState.HORAE:
                horae.update()
                horae.render()
            elif current_state == GameState.MATCH3 and match3_game is not None:
                match3_game.process(delta)
                match3_game.render(screen)
            elif current_state == GameState.GUI and gui_state is not None:
                gui_state.update()
                gui_state.render()
                
        except Exception as e:
            print("\nError in game loop:")
            print(f"  {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            running = False
            
        pygame.display.flip()
            
    pygame.quit()

if __name__ == "__main__":
    main()