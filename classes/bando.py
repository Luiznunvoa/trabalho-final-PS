from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .aliado import Aliado
    from .jogador import Jogador

class Bando:
    def __init__(self, cartas: list["Aliado"], jogador: "Jogador"):
        self.tamanho_original = len(cartas)
        self._cartas = cartas
        self._lider: Optional["Aliado"] = None
        self.jogador = jogador

    def define_lider(self, carta: "Aliado"):
        self._lider = carta

    @property
    def lider(self):
        return self._lider

    @property
    def cartas(self):
        return self._cartas

    @property
    def is_valid(self) -> bool:
        if not self._cartas:
            return False
        if len(set(c.tribo.nome for c in self._cartas)) == 1:
            return True
        if len(set(c.reino.idx for c in self._cartas)) == 1:
            return True
        return False

    def invocarHabilidade(self, contexto: dict):
        if self.jogador.tribo:
            self.jogador.tribo.ativarHabilidade(self.jogador, contexto)