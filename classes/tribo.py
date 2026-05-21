from __future__ import annotations
from typing import TYPE_CHECKING
from .constantes import TRIBE_DESC, TRIBE_COLORS, TRIBE_SYMBOLS, GRAY, ALL_TRIBES

if TYPE_CHECKING:
    from .jogador import Jogador
    from .dragao import Dragao


class Tribo:
    PODERES = {
        "Centauro": "compra_extra",
        "Halfling": "bonus_pontos",
        "Esqueleto": "guarda_cartas",
        "Elfo": "mantem_carta",
        "Gigante": "bonus_fixo",
        "Mago": "compra_topo",
        "Troll": "controle_extra",
        "Orc": "compra_mercado",
    }

    def __init__(self, nome: str):
        self.nome = nome
        self.descricao = TRIBE_DESC.get(nome, "")
        self._poder = self.PODERES.get(nome, "nenhum")

    def ativarHabilidade(self, jogador: "Jogador", contexto: dict) -> None:
        tabuleiro = contexto.get("tabuleiro")
        lider = contexto.get("lider")
        cartas = contexto.get("cartas", [])

        if self._poder == "compra_extra":
            if tabuleiro:
                c = tabuleiro.compra_carta()
                if c:
                    jogador.pegar_carta(c)
        elif self._poder == "bonus_pontos":
            jogador.glorias += len(cartas)
        elif self._poder == "guarda_cartas":
            for c in cartas:
                jogador._cartas_guardadas.append(c.criarCarta())
        elif self._poder == "mantem_carta":
            if cartas:
                jogador.pegar_carta(cartas[0].criarCarta())
        elif self._poder == "bonus_fixo":
            jogador.glorias += 3
        elif self._poder == "compra_topo":
            from .dragao import Dragao
            if tabuleiro and tabuleiro.baralho:
                top = tabuleiro.baralho[-1]
                if not isinstance(top, Dragao):
                    jogador.pegar_carta(tabuleiro.compra_carta())
        elif self._poder == "controle_extra":
            if lider and lider.reino:
                jogador.marcadores += 1
                contexto.get("influencias_extra", []).append((jogador, lider.reino))
        elif self._poder == "compra_mercado":
            if tabuleiro and tabuleiro.cartasAbertas:
                c = tabuleiro.comprar_carta_aberta()
                if c:
                    jogador.pegar_carta(c)

    @property
    def cor(self):
        return TRIBE_COLORS.get(self.nome, GRAY)

    @property
    def simbolo(self):
        return TRIBE_SYMBOLS.get(self.nome, "?")


TRIBOS = {nome: Tribo(nome) for nome in ALL_TRIBES}