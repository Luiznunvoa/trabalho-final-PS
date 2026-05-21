from .era import Era

class Token:
    def __init__(self, valor: int, era: Era):
        self.valor = valor
        self.era = era

    def __repr__(self):
        return f"Token({self.valor}, {self.era})"