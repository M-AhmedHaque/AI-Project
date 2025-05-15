import random
from constants import COLORS, NUMBERS, ACTIONS, WILD
from card import Card

class UnoGameLogic:
    def __init__(self):
        self.deck = []
        self.discard_pile = []
        self.player_hand = []
        self.ai_hand = []
        self.current_color = None
        self.current_value = None
        self.direction = 1  # 1 for clockwise, -1 for reverse
        self.turn = 0  # 0 for player, 1 for AI
        self.create_deck()
        self.deal_cards()

    def create_deck(self):
        # Create number cards
        for color in COLORS:
            for number in NUMBERS:
                self.deck.append(Card(color, str(number)))
        # Create action cards
        for color in COLORS:
            for action in ACTIONS:
                for _ in range(2):
                    self.deck.append(Card(color, action))
        # Create wild cards
        for wild in WILD:
            for _ in range(4):
                self.deck.append(Card(None, wild))
        random.shuffle(self.deck)

    def deal_cards(self):
        for _ in range(7):
            self.player_hand.append(self.deck.pop())
            self.ai_hand.append(self.deck.pop())
        self.discard_pile.append(self.deck.pop())
        self.current_color = self.discard_pile[-1].color
        self.current_value = self.discard_pile[-1].value

    def ai_choose_card(self):
        playable_cards = [card for card in self.ai_hand if card.can_play(self.discard_pile[-1])]
        if not playable_cards:
            return None, None
        # Heuristic scoring
        best_score = -1
        best_card = None
        chosen_color = None
        color_counts = {color: sum(1 for card in self.ai_hand if card.color == color) for color in COLORS}
        max_color = max(color_counts, key=color_counts.get) if color_counts else 'Red'
        for card in playable_cards:
            score = 0
            if card.color == self.current_color:
                score += 5
            if card.color == max_color:
                score += 3
            if card.value in ACTIONS:
                score += 10
            if card.color is None:  # Wild card
                score += 8
                if card.value == 'WildDrawFour':
                    score += 2
            if score > best_score:
                best_score = score
                best_card = card
                chosen_color = max_color if card.color is None else None
        return best_card, chosen_color

    def draw_card(self, hand):
        if self.deck:
            hand.append(self.deck.pop())
        else:
            # Reshuffle discard pile except top card
            top = self.discard_pile.pop()
            self.deck = self.discard_pile
            self.discard_pile = [top]
            random.shuffle(self.deck)
            if self.deck:
                hand.append(self.deck.pop())

    def handle_action(self, card, hand):
        if card.value == 'Skip':
            self.turn = (self.turn + self.direction) % 2
        elif card.value == 'Reverse':
            self.direction *= -1
        elif card.value == 'DrawTwo':
            next_player = (self.turn + self.direction) % 2
            target_hand = self.ai_hand if next_player == 1 else self.player_hand
            for _ in range(2):
                self.draw_card(target_hand)
            self.turn = (self.turn + self.direction) % 2
        elif card.value == 'WildDrawFour':
            next_player = (self.turn + self.direction) % 2
            target_hand = self.ai_hand if next_player == 1 else self.player_hand
            for _ in range(4):
                self.draw_card(target_hand)
            self.turn = (self.turn + self.direction) % 2

    def has_playable_card(self):
        return any(card.can_play(self.discard_pile[-1]) for card in self.player_hand)