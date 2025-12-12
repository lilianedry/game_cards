class GameLogic:
    def __init__(self, ods=None, cards=None, max_cartas=10):
        self.ods = ods or {"ODS1": 5, "ODS3": 5, "ODS4": 5, "ODS15": 5}
        self.cards = cards or []
        self.current_index = 0
        self.max_cartas = max_cartas

    def apply_effects(self, effects):
        for nome, delta in effects:
            if nome in self.ods:
                self.ods[nome] += delta
                self.ods[nome] = max(0, min(self.ods[nome], 10))

    def choose_right(self):
        card = self.cards[self.current_index]
        self.apply_effects(card["right"])
        self.current_index += 1

    def choose_left(self):
        card = self.cards[self.current_index]
        self.apply_effects(card["left"])
        self.current_index += 1

    def check_end(self):
        for nome, valor in self.ods.items():
            if valor <= 0:
                return True, False, nome
        if self.current_index >= self.max_cartas:
            return True, True, None
        return False, False, None
