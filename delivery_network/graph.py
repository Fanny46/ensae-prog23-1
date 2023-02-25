class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges.
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.nodes  : 
            self.nodes.append(node1)
            self.graph[node1]=[]
            self.nb_nodes+=1
        if node2 not in self.nodes : 
            self.nodes.append(node2)
            self.graph[node2]=[]
            self.nb_nodes+=1
        self.graph[node1]=self.graph[node1]+[[node2, power_min, dist]]
        self.graph[node2]=self.graph[node2]+[[node1, power_min, dist]]
        self.nb_edges+=1


    def get_path_with_power(self, src, dest, power):
        nodes_v={node : False for node in self.nodes} #dictionnaire qui permet de savoir si l'on est déjà passé par un point
        nodes_v[src] = True
        def parcours(node, chemin) :
            if node == dest:
                return chemin
            for i in self.graph[node] :
                k=i[0]
                k_power = i[1]
                if power >= k_power and not nodes_v[k]:
                    nodes_v[k]=True
                    return parcours(k, chemin+[k])
            return None
        
        return parcours(src, [src])

    def connected_components(self):
        l=[] #listes vides qui contiendra les listes de composants connectés
        nodes_v={node : False for node in self.nodes} #dictionnaire qui permet de savoir si l'on est déjà passé par un point

        def components(node) :
            comp=[node]
            for i in self.graph[node] :
                k=i[0]
                if not nodes_v[k] :
                    nodes_v[k]=True
                    comp+=components(k)
            return comp
        
        for k in self.nodes :
            if not nodes_v[k] : l.append(components(k))

        return l



    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest):
        dict_graph = {n : {self.graph[n][v][0] : self.graph[n][v][1] for v in range(len(self.graph[n]))} for n in self.nodes}
            
        from collections import deque
        def dijkstraAlgo(graph, src):
            queue = deque([src])
            power = {src: 0}
            power_min = 0
            while queue:
                t = queue.popleft()
                for voisin in graph[t]:
                        queue.append(voisin)
                        if(voisin not in power or power_min > power[voisin]):
                            power[voisin] = power_min
            return power[dest]
        
        return dijkstraAlgo(dict_graph, src)



        def parcours(node, chemin, power_min) :
            if node == dest:
                return chemin, power_min
            for i in self.graph[node] :
                k=i[0]
                k_power = i[1]
                if not nodes_v[k]:
                    nodes_v[k]=True
                    if k_power>power_min : power_min = k_power
                    return parcours(k, chemin+[k], power_min)
            return None
        
        return parcours(src, [src], 0)



def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    G: Graph
        An object of the class Graph with the graph from file_name.
    """
    f=open(filename)
    ligne=f.readline().split()
    nb_node=int(ligne[0])
    nb_edge=int(ligne[1])
    nodes=[i for i in range(1, nb_node+1)]
    G=Graph(nodes)
    for i in range(nb_edge) :
        ligne=f.readline().split()
        node1=int(ligne[0])
        node2=int(ligne[1])
        power_min=int(ligne[2])
        if len(ligne)==3 : G.add_edge(node1, node2, power_min)
        else : 
            dist=int(ligne[3])
            G.add_edge(node1, node2, power_min, dist)
    return G

g = graph_from_file("input/network.02.in")
print(g.min_power(1, 2))
