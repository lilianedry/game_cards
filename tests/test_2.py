from game.logic import GameLogic

def test_first_choice_only_counts():
    logic = GameLogic(cards=[
        {"right": [["ODS1", 5]], "left": [["ODS1", -5]]}
    ])

    logic.choose_right()   
    

    before = logic.ods["ODS1"]
    if logic.current_index == 0:
        logic.choose_left()

    after = logic.ods["ODS1"]

    assert before == after, "O segundo clique não deve ser considerado"
