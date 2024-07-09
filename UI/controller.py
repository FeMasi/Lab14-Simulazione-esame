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
        self._view.txt_result2.clean()
        self._view.txt_result3.clean()
        soglia = float(self._view.txt_name.value)
        #print(soglia)
        if soglia > self._model.getMaximumWeight() or soglia < self._model.getMinimumWeight():
            self._view.create_alert("Valore di soglia non valida!")
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso maggiore della soglia: {self._model.contaArchiMaggioriDiSoglia(soglia)}"))
        self._view.txt_result2.controls.append(ft.Text(
            f"Numero di archi con peso minore della soglia: {self._model.contaArchiMinoriDiSoglia(soglia)}"))
        self._view.update_page()
    def handle_search(self, e):
        self._view.txt_result3.clean()
        soglia = float(self._view.txt_name.value)

        self._model.cerca_cammino(soglia)
        self._view.txt_result3.controls.append(ft.Text(f"Numero archi percorso più lungo: {len(self._model.solBest)}"))
        self._view.txt_result3.controls.append(ft.Text(f"Peso complessivo del cammino: {self._model.computeWeightPath(self._model.solBest)}"))
        for e in self._model.solBest:
            self._view.txt_result3.controls.append(ft.Text(f"{e[0]} --> {e[1]}: {e[2]['weight']}"))


        self._view.update_page()