
import matplotlib.pyplot as plt
from ase.eos import EquationOfState
import numpy as np
import json
from ase.io import read
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from jobflow_remote.jobs.jobcontroller import JobController
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]

def get_job_output_dirs(db_id):
    jc = JobController.from_project_name("autoplex_project")
    doc=jc.get_jobs_info(db_ids=[str(db_id)])
    match = re.search(r"run_dir='([^']+)'", str(doc[0]))
    if match:
        run_dir = match.group(1)
        return f'{run_dir}/remote_job_data.json'

PBE_encut_666=[get_job_output_dirs(i) for i in range(1968,1995)]
RSCAN_encut_666=[get_job_output_dirs(i) for i in range(1995,2022)]
PBE_1100_kpoints=[get_job_output_dirs(i) for i in range(2022,2037)]
RSCAN_1100_kpoints=[get_job_output_dirs(i) for i in range(2037,2052)]

# np.set_printoptions(precision=4, suppress=True)
lst1=[PBE_encut_666,RSCAN_encut_666,PBE_1100_kpoints,RSCAN_1100_kpoints]

# filenames=lst1[0]

# energy, encut, xc, kpoints, forces =([] for i in range(5))
# for file in filenames:
#     with open(file,'r') as f:
#         data=json.load(f)
#     energy.append(data[0]['output']['output']["energy_per_atom"])
#     encut.append(data[0]['output']['input']['input_set']['param']['cut_off_energy'])
#     xc.append(data[0]['output']['input']['input_set']['param']['xc_functional'])
#     kpoints.append(data[0]['output']['input']['input_set']['cell']['kpoints_mp_grid'])
#     forces.append(data[0]['output']['output']["forces"])

# def name(file):
#     with open(file[0],'r') as f:
#         data=json.load(f)
#     encut_1=(data[0]['output']['input']['input_set']['param']['cut_off_energy'])
#     xc_1=(data[0]['output']['input']['input_set']['param']['xc_functional'])
#     kpoints_1=(data[0]['output']['input']['input_set']['cell']['kpoints_mp_grid'])[0]
#     if encut_1==1100:
#         return f'{xc_1}_{encut_1}_kpoints'
#     else:
#         return f'{xc_1}_encut_{kpoints_1}{kpoints_1}{kpoints_1}'





#make a function that calculates name of folder from json
#copy that folder to castep_data
#make a new function that allows the new data to be plotted

def new_name(file,kpoints=None):
    with open(file,'r') as f:
        data=json.load(f)
    encut_1=(data[0]['output']['input']['input_set']['param']['cut_off_energy'])
    xc_1=(data[0]['output']['input']['input_set']['param']['xc_functional'])
    kpoints_1=(data[0]['output']['input']['input_set']['cell']['kpoints_mp_grid']).split()[0]
    if kpoints:
        return f'{xc_1}_{encut_1}_kpoints'
    else:
        return f'{xc_1}_encut_{kpoints_1}_{kpoints_1}_{kpoints_1}'
    


#make a dictionary, key is name, value is directory
dict={}
for i in range(2):
    for j in range(len(lst1[i])):
        dict[new_name(lst1[i][j],kpoints=True)]=Path(lst1[i][j]).parent
for i in range(2,4):
    for j in range(len(lst1[i])):
        dict[new_name(lst1[i][j],kpoints=False)]=Path(lst1[i][j]).parent


#print(dict.keys())

# #!/usr/bin/env python3
# import shutil
# from pathlib import Path

# # <-- EDIT this mapping: keys are the new names, values are the source directories
# mapping=dict

# DEST_ROOT = Path("/u/vld/sedm7085/project/convergence_tests/castep_data")  # <-- destination root
# DEST_ROOT.mkdir(parents=True, exist_ok=True)

# # If True, overwrite any existing destination directory with the same name.
# OVERWRITE = False

# for name, src in mapping.items():
#     srcp = Path(src)
#     dst = DEST_ROOT / name

#     if not srcp.is_dir():
#         print(f"SKIP {name}: source not found or not a dir -> {src}")
#         continue

#     if dst.exists():
#         if OVERWRITE:
#             shutil.rmtree(dst)
#         else:
#             print(f"SKIP {name}: destination exists -> {dst}")
#             continue

#     shutil.copytree(srcp, dst)
#     print(f" COPIED {srcp} -> {dst}")


from pathlib import Path
import json

root = Path(f"{PROJECT_ROOT}/castep_data")
functional="PBE"
sweep_type="encut"
energy, encut, xc, kpoints, forces =([] for i in range(5))
for json_file in root.rglob("remote_job_data.json"):
    dirname = json_file.parent.name
    
    if functional in dirname and sweep_type in dirname:
        with open(json_file, 'r') as f:
            data = json.load(f)
        energy.append(data[0]['output']['output']["energy_per_atom"])
        encut.append(data[0]['output']['input']['input_set']['param']['cut_off_energy'])
        xc.append(data[0]['output']['input']['input_set']['param']['xc_functional'])
        kpoints.append(data[0]['output']['input']['input_set']['cell']['kpoints_mp_grid'].split()[0])
        forces.append(data[0]['output']['output']["forces"])
        encut_1=(data[0]['output']['input']['input_set']['param']['cut_off_energy'])
        xc_1=(data[0]['output']['input']['input_set']['param']['xc_functional'])
        kpoints_1=(data[0]['output']['input']['input_set']['cell']['kpoints_mp_grid']).split()[0]
        if sweep_type=="kpoints":
            name=f'{xc_1}_{encut_1}_kpoints'
        else:
            name=f'{xc_1}_encut_{kpoints_1}_{kpoints_1}_{kpoints_1}'
print(forces)
print(kpoints)

energy_dif=np.array([np.abs((energy[i+1]-energy[i]))*1000 for i in range(len(energy)-1)])#plot against Encut[1:]
energy_ref=np.array([np.abs(energy[i]-energy[-1])*1000 for i in range(len(energy))])
forces_rmse_ref=np.array([(np.sum([(np.linalg.norm(np.array(forces[j][i])-np.array(forces[-1][i])))/np.sqrt(6) for i in range(6)])/6) for j in range(len(forces))])

def plot_graph_encut(y_var):
    filepath=f'{PROJECT_ROOT}/graphs/'
    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(100))
    plt.yscale('log')
    if y_var[0]==energy_dif[0]:
        plt.grid(True)
        plt.xlabel('cut off energy / eV')
        plt.ylabel('log of energy change /meV')
        plt.scatter(encut[1:],energy_dif)
        plt.plot(np.linspace(300,1600,(len(energy)-2)),np.ones(len(energy)-2))
        plt.savefig(f"{filepath}{name}_energy_dif.png", dpi=600, bbox_inches="tight")
    elif y_var[0]==energy_ref[0]:
        plt.grid(True)
        plt.xlabel('cut off energy / eV')
        plt.ylabel('log of energy relative to final energy /meV')
        plt.scatter(encut,energy_ref)
        plt.plot(np.linspace(300,1600,(len(energy)-2)),np.ones(len(energy)-2))
        plt.plot(np.linspace(300,1600,(len(energy)-2)),np.ones(len(energy)-2)/10)
        plt.savefig(f"{filepath}{name}_energy_ref.png", dpi=600, bbox_inches="tight")
    elif y_var[0]==forces_rmse_ref[0]:
        plt.grid(True)
        plt.xlabel('cut off energy / eV')
        plt.ylabel('log of rmse forces relative to final forces per atom / eV/A')
        plt.scatter(encut,forces_rmse_ref)
        #plt.plot(np.linspace(300,1600,(len(energy)-2)),np.ones(len(energy)-2))
        plt.savefig(f"{filepath}{name}_forces_rmse_ref.png", dpi=600, bbox_inches="tight")

def plot_graph_kpoints(y_var):
    kpoints=list(range(6,21))
    filepath=f'{PROJECT_ROOT}/graphs/'
    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator())
    plt.yscale('log')
    if y_var[0]==energy_dif[0]:
        plt.grid(True)
        plt.xlabel('kpoints')
        plt.ylabel('log of energy change /meV')
        plt.scatter(kpoints[1:],energy_dif)
        plt.plot(np.linspace(6,20,(len(energy)-2)),np.ones(len(energy)-2))
        plt.savefig(f"{filepath}{name}_energy_dif.png", dpi=600, bbox_inches="tight")
    elif y_var[0]==energy_ref[0]:
        plt.grid(True)
        plt.xlabel('kpoints')
        plt.ylabel('log of energy relative to final energy /meV')
        plt.scatter(kpoints,energy_ref)
        plt.plot(np.linspace(6,20,(len(energy)-2)),np.ones(len(energy)-2))
        plt.savefig(f"{filepath}{name}_energy_ref.png", dpi=600, bbox_inches="tight")
    elif y_var[0]==forces_rmse_ref[0]:
        print(len(kpoints),len(forces_rmse_ref))
        plt.grid(True)
        plt.xlabel('kpoints')
        plt.ylabel('log of rmse forces relative to final forces per atom / eV/A')
        plt.scatter(kpoints,forces_rmse_ref)
        plt.plot(np.linspace(6,20,(len(energy)-2)),np.ones(len(energy)-2))
        plt.savefig(f"{filepath}{name}_forces_rmse_ref.png", dpi=600, bbox_inches="tight")


# encut_change=True
# if encut_change==True:
#     plot_graph_encut(energy_ref)
#     #plot_graph_encut(energy_perc)
#     plot_graph_encut(energy_dif)
#     plot_graph_encut(forces_rmse_ref)
# else:
#     plot_graph_kpoints(energy_ref)
#     #plot_graph_kpoints(energy_perc)
#     plot_graph_kpoints(energy_dif)
#     plot_graph_kpoints(forces_rmse_ref)
# #had to rerun because all jobs were geometry optimizations
plot_graph_kpoints(forces_rmse_ref)