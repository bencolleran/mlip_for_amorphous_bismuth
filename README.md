# Machine-Learning-Driven Modelling of Amorphous Bismuth

This project contains all the work from my Masters degree project in modelling Amorphous Bismuth using Machine Learned Interatomic Potentials.

## Overview

The purpose of this project was to explore the structure of a-Bi to the highest accuracy yet. It follows on from previous work in Volker Deringer's group at the University of Oxford into the amorphous structures of the Group 15 elements, particularly Phosphourous and Arsenic. The project uses an automated iterative framework, Autoplex, to calcualate a machine learned interatomic potential for the system which is then used in Molecular Dynamics Simulations for fine tuning and structural analysis.

## Features

Some of the functionalities of the project are workflows for benchmarking DFT functionals, Convergence testing DFT parameters, Analysis tools for the outputs of the Autople workflow, Analysis tools for the outputs of LAMMPS simulations, Graph digitization tools and a range of workflows for fitting different machine learning architectures such as GAP and MACE.

## Dependencies

The project requires a working installation of:

- Python 3.10+
- autoplex==0.2.0  
- jobflow-remote==0.1.5  
- MongoDB  
- CASTEP  
- LAMMPS  