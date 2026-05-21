from enum import Enum

class Era(Enum):
    PROLOGO = 1
    JORNADA = 2
    EPILOGO = 3

    def __str__(self):
        return self.name.capitalize()

    @property
    def numero(self) -> int:
        return self.value