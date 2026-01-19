import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodes = []
    def build_graph(self, min_duration):
        self._grafo.clear()
        self._nodes = DAO.get_all_albums(min_duration)
        self._grafo.add_nodes_from(self._nodes)

        self.idMap = {a.album_id: a for a in self._nodes}
        edges = DAO.get_all_edges()

        for u, v in edges:
            if u in self.idMap and v in self.idMap:
                nodo_u = self.idMap[u]
                nodo_v = self.idMap[v]
                self._grafo.add_edge(nodo_u, nodo_v)

        print(f"Grafo creato! Nodi: {self._grafo.number_of_nodes()}, Archi: {self._grafo.number_of_edges()}")

    def get_nodes(self):
        return self._nodes

    def get_size_connessa(self, id_album):
        v0 = self.idMap[id_album]
        componente = nx.node_connected_component(self._grafo, v0)

        dimensione = len(componente)

        durata_complessiva = 0
        for album in componente:
            durata_complessiva += album.totD

        return dimensione, durata_complessiva