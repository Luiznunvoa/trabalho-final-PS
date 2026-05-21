from __future__ import annotations
from typing import Optional
from .era import Era
from .jogador import Jogador
from .tabuleiro import Tabuleiro
from .bando import Bando
from .reino import Reino, REINOS
from .dragao import Dragao
from .carta import Carta
from .influencia import Influencia
from .tribo import TRIBOS
from .constantes import ALL_TRIBES, BAND_BONUS, NUM_DRAGONS, REGION_SCORES

class Jogo:
    _instancia: Optional["Jogo"] = None

    def __init__(self):
        self._id_jogador_atual = 0
        self.tabuleiro = Tabuleiro()
        self.eraAtual = Era.PROLOGO
        self.jogadores: list[Jogador] = []
        self.influencias: list[Influencia] = []

    @classmethod
    def getInstancia(cls) -> "Jogo":
        if cls._instancia is None:
            cls._instancia = Jogo()
        return cls._instancia

    @property
    def id_jogador_atual(self):
        return self._id_jogador_atual

    @id_jogador_atual.setter
    def id_jogador_atual(self, v):
        self._id_jogador_atual = v

    @property
    def jogador_atual(self) -> Jogador:
        return self.jogadores[self._id_jogador_atual]

    def criar_jogador(self) -> Jogador:
        j = Jogador(len(self.jogadores))
        self.jogadores.append(j)
        return j

    def iniciar_jogo(self):
        self.eraAtual = Era.PROLOGO
        for j in self.jogadores:
            j.reset_full()
        self._iniciar_era()

    def _iniciar_era(self):
        tribos = [TRIBOS[n] for n in ALL_TRIBES]
        self.tabuleiro.montar_baralho(tribos)
        for j in self.jogadores:
            j.reset_for_age()
        for j in self.jogadores:
            self.dar_carta(self.tabuleiro.compra_carta(), j)
        self._id_jogador_atual = 0

    def pasar_era(self):
        self._pontuar_reinos()
        if self.eraAtual == Era.PROLOGO:
            self.eraAtual = Era.JORNADA
            self._iniciar_era()
        elif self.eraAtual == Era.JORNADA:
            self.eraAtual = Era.EPILOGO
            self._iniciar_era()

    def _pontuar_reinos(self):
        for r in range(6):
            ranking = sorted(
                [(j.controle[r], j.id) for j in self.jogadores if j.controle[r] > 0],
                reverse=True
            )
            scores = REGION_SCORES[r]
            for rank, (_, jid) in enumerate(ranking):
                if rank < len(scores):
                    self.jogadores[jid].glorias += scores[rank]

    def fazer_ataque(self, bando: Bando, reino: Reino):
        jogador = bando.jogador
        jogador.controle[reino.idx] += 1
        jogador.glorias += BAND_BONUS.get(bando.tamanho_original, 15)
        jogador._bandos.append(bando)
        contexto = {
            "tabuleiro": self.self.tabuleiro if hasattr(self, 'self') else self.tabuleiro,  # Ajustado conforme imagem
            "lider": bando.lider,
            "cartas": bando.cartas,
            "influencias_extra": [],
        }
        contexto["tabuleiro"] = self.tabuleiro
        
        bando.invocarHabilidade(contexto)
        for (j, rn) in contexto.get("influencias_extra", []):
            j.controle[rn.idx] += 1

    def dar_carta(self, carta: Optional[Carta], jogador: Jogador) -> bool:
        if carta is None:
            return False
        if isinstance(carta, Dragao):
            total = self.tabuleiro.revelar_dragao()
            if total >= NUM_DRAGONS:
                return False
            return self.dar_carta(self.tabuleiro.compra_carta(), jogador)
        jogador.pegar_carta(carta)
        return True

    def pegar_vencedor(self) -> Optional[Jogador]:
        if not self.jogadores:
            return None
        return max(self.jogadores, key=lambda j: j.glorias)

    def proximo_turno(self):
        self._id_jogador_atual = (self._id_jogador_atual + 1) % len(self.jogadores)