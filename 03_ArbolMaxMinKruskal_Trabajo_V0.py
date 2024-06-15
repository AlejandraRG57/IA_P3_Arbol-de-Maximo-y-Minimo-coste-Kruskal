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
            'A': (10.5,0), 'B': (9.8,2), 'C': (10.8,3.4), 'D': (7.6,3), 
            'E': (7.8,4.8), 'F': (4.1,6.2), 'G': (0,5.9), 'H': (.4,2.8)
        }

        #Agregamos todas las aristas al grafo de networkx.
        for edge in all_edges:
            from_node, to_node, weight = edge
            G.add_edge(from_node, to_node, weight=weight)

        plt.figure(figsize=(10, 6)) #Configuramos el tamaño de la figura.

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
for node in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
    game_map.add_node(node)

#Agregamos aristas al grafo con sus pesos.
game_map.add_edge('A', 'H', 20)
game_map.add_edge('A', 'G', 25)
game_map.add_edge('A', 'D', 5)
game_map.add_edge('A', 'B', 2)
game_map.add_edge('A', 'C', 4)

game_map.add_edge('B', 'A', 2)
game_map.add_edge('B', 'C', 1)
game_map.add_edge('B', 'E', 2)
game_map.add_edge('B', 'D', 2)
game_map.add_edge('B', 'H', 20)

game_map.add_edge('C', 'A', 4)
game_map.add_edge('C', 'B', 1)
game_map.add_edge('C', 'E', 5)

game_map.add_edge('D', 'A', 5)
game_map.add_edge('D', 'B', 2)
game_map.add_edge('D', 'E', 2)
game_map.add_edge('D', 'F', 7)
game_map.add_edge('D', 'G', 15)
game_map.add_edge('D', 'H', 15)

game_map.add_edge('E', 'C', 5)
game_map.add_edge('E', 'B', 2)
game_map.add_edge('E', 'D', 2)
game_map.add_edge('E', 'H', 15)
game_map.add_edge('E', 'F', 5)

game_map.add_edge('F', 'E', 5)
game_map.add_edge('F', 'D', 7)
game_map.add_edge('F', 'H', 10)
game_map.add_edge('F', 'G', 5)

game_map.add_edge('G', 'F', 5)
game_map.add_edge('G', 'D', 15)
game_map.add_edge('G', 'A', 25)
game_map.add_edge('G', 'H', 5)

game_map.add_edge('H', 'A', 20)
game_map.add_edge('H', 'B', 20)
game_map.add_edge('H', 'D', 15)
game_map.add_edge('H', 'E', 15)
game_map.add_edge('H', 'F', 10)
game_map.add_edge('H', 'G', 5)

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