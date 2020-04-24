#!/usr/bin/python3
#######################################################################
# Copyright 2020 Josep Argelich

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

# Libraries

import sys
import random
import frontier1
import networkx as nx
import pygraphviz as pgv

# Classes

class CNF():
    """A CNF formula randomly generated"""

    def __init__(self, num_nodes, edge_prob, num_colors):
        """
        Initialization
        num_nodes: Number of nodes
        edge_prob: Edge probability between two nodes
        num_colors: Number of colors to color the graph
        clauses: List of clauses
        """
        self.num_nodes = num_nodes
        self.edge_prob = edge_prob
        self.num_colors = num_colors
        self.clauses = []
        self.gen_node_clauses()
        self.gen_edge_clauses()

    def gen_node_clauses(self):
        '''Generate the ALO + AMO clauses for all the nodes'''
        for n in range(self.num_nodes):
            # ALO
            var1 = n * self.num_colors + 1
            self.clauses.append([i for i in range(var1, var1 + self.num_colors)])
            # AMO
            for v1 in range(var1, var1 + self.num_colors - 1):
                for v2 in range(v1 + 1, var1 + self.num_colors):
                    self.clauses.append([-v1, -v2])
            graph_structure.add_node(n+1)

    def gen_edge_clauses(self):
        '''Generates the clauses for each pair of nodes that have an edge with certain prob'''
        for n1 in range(self.num_nodes - 1):
            for n2 in range(n1 + 1, self.num_nodes):
                if random.random() < self.edge_prob:
                    var1 = n1 * self.num_colors + 1
                    var2 = n2 * self.num_colors + 1
                    for c in range(self.num_colors):
                        self.clauses.append([-(var1 + c), -(var2 + c)])
                        graph_structure.add_edge(n1+1, n2+1)

    def show(self):
        """Prints the formula to the stdout"""
        sys.stdout.write("c Random CNF formula\n")
        sys.stdout.write("p cnf %d %d\n" % (self.num_nodes * self.num_colors, len(self.clauses)))
        for c in self.clauses:
            sys.stdout.write("%s 0\n" % " ".join(map(str, c)))

    def write(self):
        """Write the formula to a file"""
        f = open("graph-coloring-cnf.txt", "w")
        f.write("c Random CNF formula\n")
        f.write("p cnf %d %d\n" % (self.num_nodes * self.num_colors, len(self.clauses)))
        for c in self.clauses:
            f.write("%s 0\n" % " ".join(map(str, c)))
        f.close()

def draw_graph():

    # Possible colore
    colors = {1:"red", 2:"blue", 3:"green", 4:"yellow", 5:"purple", 6:"orange", 7:"brown", 8:"pink", 9:"grey", 10:"white"}

    # Write the generated formula to a file
    cnf_formula.write()

    # Call the solver and get the solution
    solution = frontier1.solve("graph-coloring-cnf.txt")
    print("\nSolver solution:\n", " ".join(solution))

    # Get coloring solution
    for node_num in range(num_nodes):

        # For each node we obtain its possible colors
        possible_node_colors = solution[node_num*num_colors:node_num*num_colors+num_colors]

        # For each node we obtain its color
        for color in possible_node_colors:
            if int(color)>0:
                node_color = abs(int(color))%num_colors
                if node_color == 0:
                    node_color = num_colors

        # Add color to node
        graph_structure.add_node(node_num+1,style='filled',fillcolor=colors.get(node_color))

    # Draw the graph
    graph_drawing = nx.nx_agraph.to_agraph(graph_structure)
    graph_drawing.layout(prog='dot')
    graph_drawing.draw('colored-graph.png')

# Main

if __name__ == '__main__' :
    """A random CNF generator"""

    # Check parameters
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        sys.exit("Use:   %s <num-nodes> <edge-prob> <num-colors> [<random-seed>]" % sys.argv[0])

    try:
        num_nodes = int(sys.argv[1])
    except:
        sys.exit("ERROR: Number of nodes not an integer (%s)." % sys.argv[1])
    if (num_nodes < 1):
        sys.exit("ERROR: Number of nodes must be >= 1 (%d)." % num_nodes)

    try:
        edge_prob = float(sys.argv[2])
    except:
        sys.exit("ERROR: Edge probability not a float (%s)." % sys.argv[2])
    if (edge_prob < 0 or edge_prob > 1):
        sys.exit("ERROR: Edge probability must be in [0, 1] range (%d)." % edge_prob)

    try:
        num_colors = int(sys.argv[3])
    except:
        sys.exit("ERROR: Number of colors not an integer (%s)." % sys.argv[3])
    if (num_colors < 1):
        sys.exit("ERROR: Number of colors must be >= 1 (%d)." % num_colors)

    if len(sys.argv) > 4:
        try:
            seed = int(sys.argv[4])
        except:
            sys.exit("ERROR: Seed number not an integer (%s)." % sys.argv[4])
    else:
        seed = None

    # Initialize graph structure
    graph_structure = nx.Graph()

    # Initialize random seed (current time)
    random.seed(seed)

    # Create a CNF instance
    cnf_formula = CNF(num_nodes, edge_prob, num_colors)

    # Show formula
    cnf_formula.show()

    # Draw the graph generated with the coloring of the solution
    draw_graph()
