import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        self._nodes = None
        self._edges = None

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        #print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        pass

    def build_graph(self, min_album):
        self._graph.clear()
        #print(f'Num min: {min_album}') -> 5
        self._nodes = DAO.get_artisti_n_maggiore_album(min_album)
        #print(f'numero nodi: {len(self._nodes)}')
        self._graph.add_nodes_from(self._nodes)
        #print(f'Nodi: {self._graph.nodes}') -> Artist(id=1, name='AC/DC')
        self._edges = DAO.get_all_edges(min_album, self._nodes)
        for arco in self._edges.values():
            self._graph.add_edge(arco.a1, arco.a2, weight= arco.peso)
            #print(f'ARCO: {arco}') -> Collegamento : 22 - 58,peso : 2

    def get_artista_oggetto(self, id_artista):
        diz_artisti = DAO.get_artisti()
        return diz_artisti.get(id_artista)

    def artisti_collegati(self, nodo):
        artisti_peso = []
        for artista in self._graph.neighbors(nodo):
            artisti_peso.append((artista, self._graph.get_edge_data(nodo, artista)))
        return artisti_peso

    def cammino_max(self, durata_minima, numero_artisti_max, artista_iniziale, NumAlbum):
        self.soluzione_migliore = []
        self.percorso_archi = []
        self.peso_totale_max = 0
        #print(f'durata minima: {durata_minima}') -> 3.2
        #print(f'numero artisti max: {numero_artisti_max}') -> 6
        #print(f'artista iniziale: {artista_iniziale}') -> oggetto
        sequenza_parziale = [artista_iniziale]
        archi_esplorati = []
        self._ricorsione(sequenza_parziale, archi_esplorati, durata_minima, numero_artisti_max, NumAlbum)
        return

    def _ricorsione(self, sequenza_parziale, archi_esplorati, durata_minima, numero_artisti_max, NumAlbum):
        ultimo_nodo = sequenza_parziale[-1]
        vicini_ultimo_nodo = self.get_vicini_nodo(ultimo_nodo, durata_minima, NumAlbum)

        if len(sequenza_parziale) == numero_artisti_max:
            peso_cammino = self.calcola_peso_percorso(archi_esplorati)
            if peso_cammino > self.peso_totale_max:
                self.peso_totale_max = peso_cammino
                self.soluzione_migliore = sequenza_parziale[:]
                self.percorso_archi = archi_esplorati[:]
            return self.soluzione_migliore , self.peso_totale_max

        if vicini_ultimo_nodo is None:
            for vicino in vicini_ultimo_nodo:
                archi_esplorati.append(ultimo_nodo, vicino, self._graph.get_edge_data(ultimo_nodo, vicino)['weight'])
                sequenza_parziale.append(vicino)

                self._ricorsione(sequenza_parziale, archi_esplorati, durata_minima, numero_artisti_max)

                sequenza_parziale.pop()
                archi_esplorati.pop()

    def calcola_peso_percorso(self, archi_esplorati):
        tot = 0
        for arco in archi_esplorati:
            tot += arco[2]
        return tot

    def get_vicini_nodo(self, ultimo_nodo, durata_minima, NumAlbum):
        #print(f'ultimo nodo: {ultimo_nodo}') -> 90, Iron Maiden
        all_vicini = self._graph.neighbors(ultimo_nodo)
        print(f'vicini {all_vicini}')
        nodi_ammessi = DAO.get_artisti_canzone_min(durata_minima, NumAlbum)
        print(f'nodi {nodi_ammessi}')
        for vicino in all_vicini:
            if vicino in all_vicini:
                pass





