from abc import ABC, abstractmethod

class Carta(ABC):
    def __init__(self, nome: str, imagem: str = ""):
        self.nome = nome
        self.imagem = imagem

    @abstractmethod
    def criarCarta(self) -> "Carta":
        pass

    def __repr__(self):
        return f"[{self.nome}]"