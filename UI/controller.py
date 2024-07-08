import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handle_graph(self, e):
        self._model.build_graph()
        self._view.txt_result.controls.append(ft.Text(f"grafo creato con {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi"))
        self._view.txt_result.controls.append(ft.Text(f"Arco di peso massimo: {self._model.getMaximumWeight()}"))
        self._view.txt_result.controls.append(ft.Text(f"Arco di peso minimo: {self._model.getMinimumWeight()}"))
        self._view.update_page()
    def handle_countedges(self, e):
        soglia = int(self._view.txt_name.value)
        print(soglia)
        if soglia > self._model.getMaximumWeight() or soglia < self._model.getMinimumWeight():
            self._view.create_alert("Valore di soglia non valida!")


    def handle_search(self, e):
        pass