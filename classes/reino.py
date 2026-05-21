from .constantes import REGION_NAMES, REGION_COLORS, REGION_SHORT, REGION_SCORES
from .era import Era
from .token import Token

class Reino:
    def __init__(self, idx: int):
        self.idx = idx
        self.nome = REGION_NAMES[idx]
        self.cor = REGION_COLORS[idx]
        self._scores = REGION_SCORES[idx]
        self.glorias = [Token(v, era) for era in Era for v in self._scores]

    def pegar_gloria(self, era: Era) -> list[Token]:
        return [t for t in self.glorias if t.era == era]

    @property
    def nome_curto(self) -> str:
        return REGION_SHORT[self.idx]

REINOS = [Reino(i) for i in range(6)]