"""
AMMM Lab Heuristics
Representation of a solution instance
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

import copy
from Heuristics.solution import _Solution


# This class stores the load of the highest loaded CPU
# when a task is assigned to a CPU.
#class Assignment(object):
#    def __init__(self, taskId, cpuId, highestLoad):
#        self.taskId = taskId
#        self.cpuId = cpuId
#        self.highestLoad = highestLoad

#    def __str__(self):
#        return "<t_%d, c_%d>: highestLoad: %.2f%%" % (self.taskId, self.cpuId, self.highestLoad*100)


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, G, H):
        self.G = G
        self.H = H
        self.embedding = {}
        self.cost = 0.0
        super().__init__()

    def computeCost(self, nodeImage, nodeShape):

        cost = 0
        for neighbor_shape, neighbor_image in self.embedding.items():

            if neighbor_image not in list(nodeImage.adjacent.keys()) or neighbor_shape not in list(nodeShape.adjacent.keys()):
                local_cost = 0
            else:
                weight1 = nodeShape.get_weight(neighbor_shape)
                weight2 = nodeImage.get_weight(neighbor_image)
                local_cost = abs(weight2-weight1)

            cost = cost + local_cost

        return cost

    def solutionCost(self):
        cost = 0

        for neighbor_shape, neighbor_image in self.embedding.items():
            for nodeShapeIndex, nodeImageIndex in self.embedding.items():
                nodeImage = self.G.vert_dict[nodeImageIndex]
                nodeShape = self.H.vert_dict[nodeShapeIndex]
                if neighbor_image not in list(nodeImage.adjacent.keys()) or neighbor_shape not in list(
                        nodeShape.adjacent.keys()):
                    local_cost = 0
                else:
                    weight1 = nodeShape.get_weight(neighbor_shape)
                    weight2 = nodeImage.get_weight(neighbor_image)
                    local_cost = abs(weight2 - weight1)
                cost = cost + local_cost

        return cost/2


    def isFeasibleToAssignImagetoShape(self, nodeImage, nodeShape):
        #print(nodeImage.id, nodeShape.id, list(self.embedding.values()))
        if nodeImage.id in list(self.embedding.values()):
            #print("I'm returning False")
            return False

        if len(nodeImage.adjacent) < len(nodeShape.adjacent):
            return False

        embedding_keys = list(self.embedding.keys())
        embedding_values = list(self.embedding.values())
        neighbors_nodeS = list(nodeShape.adjacent.keys())
        neighbors_nodeI = list(nodeImage.adjacent.keys())

        #matches_shape = len(set(embedding_keys).intersection(neighbors_nodeS))
        matches_shape = set(embedding_keys).intersection(neighbors_nodeS)
        f_ms = [self.embedding[x] for x in matches_shape]
        #print("Intersection Shape: ", matches_shape)
        #matches_image = len(set(embedding_values).intersection(neighbors_nodeI))
        matches_image = set(embedding_values).intersection(neighbors_nodeI)
        #print("Intersection Image: ", matches_image)

        #if matches_shape != matches_image:
        if set(f_ms) != matches_image:
            return False

        return True

    def assign(self, nodeImage, nodeShape):
        self.embedding[nodeShape.id] = nodeImage.id

        return True

    def unassign(self, taskId, cpuId):
        if not self.isFeasibleToUnassignTaskFromCPU(taskId, cpuId): return False

        del self.taskIdToCPUId[taskId]
        self.cpuIdToListTaskId[cpuId].remove(taskId)
        self.availCapacityPerCPUId[cpuId] += self.tasks[taskId].getTotalResources()

        self.updateHighestLoad()
        return True

    #def findFeasibleAssignments(self, taskId):
    #    feasibleAssignments = []
    #    for cpu in self.cpus:
    #        cpuId = cpu.getId()
    #        feasible = self.assign(taskId, cpuId)
    #        if not feasible: continue
    #        assignment = Assignment(taskId, cpuId, self.fitness)
    #        feasibleAssignments.append(assignment)

    #        self.unassign(taskId, cpuId)

    #    return feasibleAssignments

    #def findBestFeasibleAssignment(self, taskId):
    #    bestAssignment = Assignment(taskId, None, float('infinity'))
    #    for cpu in self.cpus:
    #        cpuId = cpu.getId()
    #        feasible = self.assign(taskId, cpuId)
    #        if not feasible: continue

    #        curHighestLoad = self.fitness
    #        if bestAssignment.highestLoad > curHighestLoad:
    #            bestAssignment.cpuId = cpuId
    #            bestAssignment.highestLoad = curHighestLoad

    #        self.unassign(taskId, cpuId)

    #    return bestAssignment

    def __str__(self):
        strSolution = 'OBJECTIVE = %10.3f;\n' % self.cost
        #strSolution = str(self.embedding)
        if self.cost == float('inf'): return strSolution

        for key, value in self.embedding.items():
            strSolution += 'f('+str(key)+')' + ' = ' + str(value) + '\n'

        return strSolution

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
