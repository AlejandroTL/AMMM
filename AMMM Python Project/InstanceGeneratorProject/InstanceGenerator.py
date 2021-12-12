'''
AMMM P3 Instance Generator v2.0
Instance Generator class.
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
import math
import os, random
from AMMMGlobals import AMMMException
import numpy as np
from random import uniform, randrange

class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):

        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        V = self.config.V
        E = self.config.E
        W = self.config.W
        F = self.config.F

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            G = np.zeros(shape=(V, V))
            H = np.zeros(shape=(W, W))

            fInstance.write('n = %d;\n' % V)
            fInstance.write('m = %d;\n' % W)
            fInstance.write('\n')

            iterations = E
            while iterations > 0:
                row = randrange(0, V)
                col = randrange(0, V)
                if G[row, col] == 0 and (row != col):
                    G[row, col] = round(uniform(0, 1),2)
                    G[col, row] = G[row, col]
                    iterations = iterations - 1

            iterations = F
            while iterations > 0:
                row = randrange(0, W)
                col = randrange(0, W)
                if H[row, col] == 0 and (row != col):
                    H[row, col] = round(uniform(0, 1),2)
                    H[col, row] = H[row, col]
                    iterations = iterations - 1

            np.set_printoptions(threshold=np.inf, linewidth=np.inf)
            fInstance.write('G = \n%s;\n' % G)
            fInstance.write('\n')
            fInstance.write('H = \n%s;\n' % H)

            fInstance.close()
