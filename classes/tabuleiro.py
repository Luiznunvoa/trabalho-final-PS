import random
from typing import Optional
from .aliado import Aliado
from .carta import Carta
from .dragao import Dragao
from .tribo import Tribo
from .reino import REINOS
from .constantes import NUM_DRAGONS, ALL_TRIBES
from .tribo import TRIBOS


class Tabuleiro:
    def __init__(self):
        self.baralho: list[Carta] = []
        self.cartasAbertas: list[Aliado] = []
        self.dragoes: list[Dragao] = []
        
    def embaralhar(self):
        random.shuffle(self.baralho)
        
    def receber_carta(self, carta: Carta):
        if isinstance(carta, Aliado):
            self.cartasAbertas.append(carta)
            
    def revelar_dragao(self) -> int:
        self.dragoes.append(Dragao())
        return len(self.dragoes)
        
    def comprar_carta_aberta(self) -> Optional[Aliado]:
        if self.cartasAbertas:
            return self.cartasAbertas.pop(random.randint(0, len(self.cartasAbertas) - 1))
        return None
        
    def compra_carta(self) -> Optional[Carta]:
        return self.baralho.pop() if self.baralho else None
        
    def montar_baralho(self, tribos: list[Tribo]):
        self.baralho.clear()
        self.cartasAbertas.clear()
        self.dragoes.clear()
        for tribo in tribos:
            for reino in REINOS:
                self.baralho.append(Aliado(tribo, reino))
                self.baralho.append(Aliado(tribo, reino))
        for _ in range(NUM_DRAGONS):
            self.baralho.append(Dragao())
        self.embaralhar()
        
    def __len__(self):
        return len(self.baralho)