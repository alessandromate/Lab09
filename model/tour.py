from dataclasses import dataclass, field

@dataclass()
class Tour:
    id: str
    nome: str
    durata_giorni: int
    costo: float
    id_regione: str

    # RELAZIONE (N:N)  #dunque ogni oggetto tour conterrà un set di ogg attrazioni
    attrazioni: set = field(default_factory=set)

    def __eq__(self, other):
        return isinstance(other, Tour) and self.id == other.id

    def __str__(self):
        return f"{self.nome} | Durata: {self.durata_giorni} giorni | Costo: €{round(self.costo, 2)}"

    def __repr__(self):
        return f"{self.nome} | Durata: {self.durata_giorni} giorni | Costo: €{round(self.costo, 2)}"

    def __hash__(self):
        return hash(self.id)
