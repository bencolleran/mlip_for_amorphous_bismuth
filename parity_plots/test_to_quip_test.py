#read an extxyz file and label with quip then make quip extxyz file

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
import re,json
import numpy as np
from pathlib import Path
from ase.io import read,write
from quippy.potential import Potential
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", module="ase.calculators.castep")
warnings.filterwarnings("ignore", module="ase.io.castep")

PROJECT_ROOT = Path(__file__).resolve().parents[0]


test=f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip/new_test.extxyz"
train=f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip/new_train.extxyz"
frames=read(test,index=":")
for frame in frames:
    xml_path = f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip/GAP.xml"
    gap = Potential(args_str="IP GAP", param_filename=str(xml_path))#correct quip code
    frame.calc = gap
    frame.arrays['forces']=frame.get_forces()
    frame.info['energy']=frame.get_total_energy()
    if "initial_charges" in frame.arrays:
        frame.calc = None
        frame.arrays["charge"]=frame.arrays["initial_charges"]
        del frame.arrays["initial_charges"]
    if "magmoms" in frame.arrays:
        del frame.arrays["magmoms"]
    write(f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip/quip_new_test.extxyz", frame, format="extxyz",append=True)

# test=f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip/new_test.extxyz"
# train=f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip/new_train.extxyz"
# frames=read(test,index=":")
# for frame in frames:
#     xml_path = f"{PROJECT_ROOT}/potential_data/initial_autoplex_mlip/gap_file.xml"
#     gap = Potential(args_str="IP GAP", param_filename=str(xml_path))#correct quip code
#     frame.calc = gap
#     frame.arrays['forces']=frame.get_forces()
#     frame.info['energy']=frame.get_total_energy()
#     if "initial_charges" in frame.arrays:
#             frame.calc = None
#             frame.arrays["charge"]=frame.arrays["initial_charges"]
#             del frame.arrays["initial_charges"]
#     write(f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip/old_potential_test_quip_test.extxyz", frame, format="extxyz",append=True)

# test=f"{PROJECT_ROOT}/potential_data/initial_autoplex_mlip/test.extxyz"
# train=f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip/new_train.extxyz"
# frames=read(test,index=":")
# for frame in frames:
#     xml_path = f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip/GAP.xml"
#     gap = Potential(args_str="IP GAP", param_filename=str(xml_path))#correct quip code
#     frame.calc = gap
#     frame.arrays['forces']=frame.get_forces()
#     frame.info['energy']=frame.get_total_energy()
#     if "initial_charges" in frame.arrays:
#             frame.calc = None
#             frame.arrays["charge"]=frame.arrays["initial_charges"]
#             del frame.arrays["initial_charges"]
#     write(f"{PROJECT_ROOT}/potential_data/correct_extended_data_mlip/new_potential_on_old_test_quip_test.extxyz", frame, format="extxyz",append=True)

