import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            min_album= int(self._view.txtNumAlbumMin.value)
            if min_album <= 0:
                self._view.show_alert(f"Errore nell'inserimento del Numero album minimo")
                return
        except:
            self._view.show_alert(f"Errore nell'inserimento del Numero album minimo")


        self._model.build_graph(min_album)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f'Grafo creato: {len(self._model._nodes)} nodi (artisti), {self._model._graph.number_of_edges()} archi'))

        for nodo in self._model._nodes.values():
            #print(nodo) -> oggetto
            self._view.ddArtist.options.append(ft.dropdown.Option(text = nodo.name, key= nodo.id))

        self._view.update_page()

    def handle_connected_artists(self, e):
        id_artista = int(self._view.ddArtist.value)
        #print(f'id_artista: {id_artista}')
        artista = self._model.get_artista_oggetto(id_artista)
        #print(f'artista: {artista}')
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Artisti direttamente collegati all'artista {artista}"))

        for artista, peso in self._model.artisti_collegati(artista):
            #print(f'artista: {artista}')
            #print(f'peso: {peso}')
            self._view.txt_result.controls.append(ft.Text(f'{artista} - Numero di generi in comune: {peso['weight']}'))
            self._view.update_page()

    def cerca_cammino(self, e):
        try:
            durata_minima = float(self._view.txtMinDuration.value)
            if durata_minima <= 0:
                self._view.show_alert(f"Errore nell'inserimento della durata minima")
                return
            numero_artisti_max = int(self._view.txtMaxArtists.value)
            if numero_artisti_max < 0 or numero_artisti_max > len(self._model._nodes):
                self._view.show_alert(f"Errore nell'inserimento del numero di artisti massimo")
                return
        except:
            self._view.show_alert(f"Errore nell'inserimento dei dati")
        NumAlbum = int(self._view.txtNumAlbumMin.value)
        id_artista = int(self._view.ddArtist.value)
        artista_iniziale = self._model.get_artista_oggetto(id_artista)
        soluzione_migliore, peso_totale_max = self._model.cammino_max(durata_minima, numero_artisti_max, artista_iniziale, NumAlbum)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Cammino di peso massimo dall'artista {artista_iniziale}"))
        self._view.txt_result.controls.append(ft.Text(f"Lunghezza {len(soluzione_migliore)}"))
        for artista in soluzione_migliore:
            self._view.txt_result.controls.append(ft.Text(artista))
        self._view.txt_result.controls.append(ft.Text(f"Peso massimo {peso_totale_max}"))


        self._view.update_page()







