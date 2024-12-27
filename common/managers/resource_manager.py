# common/managers/resource_manager.py
class ResourceManager:
    def __init__(self):
        self.gems = 0
        self.unlocked_cards = []  # Store unlocked card data (e.g., filenames)

    def award_resources(self, explode_and_replace_phase):
        # Calculate gems earned based on match and combo level
        # (example logic – refine as needed)
        match_count = len(explode_and_replace_phase.matches)
        combo_multiplier = explode_and_replace_phase.combo_level + 1  #Example logic from your example.py code
        self.gems += match_count * combo_multiplier

    def check_card_unlocks(self):
        unlocked = []
        if self.gems >= 10 and "card_1.png" not in self.unlocked_cards: #Example reward, replace with actual implementation
            unlocked.append("card_1.png")
            self.unlocked_cards.append("card_1.png")
        elif self.gems >= 20 and "card_2.png" not in self.unlocked_cards:
            unlocked.append("card_2.png")
            self.unlocked_cards.append("card_2.png")
        # ... more unlock conditions ...
        return unlocked