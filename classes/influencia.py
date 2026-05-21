from .era import Era
from .reino import Reino

class Influencia:
    def __init__(self, jogador, reino: Reino, era: Era):
        self.jogador = jogador
        self.reino = reino
        self.era = era
        self.marcadores = 0

    def calc_marcadores(self) -> int:
        return self.marcadores