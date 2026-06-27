import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        # Il contenitore del nostro grafo (Non orientato e pesato)
        self._grafo = nx.Graph()

        # Dizionario di supporto (Id -> OggettoArtObject)
        # Fondamentale per trovare velocemente un nodo sapendo solo il suo ID
        self._idMap = {}

        # Lista di tutti gli oggetti (nodi)
        self._oggetti = []

    def crea_grafo(self):
        """Metodo meccanico per costruire il grafo."""

        # 1. Recupero i dati dal DAO
        self._oggetti = DAO.get_all_objects()

        # 2. Riempio la idMap (Mapping ID -> Oggetto)
        self._idMap = {obj.object_id: obj for obj in self._oggetti}

        # 3. AGGIUNGO I NODI
        # NetworkX accetta direttamente una lista di oggetti
        self._grafo.add_nodes_from(self._oggetti)

        # 4. AGGIUNGO GLI ARCHI (Recuperati con la query del Self-Join)
        connessioni = DAO.get_all_connessioni()

        for c in connessioni:
            # Recupero gli oggetti reali dalla idMap usando gli ID che vengono dal DAO
            u = self._idMap.get(c.id_oggetto_1)
            v = self._idMap.get(c.id_oggetto_2)

            # Controllo di sicurezza: aggiungo l'arco solo se entrambi i nodi esistono
            if u is not None and v is not None:
                self._grafo.add_edge(u, v, weight=c.peso)

    def get_connected_component(self, object_id):
        """Trova tutti i nodi raggiungibili partendo da un ID specifico."""

        # 1. Trasformo l'ID nell'oggetto reale presente nel grafo
        nodo_partenza = self._idMap.get(object_id)

        if nodo_partenza is None:
            return None  # L'ID inserito non esiste nel database

        # 2. Uso NetworkX per trovare la componente connessa
        # Restituisce un 'set' (insieme) di nodi
        comp_connessa = nx.node_connected_component(self._grafo, nodo_partenza)

        return comp_connessa

    # Metodi di utilità per il Controller
    def get_num_nodes(self):
        return self._grafo.number_of_nodes()

    def get_num_edges(self):
        return self._grafo.number_of_edges()

    def esiste_oggetto(self, obj_id):
        return obj_id in self._idMap