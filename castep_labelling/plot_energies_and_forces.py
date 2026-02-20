import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
from jobflow_remote.jobs.jobcontroller import JobController
import re,json
from datetime import datetime
from datetime import datetime
import numpy as np
from pathlib import Path
import gzip
from ase.io import read
from quippy.potential import Potential
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", module="ase.calculators.castep")
warnings.filterwarnings("ignore", module="ase.io.castep")

PROJECT_ROOT = Path(__file__).resolve().parents[0]

def time_diff(t1: str, t2: str, unit: str = "seconds") -> float:
    delta = datetime.fromisoformat(t2) - datetime.fromisoformat(t1)
    seconds = delta.total_seconds()

    if unit == "seconds":
        return seconds
    elif unit == "minutes":
        return seconds / 60
    elif unit == "hours":
        return seconds / 3600
    else:
        raise ValueError("unit must be 'seconds', 'minutes', or 'hours'")

jc = JobController.from_project_name("autoplex_project")
database_ids = [f.db_ids for f in jc.get_flows_info()]

num_completed=0
run_time=[]
completed=[]
jc.get_jobs_info(db_ids=database_ids[-1])
for id in database_ids[-1]:
    if str(jc.get_job_info(db_id=id).state)=="JobState.COMPLETED":
        num_completed+=1
        run_time.append(time_diff(
            str(jc.get_job_info(db_id=id).start_time),
            str(jc.get_job_info(db_id=id).end_time),
            unit="hours"))
        completed.append(id)

print(num_completed)
print(np.mean(run_time))


unit = "\u00C5"
print(unit)
energy=[]
forces=[]
quip_energy=[]
quip_forces=[]
structures=[]
for id in completed:
    run_dir=jc.get_job_info(db_id=id).run_dir
    file=f'{run_dir}/remote_job_data.json'
    with open(file,'r') as f:
        data=json.load(f)
        energy.append(data[0]['output']['output']["energy_per_atom"])
        forces.append(data[0]['output']['output']["forces"])
        #print(energy) N
        #print(forces) Nx192x3
    structure=f'{run_dir}/CASTEP/castep.cell.gz'
    with gzip.open(structure, "rt") as f:
        xml_path = Path(PROJECT_ROOT) / "gap_file.xml"
        gap = Potential(args_str="IP GAP", param_filename=str(xml_path))#correct quip code
        atoms=read(structure)
        atoms.calc = gap
        quip_energy.append(atoms.get_total_energy()/192.0)
        quip_forces.append(atoms.get_forces())

# print(energy,quip_energy)
# print(forces[0][0],quip_forces[0][0])
# print(forces[:6],quip_forces[:6])
forces=np.array(forces).ravel()
quip_forces=np.array(quip_forces).ravel()
energy=np.array(energy)
quip_energy=np.array(quip_energy)

rmse_energy = np.sqrt(np.mean((quip_energy - energy)**2))
rmse_forces = np.sqrt(np.mean((quip_forces - forces)**2))

fig, ax = plt.subplots()
ax.scatter(energy, quip_energy, s=10, marker='x')
ax.plot([min(energy),max(energy)],[min(energy),max(energy)], "k--")
ax.set_xlabel("DFT energy / eV")
ax.set_ylabel("Predicted energy / eV")
fig.tight_layout()
fig.savefig(f"{PROJECT_ROOT}/images/energy_plot_new.png")

fig, ax = plt.subplots()
ax.scatter(forces, quip_forces, s=10, marker='x')
ax.plot([min(forces),max(forces)],[min(forces),max(forces)], "k--")
ax.set_xlabel(f"DFT forces / eV/{unit}")
ax.set_ylabel(f"Predicted forces / eV/{unit}")
fig.tight_layout()
fig.savefig(f"{PROJECT_ROOT}/images/forces_plot_new.png")

print(f"RMSE = {rmse_energy*1000} meV")
print(f"RMSE = {rmse_forces*1000} meV/{unit}")