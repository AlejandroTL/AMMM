# Integer Linear Programming and Heuristics

Two different directories:

    AMMM Python Project: contains the Python files needed to create the problem instances and the Heuristics.
    AMMM CPLEX Project: contains the files needed to solve the problem instances with CPLEX.

## AMMM Python Project

### Instance Generator

This directory contains everything that is needed to create new problem instances.

Although we have provided you some instances, you are able to create yours by tunning the parameters specified in the config.dat file (./AMMM Python Project/InstanceGenerationProject/config/config.dat).
The parameters are called exactly as in the report, so it's easy to understand. Moreover, you can also modify the Main.py (./AMMM Python Project/InstanceGenerationProject/config/config.dat) to ease the generation directly fixing the densities and generate more that one file at once.

Once the Main.py is run, the output is stored in the folder output (./AMMM Python Project/InstanceGenerationProject/output). There are some generated files but you can generate more if you want.

### Heuristics

To select the Heuristic to use change the config file (./AMMM Python Project/Heuristics/config/config.dat). To solve a instance, it must be located at the data folder (./AMMM Python Project/Heuristics/data).

The solution is finally stored at the solution folder (/AMMM Python Project/Heuristics/solutions). It has the same output format as CPLEX. The console will also provide the final solution and the cost.

## AMMM CPLEX Project

Here there are contained some instances to test and also the CPLEX project. In particular, the CPLEX project is project.template.mod (./AMMM CPLEX Project/project.template.mod). Furthermore, there is another filled called execution_batch.mod (./AMMM CPLEX Project/execution_batch.mod) that executes different instances and outputs the result in a format suitable to be pasted into a CSV file. This is the way I've perfomed the analysis of increasing size and comparison with Heuristics.

To run the instances just create a Run Configuration, move there the right files (project.template.mod and the instance data file OR execution_batch.mod carefully edited to read the right data files).
