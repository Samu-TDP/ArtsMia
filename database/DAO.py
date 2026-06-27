from database.DB_connect import DBConnect
from model.artobject import ArtObject
from dataclasses import dataclass


# Creiamo una mini-struttura dati per trasportare comodamente
# i dati dell'arco (Nodo A, Nodo B, Peso) dal Database al Model.
@dataclass
class Connessione:
    id_oggetto_1: int
    id_oggetto_2: int
    peso: int


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_objects():
        """Questa query estrae tutti i VERTICI del nostro futuro grafo."""
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM objects"
        cursor.execute(query)

        for row in cursor:
            result.append(ArtObject(**row))  # Creiamo gli oggetti col trucchetto del **row

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_connessioni():
        """Questa query estrae tutti gli ARCHI e i relativi PESI."""
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            return []

        cursor = conn.cursor(dictionary=True)

        # ==========================================
        # LA QUERY "TRUCCHETTO" PER GLI ARCHI
        # ==========================================
        # Vogliamo due oggetti (eo1 e eo2) che stanno nella stessa mostra.
        # Condizione 1: eo1.exhibition_id = eo2.exhibition_id
        # Condizione 2 (FONDAMENTALE): eo1.object_id > eo2.object_id
        # Perché il ">"? Per evitare di collegare l'oggetto con sé stesso (es. 1 con 1)
        # e per evitare di prendere l'arco due volte (es. A-B e B-A). Il grafo è NON ORIENTATO.

        query = """
            SELECT eo1.object_id as o1, eo2.object_id as o2, count(*) as peso
            FROM exhibition_objects eo1, exhibition_objects eo2
            WHERE eo1.exhibition_id = eo2.exhibition_id
            AND eo1.object_id > eo2.object_id
            GROUP BY eo1.object_id, eo2.object_id
        """
        cursor.execute(query)

        for row in cursor:
            # Salviamo il risultato nella nostra mini-dataclass
            result.append(Connessione(row["o1"], row["o2"], row["peso"]))

        cursor.close()
        conn.close()
        return result