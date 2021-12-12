'''
AMMM P3 Instance Generator v2.0
Main function.
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

import sys
from Heuristics.datParser import DATParser
from InstanceGeneratorProject.ValidateConfig import ValidateConfig
from InstanceGeneratorProject.InstanceGenerator import InstanceGenerator
from AMMMGlobals import AMMMException
import numpy as np

def run():
    try:
        list_la = [0.15, 0.2, 0.3]
        list_dG = [0.4, 0.6]
        list_dH = [0.4, 0.6]
        list_sizes = [30]#[40, 42, 44, 46, 48, 50]
        configFile = "config\config.dat"
        print("AMMM Instance Generator")
        print("-----------------------")
        print("Reading Config file %s..." % configFile)
        config = DATParser.parse(configFile)
        baseline = config.fileNamePrefix
        for size in list_sizes:
            for la in list_la:
                for dG in list_dG:
                    for dH in list_dH:
                        config.fileNamePrefix = baseline+'_'+str(la)+'_'+str(dG)+'_'+str(dH)+'_'+str(size)
                        config.V = size
                        config.E = round(config.V*(config.V-1)*dG/2)
                        config.W = round(config.V*la)
                        config.F = round(config.W*(config.W-1)*dH/2)
                        if config.F < config.W-1: config.F = config.W-1
                        print("V = %i, E = %i, W = %i, F = %i"%(config.V,config.E,config.W,config.F))
                        #ValidateConfig.validate(config)
                        print("Creating Instances...")
                        instGen = InstanceGenerator(config)
                        instGen.generate()
                        print("Done")
        return 0
    except AMMMException as e:
        print("Exception: %s", e)
        return 1


if __name__ == '__main__':
    sys.exit(run())
