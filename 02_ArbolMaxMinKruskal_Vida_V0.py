#Alejandra Rodriguez Guevara 21310127 6E1

#Se maneja un grafo ponderado, lo que significa que cada arista del grafo tiene un 
# peso asignado. El propósito del algoritmo de Kruskal es identificar un árbol de 
# expansión mínima. Este árbol es un subconjunto de aristas que une todos los vértices 
# del grafo sin generar ciclos y con la suma de los pesos más baja posible.

import matplotlib.pyplot as plt #Importamos la biblioteca matplotlib para gráficos.
import networkx as nx #Importamos la biblioteca networkx para trabajar con grafos.

#Definimos de la clase Graph que representa un grafo.
class Graph:
    def __init__(self):
        self.nodes = set() #Conjunto para almacenar los nodos del grafo.
        self.edges = [] #Lista para almacenar las aristas del grafo.

    #Método para agregar un nodo al grafo.
    def add_node(self, value):
        self.nodes.add(value) #Agregamos el nodo al conjunto de nodos.

    #Método para agregar una arista al grafo.
    def add_edge(self, from_node, to_node, weight):
        self.edges.append((from_node, to_node, weight)) #Agregamos una arista a la lista de aristas.

    #Método para encontrar el representante de un nodo en el conjunto disjunto.
    def find(self, parent, node):
        if parent[node] != node: #Si el nodo no es su propio padre.
            parent[node] = self.find(parent, parent[node]) #Realizamos la compresión de caminos.
        return parent[node] #Devolvemos el representante del nodo.

    #Método para unir dos subconjuntos en el conjunto disjunto.
    def union(self, parent, rank, x, y):
        x_root = self.find(parent, x) #Encontramos el representante del primer subconjunto.
        y_root = self.find(parent, y) #Encontramos el representante del segundo subconjunto.

        if rank[x_root] < rank[y_root]: #Si el rango del primer subconjunto es menor.
            parent[x_root] = y_root #Unimos el primer subconjunto al segundo.
        elif rank[x_root] > rank[y_root]: #Si el rango del primer subconjunto es mayor.
            parent[y_root] = x_root #Unimos el segundo subconjunto al primero.
        else:
            parent[y_root] = x_root #Si los rangos son iguales, une uno al otro.
            rank[x_root] += 1 #Incrementamos el rango del nuevo subconjunto.

    #Método para encontrar el árbol de expansión mínima o máxima usando el algoritmo de Kruskal.
    def kruskal(self, find_minimum=True):
        parent = {} #Diccionario para almacenar el padre de cada nodo.
        rank = {} #Diccionario para almacenar el rango de cada nodo.

        #Inicializamos los conjuntos disjuntos para cada nodo.
        for node in self.nodes:
            parent[node] = node #Cada nodo es su propio padre inicialmente.
            rank[node] = 0 #El rango inicial de cada nodo es 0.

        minimum_spanning_tree = [] #Lista para el árbol de expansión mínima.
        maximum_spanning_tree = [] #Lista para el árbol de expansión máxima.

        #Ordenamos las aristas por peso, ascendente para el árbol mínimo, descendente para el árbol máximo.
        if find_minimum:
            edges = sorted(self.edges, key=lambda x: x[2]) #Ordenamos por peso ascendente.
        else:
            edges = sorted(self.edges, key=lambda x: x[2], reverse=True) #Ordenamos por peso descendente.

        #Recorremos las aristas ordenadas.
        for edge in edges:
            from_node, to_node, weight = edge #Desempaquetamos la arista.
            x = self.find(parent, from_node) #Encontramos el representante del nodo origen.
            y = self.find(parent, to_node) #Encontramos el representante del nodo destino.
            #Si los representantes son diferentes, no formamos un ciclo.
            if x != y:
                self.union(parent, rank, x, y) #Unimos los dos subconjuntos.
                if find_minimum:
                    minimum_spanning_tree.append(edge) #Agregamos la arista al árbol mínimo.
                else:
                    maximum_spanning_tree.append(edge) #Agregamos la arista al árbol máximo.

        #Devolvemos el árbol de expansión mínimo o máximo según corresponda.
        if find_minimum:
            return minimum_spanning_tree
        else:
            return maximum_spanning_tree

    #Método para dibujar el árbol de expansión en un gráfico.
    def draw_tree(self, tree_edges, all_edges):
        G = nx.Graph() #Creamos un objeto Graph de networkx.

        #Diccionario con las posiciones de los nodos para la visualización.
        positions = {
            'A': (0,9), 'B': (2.5,8.5), 'C': (4.9,7.9), 'D': (7.1,6.9), 
            'E': (8.4,6.2), 'F': (1.6,6.4), 'G': (4.1,5.9), 'H': (5.5,5.6),
            'I': (9.1,5.1), 'J': (6.6,4.9), 'K': (8.1,4.2), 'L': (5.5,4),
            'M': (7.8,3.4), 'N': (6.2,3.1), 'O': (8.9,3.2), 'P': (7.2,2.4),
            'Q': (10.1,2.4), 'R': (8.4,1.5), 'S': (10.1,1.2), 'T': (12.3,1),
            'U': (14.1,3.2), 'V': (13.6,2.2), 'W': (14.5,2.5)
        }

        #Agregamos todas las aristas al grafo de networkx.
        for edge in all_edges:
            from_node, to_node, weight = edge
            G.add_edge(from_node, to_node, weight=weight)

        plt.figure(figsize=(18, 12)) #Configuramos el tamaño de la figura.

        #Dibujamos todas las aristas en color negro.
        nx.draw(G, pos=positions, with_labels=True, node_color='skyblue', node_size=1000, font_size=10, font_weight='bold')
        nx.draw_networkx_edges(G, pos=positions, edgelist=all_edges, edge_color='black', width=1)

        #Dibujamos las aristas del árbol de expansión en rojo.
        nx.draw_networkx_edges(G, pos=positions, edgelist=tree_edges, edge_color='red', width=2)

        #Etiquetamos las aristas con sus pesos.
        edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=edge_labels)

        plt.title('Árbol de Expansión') #Título del gráfico.
        plt.show() #Mostramos el gráfico.

game_map = Graph() #Creamos una instancia de la clase Graph.

#Agregamos nodos al grafo.
for node in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']:
    game_map.add_node(node)

#Agregamos aristas al grafo con sus pesos.
game_map.add_edge('A', 'B', 2)
game_map.add_edge('A', 'F', 3)
game_map.add_edge('A', 'G', 6)
game_map.add_edge('A', 'H', 7)

game_map.add_edge('B', 'A', 2)
game_map.add_edge('B', 'F', 2)
game_map.add_edge('B', 'G', 3)
game_map.add_edge('B', 'H', 4)
game_map.add_edge('B', 'C', 2)

game_map.add_edge('C', 'B', 2)
game_map.add_edge('C', 'F', 3)
game_map.add_edge('C', 'G', 2)
game_map.add_edge('C', 'H', 2)
game_map.add_edge('C', 'D', 2)

game_map.add_edge('D', 'C', 2)
game_map.add_edge('D', 'G', 3)
game_map.add_edge('D', 'H', 2)
game_map.add_edge('D', 'J', 2)
game_map.add_edge('D', 'K', 3)
game_map.add_edge('D', 'E', 1)

game_map.add_edge('E', 'D', 1)
game_map.add_edge('E', 'H', 3)
game_map.add_edge('E', 'J', 3)
game_map.add_edge('E', 'K', 2)
game_map.add_edge('E', 'I', .5)
game_map.add_edge('E', 'U', 6)

game_map.add_edge('F', 'A', 3)
game_map.add_edge('F', 'B', 2)
game_map.add_edge('F', 'C', 3)
game_map.add_edge('F', 'G', 2)
game_map.add_edge('F', 'L', 4.5)

game_map.add_edge('G', 'F', 2)
game_map.add_edge('G', 'A', 6)
game_map.add_edge('G', 'B', 3)
game_map.add_edge('G', 'C', 2)
game_map.add_edge('G', 'D', 3)
game_map.add_edge('G', 'H', 1)
game_map.add_edge('G', 'L', 2)

game_map.add_edge('H', 'A', 1)
game_map.add_edge('H', 'B', 4)
game_map.add_edge('H', 'C', 1)
game_map.add_edge('H', 'D', 1)
game_map.add_edge('H', 'E', 4)
game_map.add_edge('H', 'J', 1)
game_map.add_edge('H', 'L', 4)
game_map.add_edge('H', 'G', 1)

game_map.add_edge('I', 'E', .5)
game_map.add_edge('I', 'K', 1)
game_map.add_edge('I', 'O', 2)
game_map.add_edge('I', 'Q', 3)
game_map.add_edge('I', 'V', 5)
game_map.add_edge('I', 'U', 5)

game_map.add_edge('J', 'H', 1)
game_map.add_edge('J', 'D', 2)
game_map.add_edge('J', 'E', 3)
game_map.add_edge('J', 'K', 1)
game_map.add_edge('J', 'M', 2)
game_map.add_edge('J', 'N', 2)
game_map.add_edge('J', 'L', 1)

game_map.add_edge('K', 'J', 1)
game_map.add_edge('K', 'D', 3)
game_map.add_edge('K', 'E', 2)
game_map.add_edge('K', 'I', 1)
game_map.add_edge('K', 'O', 1)
game_map.add_edge('K', 'M', .5)

game_map.add_edge('L', 'F', 4.5)
game_map.add_edge('L', 'G', 2)
game_map.add_edge('L', 'H', 4)
game_map.add_edge('L', 'J', 1)
game_map.add_edge('L', 'M', 2)
game_map.add_edge('L', 'N', .5)

game_map.add_edge('M', 'N', 1)
game_map.add_edge('M', 'L', 2)
game_map.add_edge('M', 'J', 2)
game_map.add_edge('M', 'K', .5)
game_map.add_edge('M', 'O', .5)
game_map.add_edge('M', 'R', 2)
game_map.add_edge('M', 'P', .5)

game_map.add_edge('N', 'L', .5)
game_map.add_edge('N', 'J', 2)
game_map.add_edge('N', 'M', 1)
game_map.add_edge('N', 'P', .5)

game_map.add_edge('O', 'M', .5)
game_map.add_edge('O', 'K', 1)
game_map.add_edge('O', 'I', 2)
game_map.add_edge('O', 'Q', 1)
game_map.add_edge('O', 'R', 1)
game_map.add_edge('O', 'P', 1)

game_map.add_edge('P', 'N', .5)
game_map.add_edge('P', 'M', .5)
game_map.add_edge('P', 'O', 1)
game_map.add_edge('P', 'R', 1)

game_map.add_edge('Q', 'I', 3)
game_map.add_edge('Q', 'U', 4)
game_map.add_edge('Q', 'W', 4)
game_map.add_edge('Q', 'V', 3)
game_map.add_edge('Q', 'T', 2.5)
game_map.add_edge('Q', 'S', 1)
game_map.add_edge('Q', 'R', 2)
game_map.add_edge('Q', 'O', 1)

game_map.add_edge('R', 'P', 1)
game_map.add_edge('R', 'M', 2)
game_map.add_edge('R', 'O', 1)
game_map.add_edge('R', 'Q', 2)
game_map.add_edge('R', 'S', 1)

game_map.add_edge('S', 'R', 1)
game_map.add_edge('S', 'Q', 1)
game_map.add_edge('S', 'V', 3)
game_map.add_edge('S', 'T', 2)

game_map.add_edge('T', 'S', 2)
game_map.add_edge('T', 'Q', 2.5)
game_map.add_edge('T', 'V', 2)
game_map.add_edge('T', 'W', 3)

game_map.add_edge('U', 'E', 6)
game_map.add_edge('U', 'I', 5)
game_map.add_edge('U', 'Q', 4)
game_map.add_edge('U', 'V', .5)
game_map.add_edge('U', 'W', .25)

game_map.add_edge('V', 'T', 2)
game_map.add_edge('V', 'S', 3)
game_map.add_edge('V', 'Q', 3)
game_map.add_edge('V', 'I', 5)
game_map.add_edge('V', 'U', .5)
game_map.add_edge('V', 'W', .25)

game_map.add_edge('W', 'T', 3)
game_map.add_edge('W', 'V', .25)
game_map.add_edge('W', 'Q', 4)
game_map.add_edge('W', 'U', .25)

#Encontramos el árbol de expansión mínima.
minimum_spanning_tree = game_map.kruskal(find_minimum=True)
print("Árbol de expansión mínima:", minimum_spanning_tree)

#Encontramos el árbol de expansión máxima.
maximum_spanning_tree = game_map.kruskal(find_minimum=False)
print("Árbol de expansión máxima:", maximum_spanning_tree)

#Dibujamos el árbol de expansión mínima y todas las aristas.
game_map.draw_tree(minimum_spanning_tree, game_map.edges)

#Dibujamos el árbol de expansión máxima y todas las aristas.
game_map.draw_tree(maximum_spanning_tree, game_map.edges)