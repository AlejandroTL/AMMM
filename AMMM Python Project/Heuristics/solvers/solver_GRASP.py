'''
AMMM Lab Heuristics
GRASP solver
Copyright 2018 Luis Velasco.

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

import random
import time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidateGRASP(self, candidateList, alpha):

        # compute boundary highest load as a function of the minimum and maximum highest loads and the alpha parameter
        candidateList = {k: candidateList[k] for k in sorted(candidateList, key=candidateList.get)}
        minCost = list(candidateList.values())[0]
        maxCost = list(candidateList.values())[-1]
        boundaryCost = minCost + (maxCost - minCost) * alpha

        # find elements that fall into the RCL
        maxIndex = 0
        for node_GID in candidateList:
            if candidateList[node_GID] <= boundaryCost:
                maxIndex += 1

        # create RCL and pick an element randomly
        if maxIndex == 0:
            rclIndex = 0
        else:
            rclIndex = random.choice(list(range(maxIndex)))
        return list(candidateList.items())[rclIndex]


    def _sortByEdges(self):
        NumberEdges = {}
        for node in self.instance.H.get_vertices():
            NumberEdges[node] = len(self.instance.H.vert_dict[node].get_connections())
        return sorted(NumberEdges.items(), key=lambda x: x[1], reverse=True)

    def _greedyRandomizedConstruction(self, alpha):
        solution = self.instance.createSolution()
        sortedEdgesH = self._sortByEdges()
        for nodeHID in sortedEdgesH:
            nodeHID = nodeHID[0]
            all_costs = {}
            for nodeGID in range(self.instance.G.num_vertices):
                nodeGID = nodeGID + 1
                if nodeGID in solution.embedding.values() or not solution.isFeasibleToAssignImagetoShape(self.instance.G.vert_dict[nodeGID], self.instance.H.vert_dict[nodeHID]):
                    continue
                else:
                    all_costs[nodeGID] = solution.computeCost(self.instance.G.vert_dict[nodeGID], self.instance.H.vert_dict[nodeHID])
            if len(all_costs) == 0:
                solution.makeInfeasible()
                break
            else:
                selectedCandidate = self._selectCandidateGRASP(all_costs, alpha)
                solution.assign(self.instance.G.vert_dict[selectedCandidate[0]], self.instance.H.vert_dict[nodeHID])
                solution.cost = round(solution.cost + selectedCandidate[1], 3)
        return solution

    def stopCriteria(self, noImprove):
        self.elapsedEvalTime = time.time() - self.startTime
        if self.elapsedEvalTime > self.config.maxExecTime or noImprove > 900000:
            return True
        else:
            return False

    def solve(self, **kwargs):
        tuneAlpha = False
        repetitions = 5
        if tuneAlpha:
            alpha_list = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]*repetitions
            cost_list = {}
        else:
            alpha_list = [self.config.alpha]
            cost_list = {}
        for alpha_ref in alpha_list:

            self.startTimeMeasure()
            incumbent = self.instance.createSolution()
            incumbent.makeInfeasible()
            bestLowCost = 9999

            iteration = 0
            count = 0
            stop = False
            while not stop:
                stop = self.stopCriteria(count)
                iteration += 1
                # force first iteration as a Greedy execution (alpha == 0)
                alpha = 0 if iteration == 1 else alpha_ref

                solution = self._greedyRandomizedConstruction(alpha)
                grasp = solution.embedding

                if self.config.localSearch:
                    localSearch = LocalSearch(self.config, None)
                    endTime = self.startTime + self.config.maxExecTime
                    solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)


                if solution.isFeasible():
                    solutionLowCost = solution.solutionCost()
                    if solutionLowCost < bestLowCost:
                        count = 0
                        incumbent = solution
                        bestLowCost = solutionLowCost
                        self.writeLogLine(bestLowCost, iteration)
                        solution.cost = bestLowCost
                    else:
                        count+=1
            if alpha in cost_list:
                cost_list[alpha].append(bestLowCost)
            else:
                cost_list[alpha] = [bestLowCost]
            self.numSolutionsConstructed = iteration
            self.printPerformance()
        if tuneAlpha:
            print("Tunning ALPHA - cost per alpha: ", cost_list)
        return incumbent

