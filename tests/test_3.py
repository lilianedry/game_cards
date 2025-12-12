import pytest
from game.logic import GameLogic

def test_indicator_updates_correctly():
    cards = [
        {
            "text": "Vacinação obrigatória?",
            "right": [["ODS3", 2], ["ODS1", -1]],
            "left":  [["ODS3", -2], ["ODS1", 1]]
        }
    ]

    logic = GameLogic(cards=cards)

    
    logic.choose_right()

    assert logic.ods["ODS3"] == 7   
    assert logic.ods["ODS1"] == 4   
