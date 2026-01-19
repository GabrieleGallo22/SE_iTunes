import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        durata = self._view.txt_durata.value

        durata_float = float(durata)
        self._model.build_graph(durata_float)

        nodes = self._model.get_nodes()
        print(f"DEBUG: Ho trovato {len(nodes)} album nel grafo.")
        self._view.dd_album.options.clear()
        for a in nodes:
            self._view.dd_album.options.append(ft.dropdown.Option(text=a.title, data=a, key=a.album_id))
        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO

    def handle_analisi_comp(self, e):
        if self._view.dd_album.value is None:
            self._view.show_alert("Selezionare un album")

        id_album_selezionato = int(self._view.dd_album.value)
        size, durata_totale = self._model.get_size_connessa(id_album_selezionato)
        durata_minuti = durata_totale

        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Componente connessa - Dimensione: {size} nodi"))
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Durata totale componente: {durata_minuti:.2f} min"))
        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO