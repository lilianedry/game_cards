import pytest
from game.logic import GameLogic

def test_indicator_limits():
    cards = [
        {"right": [["ODS1", 200]], "left": []},   
        {"right": [["ODS1", -200]], "left": []},  
    ]

    logic = GameLogic(cards=cards)

    logic.choose_right()   
    assert logic.ods["ODS1"] == 10

    logic.choose_right()   
    assert logic.ods["ODS1"] == 0
