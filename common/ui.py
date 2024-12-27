# common/ui.py
import pygame
from common.managers.managers import font_manager

def draw_text(screen, text, position, font_name="main_font", color="white"):
    font = font_manager.get_font(font_name)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def draw_resource_display(screen, resource_manager, position):
    draw_text(screen, f"Gems: {resource_manager.gems}", position)

    #Draw unlocked card counts, for instance:
    card_counts = {}
    for card in resource_manager.unlocked_cards:
        card_counts[card] = card_counts.get(card,0) + 1

    y_offset = 0
    for card, count in card_counts.items():
        draw_text(screen, f"{card}: {count}", (position[0], position[1] + 20 + y_offset ))
        y_offset += 20