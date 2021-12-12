"""
AMMM Lab Heuristics
Representation of a problem instance
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from Heuristics.problem.Graph import Graph, Vertex
from Heuristics.problem.solution import Solution
import numpy as np


class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        self.n = inputData.n
        self.m = inputData.m

        G = Graph()
        for i in range(self.n):
            G.add_vertex(i + 1)
        i = 1
        for row in inputData.G:
            j = 1
            for item in np.array(list(row)):
                if item > 0:
                    G.add_edge(i, j, item)
                j += 1
            i += 1

        H = Graph()
        for i in range(self.m):
            H.add_vertex(i + 1)
        i = 1
        for row in inputData.H:
            j = 1
            for item in np.array(list(row)):
                if item > 0:
                    H.add_edge(i, j, item)
                j += 1
            i += 1

        self.G = G
        self.H = H

    def getNumNodesImage(self):
        return self.n

    def getNumNodesShape(self):
        return self.m

    def createSolution(self):
        solution = Solution(self.G, self.H)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        vertexG = self.G.get_vertices()
        vertexH = self.H.get_vertices()
        edgesG = 0
        for node in vertexG:
            edgesG += len(self.G.get_vertex(node).get_connections())
        edgesH = 0
        for node in vertexH:
            edgesH += len(self.H.get_vertex(node).get_connections())

        if len(vertexG) < len(vertexH) or edgesG < edgesH:
            return False
        else:
            return True
