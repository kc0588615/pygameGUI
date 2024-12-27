# common/cards/card_controller.py
import pygame
from .card import Card

class CardController:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.cards: list[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def render(self, surface: pygame.Surface, delta: float) -> None:
        for card in reversed(self.cards):  # Render in reverse order for proper layering
            card.render(surface, delta)

    def process_event(self, event: pygame.event.Event) -> bool:
        for i, card in enumerate(self.cards):
            if card.process_events(event):
                # Bring the clicked card to the front
                self.cards.insert(0, self.cards.pop(i))
                return True  # Event handled
        return False  # Event not handled by any card