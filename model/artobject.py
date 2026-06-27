from dataclasses import dataclass

@dataclass
class ArtObject:
    object_id: int
    classification: str
    continent: str
    country: str
    curator_approved: int
    dated: str
    department: str
    medium: str
    nationality: str
    object_name: str
    restricted: int
    rights_type: str
    role: str
    room: str
    style: str
    title: str

    # ==========================================
    # REGOLE D'ORO PER I GRAFI (NetworkX)
    # ==========================================

    # 1. Metodo __eq__ (Uguaglianza)
    # Diciamo a Python e NetworkX che due oggetti sono la stessa cosa
    # SE E SOLO SE hanno lo stesso ID.
    def __eq__(self, other):
        return self.object_id == other.object_id

    # 2. Metodo __hash__ (La Carta d'Identità)
    # Fondamentale per inserire gli oggetti come Nodi nel Grafo.
    # L'hash si basa ESCLUSIVAMENTE sulla chiave primaria (object_id).
    def __hash__(self):
        return hash(self.object_id)

    # 3. Metodo __str__ (Per la stampa grafica)
    def __str__(self):
        return f"{self.object_id} - {self.object_name}"