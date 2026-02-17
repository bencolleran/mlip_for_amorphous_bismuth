
import matplotlib.pyplot as plt
from ase.eos import EquationOfState
import numpy as np
import json
from ase.io import read
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from jobflow_remote.jobs.jobcontroller import JobController
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]

root = Path(f"{PROJECT_ROOT}/castep_data")
functional="RSCAN"
fixed_var="kpoints"
energy, encut, xc, kpoints, forces =([] for i in range(5))
for json_file in root.rglob("remote_job_data.json"):
    dirname = json_file.parent.name
    
    if functional in dirname and fixed_var in dirname:
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
        if fixed_var=="encut":
            name=f'{xc_1}_{encut_1}_kpoints'
        else:
            name=f'{xc_1}_encut_{kpoints_1}{kpoints_1}{kpoints_1}'

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
        plt.grid(True)
        plt.xlabel('kpoints')
        plt.ylabel('log of rmse forces relative to final forces per atom / eV/A')
        plt.scatter(kpoints,forces_rmse_ref)
        plt.plot(np.linspace(6,20,(len(energy)-2)),np.ones(len(energy)-2))
        plt.savefig(f"{filepath}{name}_forces_rmse_ref.png", dpi=600, bbox_inches="tight")



if fixed_var=="kpoints":
    plot_graph_encut(energy_ref)
    #plot_graph_encut(energy_perc)
    plot_graph_encut(energy_dif)
    plot_graph_encut(forces_rmse_ref)
else:
    plot_graph_kpoints(energy_ref)
    #plot_graph_kpoints(energy_perc)
    plot_graph_kpoints(energy_dif)
    plot_graph_kpoints(forces_rmse_ref)
#had to rerun because all jobs were geometry optimizations
