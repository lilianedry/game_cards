import pytest
from game.logic import GameLogic

def test_accumulated_effects():
    cards = [
        {"right": [["ODS1", +3]], "left": []},
        {"right": [["ODS1", +2]], "left": []},
        {"right": [["ODS1", -4]], "left": []},
    ]

    logic = GameLogic(cards=cards)

    logic.choose_right()  
    logic.choose_right() 
    logic.choose_right()  

    
    assert logic.ods["ODS1"] == 6   
