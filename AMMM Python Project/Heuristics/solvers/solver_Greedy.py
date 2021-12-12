'''
AMMM Lab Heuristics
Greedy solver
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
'''

import random, time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_Greedy(_Solver):

    def _selectCandidate(self, candidateList):
        if self.config.solver == 'Greedy':
            # sort candidate assignments by highestLoad in ascending order
            sortedCandidateList = sorted(candidateList.items(), key=lambda x: x[1])
            # choose assignment with minimum highest load
            return sortedCandidateList[0]
        return random.choice(candidateList)

    def _sortByEdges(self):
        NumberEdges = {}
        for node in self.instance.H.get_vertices():
            NumberEdges[node] = len(self.instance.H.vert_dict[node].get_connections())
        return sorted(NumberEdges.items(), key=lambda x: x[1], reverse=True)

    def construction(self):
        solution = self.instance.createSolution()
        sortedEdgesH = self._sortByEdges() # the node with more edges is the more restrictive
        for nodeHID in sortedEdgesH:
            nodeHID = nodeHID[0]
            all_costs = {}
            for nodeGID in range(self.instance.G.num_vertices):
                nodeGID = nodeGID + 1
                if nodeGID in solution.embedding.values() or not solution.isFeasibleToAssignImagetoShape(
                        self.instance.G.vert_dict[nodeGID], self.instance.H.vert_dict[nodeHID]):
                    continue
                else:
                    all_costs[nodeGID] = solution.computeCost(self.instance.G.vert_dict[nodeGID],
                                                              self.instance.H.vert_dict[nodeHID])
            if len(all_costs) == 0:
                solution.makeInfeasible()
                break
            else:
                bestCandidate = self._selectCandidate(all_costs)
                solution.assign(self.instance.G.get_vertex(bestCandidate[0]), self.instance.G.vert_dict[nodeHID])
                solution.cost = round(solution.cost + bestCandidate[1], 3)
        return solution

    def solve(self, **kwargs):
        self.startTimeMeasure()

        solver = kwargs.get('solver', None)
        if solver is not None:
            self.config.solver = solver
        localSearch = kwargs.get('localSearch', None)
        if localSearch is not None:
            self.config.localSearch = localSearch

        self.writeLogLine(float('inf'), 0)

        solution = self.construction()
        if self.config.localSearch:
            localSearch = LocalSearch(self.config, self.instance)
            endTime= self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.getCost(), 1)
        self.numSolutionsConstructed = 1
        self.printPerformance()

        return solution
