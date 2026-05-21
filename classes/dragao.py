from .carta import Carta
from .constantes import DGRAY

class Dragao(Carta):
    def __init__(self):
        super().__init__(nome="Dragao", imagem="dragao.png")
        self.efeito = "3 dragoes encerram a era"

    def criarCarta(self) -> "Dragao":
        return Dragao()

    @property
    def is_dragon(self): return True
    @property
    def region_idx(self): return -1
    @property
    def region_color(self): return DGRAY
    @property
    def race_color(self): return (200, 50, 50)
    @property
    def race(self): return "Dragao"