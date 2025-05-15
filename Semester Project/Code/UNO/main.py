import asyncio
import platform
import pygame
from game_logic import UnoGameLogic
from ui import UnoGameUI
from constants import WIDTH, CARD_WIDTH, CARD_HEIGHT, CARD_SPACING, FPS, HEIGHT

async def main():
    game_logic = UnoGameLogic()
    game_ui = UnoGameUI()
    clock = pygame.time.Clock()
    color_choice = False
    selected_card = None
    message = ""

    while True:
        game_ui.draw(game_logic, message, color_choice)
        if game_logic.turn == 0:  # Player's turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if color_choice:
                        for color, button in game_ui.color_buttons.items():
                            if button.collidepoint(pos):
                                game_ui.click_sound.play()
                                game_logic.player_hand.remove(selected_card)
                                game_logic.discard_pile.append(selected_card)
                                game_logic.current_color = color
                                game_logic.current_value = selected_card.value
                                game_logic.handle_action(selected_card, game_logic.player_hand)
                                game_logic.turn = 1
                                message = "AI's turn"
                                color_choice = False
                                break
                    else:
                        # Check for card selection
                        hand_width = len(game_logic.player_hand) * (CARD_WIDTH + CARD_SPACING) - CARD_SPACING
                        start_x = (WIDTH - hand_width) // 2
                        for i, card in enumerate(game_logic.player_hand):
                            x = start_x + i * (CARD_WIDTH + CARD_SPACING)
                            y = HEIGHT - CARD_HEIGHT - 30
                            rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                            if rect.collidepoint(pos) and card.can_play(game_logic.discard_pile[-1]):
                                selected_card = card
                                if card.color is None:
                                    color_choice = True
                                else:
                                    game_ui.click_sound.play()
                                    game_logic.player_hand.remove(card)
                                    game_logic.discard_pile.append(card)
                                    game_logic.current_color = card.color
                                    game_logic.current_value = card.value
                                    game_logic.handle_action(card, game_logic.player_hand)
                                    game_logic.turn = 1
                                    message = "AI's turn"
                        # Check for draw button
                        if not game_logic.has_playable_card() and game_ui.draw_button.collidepoint(pos):
                            game_ui.click_sound.play()
                            game_logic.draw_card(game_logic.player_hand)
                            game_logic.turn = 1
                            message = "AI's turn"
        else:  # AI's turn
            await asyncio.sleep(1)  # Simulate thinking
            card, chosen_color = game_logic.ai_choose_card()
            if card:
                game_ui.click_sound.play()
                game_logic.ai_hand.remove(card)
                game_logic.discard_pile.append(card)
                game_logic.current_value = card.value
                if chosen_color:
                    game_logic.current_color = chosen_color
                else:
                    game_logic.current_color = card.color
                game_logic.handle_action(card, game_logic.ai_hand)
                message = "Your turn"
            else:
                game_logic.draw_card(game_logic.ai_hand)
                message = "AI drew a card. Your turn"
            game_logic.turn = 0

        # Check for win
        if not game_logic.player_hand:
            message = "You win!"
            game_ui.draw(game_logic, message, color_choice)
            await asyncio.sleep(3)
            return
        elif not game_logic.ai_hand:
            message = "AI wins!"
            game_ui.draw(game_logic, message, color_choice)
            await asyncio.sleep(3)
            return

        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())