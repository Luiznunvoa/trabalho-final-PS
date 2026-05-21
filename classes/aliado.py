from .carta import Carta
from .tribo import Tribo
from .reino import Reino

class Aliado(Carta):
    def __init__(self, tribo: Tribo, reino: Reino):
        super().__init__(nome=f"{tribo.nome}/{reino.nome_curto}")
        self.tribo = tribo
        self.reino = reino

    def criarCarta(self) -> "Aliado":
        return Aliado(self.tribo, self.reino)

    @property
    def is_dragon(self): return False
    @property
    def region_idx(self): return self.reino.idx
    @property
    def region_color(self): return self.reino.cor
    @property
    def race_color(self): return self.tribo.cor
    @property
    def race(self): return self.tribo.nome