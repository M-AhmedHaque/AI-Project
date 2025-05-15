class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color} {self.value}" if self.color else self.value

    def can_play(self, top_card):
        if self.color is None:  # Wild card
            return True
        return self.color == top_card.color or self.value == top_card.value or top_card.color is None