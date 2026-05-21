from __future__ import annotations
from typing import Optional
from .constantes import PLAYER_NAMES, PLAYER_COLORS, GRAY
from .carta import Carta
from .tribo import Tribo
from .bando import Bando
from .aliado import Aliado

class Jogador:
    def __init__(self, id: int):
        self.id = id
        self.nome = PLAYER_NAMES[id]
        self.cor = PLAYER_COLORS[id]
        self.glorias = 0
        self.marcadores = 0
        self.tribo: Optional[Tribo] = None
        self.mao: list[Carta] = []
        self._bandos: list[Bando] = []
        self._cartas_guardadas: list[Carta] = []
        self.controle: list[int] = [0] * 6

    def pegar_carta(self, carta: Carta):
        self.mao.append(carta)

    def usarPoder(self, contexto: dict):
        if self.tribo:
            self.tribo.ativarHabilidade(self, contexto)

    @property
    def bandos(self):
        return self._bandos

    @property
    def race_color(self):
        return self.tribo.cor if self.tribo else GRAY

    @property
    def race_symbol(self):
        return self.tribo.simbolo if self.tribo else "?"

    def reset_full(self):
        self.glorias = 0
        self.controle = [0] * 6
        self.mao.clear()
        self._bandos.clear()
        self._cartas_guardadas.clear()

    def reset_for_age(self):
        self.mao = list(self._cartas_guardadas)
        self._cartas_guardadas.clear()
        self._bandos.clear()