import pygame
import random
from animal import *
from inputmanager import InputManager
from ui import AnimalInspector
from worldGeneration.perlinNoise import *

class Test:
    def __init__(self, provided_screen=None):
        self.screenw, self.screenh = SCREEN_W, SCREEN_H
        
        # Allow external screen to be provided
        if provided_screen:
            self.screen = provided_screen
        else:
            self.screen = pygame.display.set_mode(
                (self.screenw, self.screenh),
                pygame.SCALED | pygame.RESIZABLE
            )
        
        self.backgroundStartingX = BACKGROUND_STARTING_X
        self.backgroundStartingY = BACKGROUND_STARTING_Y
        
        self.mapRowLen = MAP_ROW_LEN
        self.mapData = [[random.randint(0, 1) for c in range(self.mapRowLen)] for row in range(self.mapRowLen)]
        
        self.backgroundStartingX = 50
        self.backgroundStartingY = 50
        self.scale = 1
        
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.selectedAnimal = None
        self.inspector = AnimalInspector(None)
        
        # Initialize game state
        self.initialize_game()

    def initialize_game(self):
        """Setup initial game state"""
        self.animalList = []
        
        stag = Stag(0)
        stag2 = Stag(1)
        boar = Boar(2)
        wolf = Wolf(3)
            
        self.animalList.extend([stag, stag2, boar, wolf])
        self.input = InputManager()
        self.world = World()

    def handle_event(self, event):
        """Handle a single pygame event"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                clicked_animal = False
                
                # Check if click hit any animal
                for animal in self.animalList:
                    if animal.isBeingClicked(mouse_pos):
                        clicked_animal = True
                        self.selectedAnimal = animal
                        self.inspector = AnimalInspector(self.selectedAnimal)
                        break
                
                # If click didn't hit any animal, hide inspector
                if not clicked_animal and hasattr(self, 'inspector') and self.inspector:
                    self.inspector.isShowing = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right click
                self.inspector.isShowing = False
                
        # Also process input manager events
        self.input.handleEvents()

    def update(self, delta=None):
        """Update game state"""
        self.mousePos = pygame.mouse.get_pos()
        
        delta_ms = self.clock.tick(self.fps)
        
        for animal in self.animalList:
            animal.update(
                self.screen, 
                backgroundStartingX=self.backgroundStartingX,
                backgroundStartingY=self.backgroundStartingY,
                mousePos=self.mousePos
            )

    def render(self):
        """Render current game state"""
        self.screen.fill((0, 0, 0))  # Clear screen
        self.world.draw(self.screen)
        
        for animal in self.animalList:
            animal.update(
                self.screen,
                backgroundStartingX=self.backgroundStartingX,
                backgroundStartingY=self.backgroundStartingY,
                mousePos=self.mousePos
            )
        
        self.inspector.update(self.screen)

    def run_standalone(self):
        """Run game in standalone mode (when not integrated)"""
        run = True
        
        while run:
            self.input.handleEvents()
            self.mousePos = pygame.mouse.get_pos()
            
            if self.input.isActionPressed("escape"):
                run = False

            delta_ms = self.clock.tick(self.fps)
            
            self.world.draw(self.screen)

            for animal in self.animalList:
                animal.update(
                    self.screen,
                    backgroundStartingX=self.backgroundStartingX,
                    backgroundStartingY=self.backgroundStartingY,
                    mousePos=self.mousePos
                )
            
            if self.input.isMouseButtonPressed("left"):
                for animal in self.animalList:
                    if animal.isClicked:
                        self.selectedAnimal = animal
                        self.inspector = AnimalInspector(self.selectedAnimal)
            
            if self.input.isMouseButtonPressed("right"):
                self.inspector.isShowing = False

            self.inspector.update(self.screen)
            pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    test = Test()
    test.run_standalone()