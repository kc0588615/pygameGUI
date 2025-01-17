import pygame

class GameState:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
    
    def init(self):
        """Initialize state resources"""
        pass
        
    def cleanup(self):
        """Cleanup state resources"""
        pass
        
    def handle_event(self, event):
        """Handle input events"""
        pass
        
    def update(self, delta):
        """Update game logic"""
        pass
        
    def render(self):
        """Render the state"""
        pass 