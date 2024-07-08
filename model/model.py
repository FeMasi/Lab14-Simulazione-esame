import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self._idMap = {}

        self._listChromosome = []
        self._listGenes = []
        self._listConnectedGenes = []

        self.loadChromosome()
        self.loadGenes()
        self.loadConnectedGenes()

    def loadChromosome(self):
        self._listChromosome = DAO.getAllChromosome()

    def loadGenes(self):
        self._listGenes = DAO.getAllGenes()
        for gene in self._listGenes:
            self._idMap[gene.GeneID] = gene.Chromosome

    def loadConnectedGenes(self):
        self._listConnectedGenes = DAO.getAllConnectedGenes()

    def build_graph(self):
        self._graph.clear()
        self._nodes.clear()
        self._edges.clear()

        for c in self._listChromosome:
            self._nodes.append(c)

        self._graph.add_nodes_from(self._nodes)

        edges = {}
        for g1, g2, corr in self._listConnectedGenes:
            if (self._idMap[g1], self._idMap[g2]) not in edges:
                edges[self._idMap[g1], self._idMap[g2]] = float(corr)
            else:
                edges[self._idMap[g1], self._idMap[g2]] += float(corr)

        for k, v in edges.items():
            print(k, v)
            self._edges.append((k[0], k[1], v))

        self._graph.add_weighted_edges_from(self._edges)


    def getNumNodes(self):
        return int(self._graph.number_of_nodes())

    def getNumEdges(self):
        return self._graph.number_of_edges()

    def getMaximumWeight(self):
        return max(x[2]['weight'] for x in self.get_edges())

    def getMinimumWeight(self):
        return min(x[2] ['weight'] for x in self.get_edges())

    def get_nodes(self):
        return self._graph.nodes()

    def get_edges(self):
        return list(self._graph.edges(data=True))

    def contaArchiMaggioriDiSoglia(self, s):

        pass

    def contaArchiMinoriDiSoglia(self, s):
        pass