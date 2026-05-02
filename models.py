from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional

class Carta(ABC):
    @property
    @abstractmethod
    def nome(self) -> str:
        pass
    
    @property
    @abstractmethod
    def imagem(self) -> str:
        pass

class Tribo:
    def __init__(self, nome: str, descricao: str, poder: str):
        self.nome = nome
        self.descricao = descricao
        self._poder = poder
    
    def ativar_poder(self, jogador: 'Jogador') -> None:
        print(f"[{jogador.nome}] Ativou poder da tribo {self.nome}: {self._poder}")

class Era(Enum):
    PROLOGO = 1
    JORNADA = 2
    EPILOGO = 3

class Token:
    def __init__(self, valor: int, era: Era):
        self.valor = valor
        self.era = era

class Reino:
    def __init__(self, nome: str, cor: tuple):
        self.nome = nome
        self.cor = cor
        self.glorias: List[Token] = []
        self.marcadores = {}  # {jogador.id: int}
        
    def pegar_gloria(self, era: Era) -> Optional[Token]:
        for token in self.glorias:
            if token.era == era:
                return token
        return None

class Influencia:
    def __init__(self, jogador: 'Jogador', reino: Reino):
        self.marcadores: int = 0
        self.jogador = jogador
        self.reino = reino
        
    def calc_marcadores(self) -> None:
        pass

class Aliado(Carta):
    def __init__(self, nome: str, imagem: str, tribo: Tribo, reino: str = ""):
        self._nome = nome
        self._imagem = imagem
        self.tribo = tribo
        self.reino = reino

    @property
    def nome(self) -> str:
        return f"{self._nome} ({self.reino})"
    
    @property
    def imagem(self) -> str:
        return self._imagem

class Dragao(Carta):
    def __init__(self, nome: str, imagem: str, efeito: str):
        self._nome = nome
        self._imagem = imagem
        self.efeito = efeito
        
    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def imagem(self) -> str:
        return self._imagem

class Bando:
    def __init__(self, tribo: Optional[Tribo] = None):
        self.tamanho_original: int = 0
        self.tribo = tribo
        self.tropas: List[Aliado] = []
        
    def _validar_bando(self, cartas: List[Carta]) -> None:
        pass
        
    def tamanho_atual(self) -> int:
        return len(self.tropas)
        
    def ativar_poder(self) -> None:
        if self.tribo:
            pass

class Tabuleiro:
    def __init__(self):
        self.cartasAbertas: List[Aliado] = []
        self.baralho: List[Carta] = []
        self.dragoes: List[Dragao] = []
        
    def _embaralhar(self) -> None:
        import random
        random.shuffle(self.baralho)
        
    def _receber_carta(self, carta: Carta) -> None:
        self.baralho.append(carta)
        
    def compra_carta(self) -> Optional[Carta]:
        if self.baralho:
            return self.baralho.pop()
        return None

class Jogador:
    def __init__(self, id: int, nome: str):
        self.id = id
        self.nome = nome
        self.cor: str = ""
        self.glorias: int = 0
        self.marcadores: int = 0
        self.bandos: List[Bando] = []
        self.mao: List[Carta] = []
        self.tribo_selecionada: Optional[Tribo] = None  # Vincula a raça escolhida na setup
        
    def _criar_bando(self) -> None:
        pass
        
    def _validar_mao(self) -> None:
        pass
        
    def calc_gloria(self) -> None:
        pass
        
    def escolher_cor(self) -> None:
        pass
        
    def selecionar_bando(self) -> Optional[Bando]:
        return None
        
    def pegar_carta(self, carta: Carta) -> None:
        self.mao.append(carta)
        
    def retornar_cartas(self) -> List[Carta]:
        return self.mao

class Jogo:
    def __init__(self):
        self._id_jogador_atual: int = 0
        self.tabuleiro = Tabuleiro()
        self.jogadores: List[Jogador] = []
        self.eraAtual: Era = Era.PROLOGO
        
        # Criação dos Reinos com 3 tokens aleatórios baseados nas regras gerais (valores de 0 a 10 por região/era)
        import random
        cores_reinos = {
            "Floresta": (34, 139, 34),
            "Montanha": (105, 105, 105),
            "Deserto": (210, 180, 140),
            "Pântano": (85, 107, 47),
            "Planícies": (154, 205, 50),
            "Mar": (70, 130, 180)
        }
        self.reinos: List[Reino] = []
        for nome, cor in cores_reinos.items():
            r = Reino(nome, cor)
            tokens_valores = sorted([random.randint(0, 4), random.randint(2, 6), random.randint(4, 10)])
            r.glorias = [
                Token(tokens_valores[0], Era.PROLOGO),
                Token(tokens_valores[1], Era.JORNADA),
                Token(tokens_valores[2], Era.EPILOGO)
            ]
            self.reinos.append(r)
        
    def passar_era(self) -> None:
        self._computar_gloria_da_era()
        if self.eraAtual == Era.PROLOGO:
            self.eraAtual = Era.JORNADA
        elif self.eraAtual == Era.JORNADA:
            self.eraAtual = Era.EPILOGO
        else:
            print("FIM DO JOGO!")
            
    def _computar_gloria_da_era(self) -> None:
        for r in self.reinos:
            token = r.pegar_gloria(self.eraAtual)
            if not token or not r.marcadores:
                continue
            
            # Encontrar o jogador com mais marcadores (controle)
            max_marcadores = max(r.marcadores.values())
            if max_marcadores == 0:
                continue
                
            empatados = [jid for jid, mq in r.marcadores.items() if mq == max_marcadores]
            # Em caso de empate, todos ganham a glória
            for jid in empatados:
                jogador = self.get_jogador_by_id(jid)
                if jogador:
                    jogador.glorias += token.valor
                    print(f"[Glória] {jogador.nome} ganhou {token.valor} pontos no reino {r.nome} (Era: {self.eraAtual.name})!")

    def get_jogador_by_id(self, jid: int) -> Optional[Jogador]:
        for j in self.jogadores:
            if j.id == jid:
                return j
        return None
        
    def criar_jogador(self, id: int, nome: str) -> None:
        self.jogadores.append(Jogador(id, nome))
        
    def descartar_bando(self, bando: Bando) -> None:
        pass
        
    def iniciar_jogo(self, tribos_escolhidas: List[Tribo]) -> None:
        import json
        import os
        self.tabuleiro.baralho.clear()
        
        # Load from json
        try:
            with open(os.path.join("ethnos", "cartas.json"), encoding="utf-8") as f:
                dados_cartas = json.load(f)
        except Exception:
            dados_cartas = {}

        for tribo in tribos_escolhidas:
            info = dados_cartas.get(tribo.nome)
            if info:
                # Ethnos has around 12 per tribe, so create 2 of each of the 6 kinds
                for carta_info in info.get("cartas", []):
                    for _ in range(2): 
                        carta = Aliado(carta_info["nome"], "", tribo, carta_info["reino"])
                        self.tabuleiro._receber_carta(carta)
            else:
                # Fallback se nao houver no json
                for i in range(12):
                    carta = Aliado(f"Aliado {tribo.nome} {i+1}", "", tribo, "Aleatório")
                    self.tabuleiro._receber_carta(carta)
                    
        # Dragões
        for i in range(3):
            dragao = Dragao("Dragão", "", "O Fim da Era se aproxima.")
            self.tabuleiro._receber_carta(dragao)
            
        self.tabuleiro._embaralhar()
        
        # Dar 1 carta inicial pra cada
        for jogador in self.jogadores:
            c = self.tabuleiro.compra_carta()
            if c: self.dar_carta(c, jogador)
            
        self._id_jogador_atual = 0

    def proximo_turno(self) -> None:
        self._id_jogador_atual = (self._id_jogador_atual + 1) % len(self.jogadores)
        
    def jogador_atual(self) -> Jogador:
        return self.jogadores[self._id_jogador_atual]
        
    def pegar_vencedor(self) -> Jogador:
        pass
        
    def fazer_ataque(self, bando: Bando, reino: Reino) -> None:
        pass
        
    def dar_carta(self, carta: Carta, jogador: Jogador) -> None:
        jogador.pegar_carta(carta)
        
    def voltar_carta_pro_tabuleiro(self) -> None:
        pass