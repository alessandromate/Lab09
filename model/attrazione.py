from dataclasses import dataclass, field

@dataclass()
class Attrazione:
    id: str
    nome: str
    valore_culturale: int

    # set in cui aggiungo tutti gli ogg tour associati
    tour: set = field(default_factory=set)

    def __eq__(self, other):
        return isinstance(other, Attrazione) and self.id == other.id

    def __str__(self):
        return f"{self.nome} ({self.valore_culturale})"

    def __repr__(self):
        return f"{self.nome} ({self.valore_culturale})"

    def __hash__(self):
        return hash(self.id)
