import pygame
import pygame_gui
from common.game_states.base_state import GameState
from common.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class GUIState(GameState):
    def __init__(self, screen):
        super().__init__(screen)
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(self.manager.get_theme().get_colour('dark_bg'))
        
        # Create container for our grid
        self.container = pygame_gui.core.UIContainer(
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            manager=self.manager
        )
        
        self.create_card_grid()

    def create_card_grid(self):
        # Create a grid of buttons representing cards
        button_width = 60
        button_height = 90
        spacing = 20
        
        for row in range(3):
            for col in range(4):
                position = (
                    col * (button_width + spacing) + spacing,
                    row * (button_height + spacing) + spacing
                )
                
                pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect(position, (button_width, button_height)),
                    text=f'Card {row},{col}',
                    manager=self.manager,
                    container=self.container,
                    object_id=f'#card_{row}_{col}'
                )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # Handle button clicks here
            pass
            
        self.manager.process_events(event)

    def update(self):
        time_delta = self.clock.tick(60)/1000.0
        self.manager.update(time_delta)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.manager.draw_ui(self.screen) 