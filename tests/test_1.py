import pytest
from game.logic import GameLogic

def test_cards_have_valid_options():
    logic = GameLogic(cards=[
        {"text": "Teste", "right": [["ODS1", 1]], "left": [["ODS1", -1]]}
    ])

    for card in logic.cards:
        assert "right" in card
        assert "left" in card
        assert isinstance(card["right"], list)
        assert isinstance(card["left"], list)
