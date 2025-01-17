from animal import Animal
import pygame
 
class AnimalInspector:
    def __init__(self, animal : Animal):
        self.animal = animal
        # Reduce surface size from 300x200 to 150x100
        self.display = pygame.Surface((150, 100), pygame.SRCALPHA)
        # Reduce font size from 24 to 12
        self.font = pygame.font.SysFont("Arial", 12)
        self.isShowing = True
        
    def createDisplay(self):
        self.display.fill((0,0,0, 128))
        
        # Create text elements
        self.currentStateText = self.font.render(f"State: {self.animal.currentState}--{self.animal.currentMovementState}", True, (255, 255, 255))
        self.currentDirectionText = self.font.render(f"Direction: {self.animal.currentDirection}", True ,(255, 255, 255))
        self.hungerText = self.font.render(f"Hunger:" , True,(255, 255, 255))
        self.thirstText = self.font.render(f"Thirst:", True,(255, 255, 255))

        # Adjust bar sizes and positions
        self.hungerBar = Bar(40, 52, 100, self.animal.maxHunger, self.animal.hunger)
        self.thirstBar = Bar(40, 67, 100, self.animal.maxThirst, self.animal.thirst)

        # Adjust text positions
        self.display.blit(self.currentStateText, (0, 20))
        self.display.blit(self.currentDirectionText, (0, 35))
        self.display.blit(self.hungerText, (0, 50))
        self.display.blit(self.thirstText, (0, 65))

        self.hungerBar.update(self.display, self.animal.hunger, self.animal)
        self.thirstBar.update(self.display, self.animal.thirst, self.animal)

        
    def update(self, screen):
        if self.animal != None:
            self.createDisplay()
            self.draw(screen=screen)

    def draw(self, screen):
        if self.isShowing:
            screen.blit(self.display, (self.animal.rect.x, self.animal.rect.y))
    

class Bar:
    def __init__(self, left, top, width, maxStat, currentStat):
        self.left = left
        self.top = top
        self.width = width
        self.maxStat = maxStat
        self.currentStat = currentStat
        self.unitWidth = self.width / self.maxStat
        self.maxStatRect = pygame.Rect(self.left, self.top, self.width, 24)
        self.currentStatRect = pygame.Rect(self.left, self.top, self.unitWidth * self.currentStat, 24)
        

    def update(self, screen,  currentStat, animal):
        self.currentStat = currentStat
        self.currentStatRect = pygame.Rect(self.left, self.top, self.unitWidth * self.currentStat, 24)
        self.draw(screen, animal)
    
    def draw(self, screen, animal):
        pygame.draw.rect(screen, (255, 0, 0), self.maxStatRect)
        pygame.draw.rect(screen, (0, 255, 0), self.currentStatRect)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(int(self.left + self.unitWidth * animal.needThreshold), self.top, 1, 24))

