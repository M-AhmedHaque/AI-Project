import pygame
import numpy as np
from constants import WIDTH, HEIGHT, CARD_WIDTH, CARD_HEIGHT, CARD_SPACING, COLOR_MAP, BUTTON_COLOR, BUTTON_HOVER_COLOR
from card import Card

class UnoGameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("UNO Game")
        self.font = pygame.font.SysFont('arial', 20, bold=True)
        self.message_font = pygame.font.SysFont('arial', 24, bold=True)
        self.draw_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 120, 120, 40)
        self.color_buttons = {
            'Red': pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 50, 50, 30),
            'Green': pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 50, 50, 30),
            'Blue': pygame.Rect(WIDTH // 2, HEIGHT // 2 + 50, 50, 30),
            'Yellow': pygame.Rect(WIDTH // 2 + 60, HEIGHT // 2 + 50, 50, 30)
        }
        self.hovered_card = None
        self.click_sound = self.create_click_sound()

    def create_click_sound(self):
        sample_rate = 44100
        freq = 440
        duration = 0.1
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = 0.5 * np.sin(2 * np.pi * freq * t)
        stereo = np.column_stack((wave, wave)).astype(np.float32)
        sound = pygame.sndarray.make_sound(stereo)
        return sound

    def render_card(self, card, x, y, hidden=False, hovered=False):
        color = COLOR_MAP['Black'] if card.color is None else COLOR_MAP[card.color]
        if hovered:
            pygame.draw.rect(self.screen, (50, 50, 50), (x + 5, y + 5, CARD_WIDTH, CARD_HEIGHT), border_radius=10)
        pygame.draw.rect(self.screen, color, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=10)
        if not hidden:
            text = self.font.render(str(card), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
            pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(4, 4))
            self.screen.blit(text, text_rect)

    def draw(self, game_logic, message, color_choice):
        # Draw gradient background
        for y in range(HEIGHT):
            color = (0, 100 - y // 10, 0)
            pygame.draw.line(self.screen, color, (0, y), (WIDTH, y))
        # Draw discard pile
        if game_logic.discard_pile:
            self.render_card(game_logic.discard_pile[-1], WIDTH // 2 - CARD_WIDTH // 2, HEIGHT // 2 - CARD_HEIGHT - 20)
        # Draw player hand (centered)
        hand_width = len(game_logic.player_hand) * (CARD_WIDTH + CARD_SPACING) - CARD_SPACING
        start_x = (WIDTH - hand_width) // 2
        self.hovered_card = None
        for i, card in enumerate(game_logic.player_hand):
            x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            y = HEIGHT - CARD_HEIGHT - 30
            mouse_pos = pygame.mouse.get_pos()
            rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            hovered = rect.collidepoint(mouse_pos) and card.can_play(game_logic.discard_pile[-1]) if game_logic.turn == 0 else False
            if hovered:
                self.hovered_card = (card, i)
            self.render_card(card, x, y, hovered=hovered)
        # Draw AI hand (hidden, centered)
        hand_width = len(game_logic.ai_hand) * (CARD_WIDTH + CARD_SPACING) - CARD_SPACING
        start_x = (WIDTH - hand_width) // 2
        for i in range(len(game_logic.ai_hand)):
            x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            self.render_card(Card('Red', '0'), x, 30, hidden=True)
        # Draw message
        text = self.message_font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, 50))
        pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(10, 5))
        self.screen.blit(text, text_rect)
        # Draw "Draw" button if no playable cards
        if game_logic.turn == 0 and not game_logic.has_playable_card():
            mouse_pos = pygame.mouse.get_pos()
            color = BUTTON_HOVER_COLOR if self.draw_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.screen, color, self.draw_button, border_radius=5)
            text = self.font.render("Draw", True, (255, 255, 255))
            text_rect = text.get_rect(center=self.draw_button.center)
            self.screen.blit(text, text_rect)
        # Draw color choice buttons
        if color_choice:
            for color, button in self.color_buttons.items():
                mouse_pos = pygame.mouse.get_pos()
                button_color = BUTTON_HOVER_COLOR if button.collidepoint(mouse_pos) else COLOR_MAP[color]
                pygame.draw.rect(self.screen, button_color, button, border_radius=5)
                text = self.font.render(color, True, (255, 255, 255))
                text_rect = text.get_rect(center=button.center)
                pygame.draw.rect(self.screen, (0, 0, 0), text_rect.inflate(4, 4))
                self.screen.blit(text, text_rect)
        pygame.display.flip()

    def get_hovered_card_index(self):
        return self.hovered_card[1] if self.hovered_card else None