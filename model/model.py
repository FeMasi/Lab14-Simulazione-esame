import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self._idMap = {}
        self.solBest = []
        self._numRicorsione = 0

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
            #print(k, v)
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
        contatore = 0
        for e in self.get_edges():
            if e[2]['weight'] > s:
                contatore += 1
        #print(contatore)
        return contatore

    def contaArchiMinoriDiSoglia(self, s):
        c = self.getNumEdges() - self.contaArchiMaggioriDiSoglia(s)
        #print(c)
        return c

    def cerca_cammino(self, s):
        self._numRicorsione = 0
        self.solBest.clear()
        for n in self.get_nodes():
            partial= []
            partial_edges = []

            partial.append(n)
            self.ricorsione(partial, partial_edges, s)
        print("final" , len(self.solBest), [i[2]['weight'] for i in self.solBest])


    def ricorsione(self, partial, partial_edges, s):
        print(f"ricorsione: {self._numRicorsione}")
        self._numRicorsione += 1
        n_last = partial[-1]
        neigh = self.getAdmissibleNeigh(n_last, partial_edges, s)
        #stop condition
        if len(neigh) == 0:
            weight_path = self.computeWeightPath(partial_edges)
            weight_path_best = self.computeWeightPath(self.solBest)
            if weight_path_best < weight_path:
                self.solBest = partial_edges[:]
            return
        #ricorsione
        for n in neigh:
            partial.append(n)
            partial_edges.append((n_last, n, self._graph.get_edge_data(n_last, n)))
            self.ricorsione(partial, partial_edges, s)
            partial.pop()
            partial_edges.pop()



    def getAdmissibleNeigh(self, n_last, partial_edges, s):
        all_neigh = self._graph.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if e[2]['weight'] > s:
                e_inv = (e[1], e[0], e[2])
                if (e_inv not in partial_edges) and (e not in partial_edges):
                    result.append(e[1])
        return result

    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight