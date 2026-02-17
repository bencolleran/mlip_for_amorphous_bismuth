from ase.io import read
from pymatgen.io.ase import AseAtomsAdaptor
from autoplex.misc.castep.jobs import BaseCastepMaker, CastepStaticMaker
from autoplex.misc.castep.utils import CastepInputGenerator, CastepStaticSetGenerator
from jobflow import Flow
from jobflow_remote import submit_flow
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]

#want to try 1,1,1 2,2,2 and 3,3,3 for the 

# ls=[]
# for i in range(1,4):
#     for j in range(1,4):
#         ls.append([i,f"{j} {j} {j}"])

ls=[[1, '1 1 1'], [1, '2 2 2'], [1, '3 3 3'], [2, '1 1 1'], [2, '2 2 2'], [2, '3 3 3'], [3, '1 1 1'], [3, '2 2 2'], [3, '3 3 3']]

jobs=[]
#ls=[[1, '1 1 1'], [1, '2 2 2'], [1, '3 3 3'], [2, '1 1 1'], [2, '2 2 2'], [2, '3 3 3'], [3, '1 1 1'], [3, '2 2 2'], [3, '3 3 3']]
for item in ls:
    atoms = read(f'{PROJECT_ROOT}/{item[0]}.dat', format="lammps-dump-text",specorder=["Bi"])#how to read lammps dump files
    pmg_structure = AseAtomsAdaptor.get_structure(atoms)
    calc=BaseCastepMaker(
    input_set_generator=CastepStaticSetGenerator(
        user_param_settings={
        "task": 'SINGLEPOINT',
        'cut_off_energy': 600,
        'xc_functional': "PBE",
        'max_scf_cycles': 100,
        },
        user_cell_settings={
        "kpoints_mp_grid": item[1],
        "species_pot": [("Bi", 'SOC19')],
        }
    )
)
    job=calc.make(structure=pmg_structure)
    job.name=f"{item[0]}_{item[1]}"
    jobs.append(job)

flow=Flow(jobs, name="castep_test")
resources = {"qverbatim": "#$ -cwd\n#$ -pe smp 128\n#$ -N Autoplex_jf_test\n#$ -o $JOB_ID.log\n#$ -e $JOB_ID.err\n#$ -P cpu\n#$ -l s_rt=05:00:00"}
print(submit_flow(flow , worker="autoplex_project_worker", resources=resources, project="autoplex_project"))