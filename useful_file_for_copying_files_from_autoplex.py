#use jf remote to find output directories and then copy and rename
from jobflow_remote.jobs.jobcontroller import JobController
import re
import json

PBE_encut_666=[get_job_output_dirs(i) for i in range(1968,1995)]
RSCAN_encut_666=[get_job_output_dirs(i) for i in range(1995,2022)]
PBE_1100_kpoints=[get_job_output_dirs(i) for i in range(2022,2037)]
RSCAN_1100_kpoints=[get_job_output_dirs(i) for i in range(2037,2052)]

lst1=[PBE_encut_666,RSCAN_encut_666,PBE_1100_kpoints,RSCAN_1100_kpoints]


def get_job_output_dirs(db_id):
    jc = JobController.from_project_name("autoplex_project")
    doc=jc.get_jobs_info(db_ids=[str(db_id)])
    match = re.search(r"run_dir='([^']+)'", str(doc[0]))
    if match:
        run_dir = match.group(1)
        return f'{run_dir}/remote_job_data.json'


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


print(dict.keys())

#!/usr/bin/env python3
import shutil
from pathlib import Path

# <-- EDIT this mapping: keys are the new names, values are the source directories
mapping=dict

DEST_ROOT = Path("/u/vld/sedm7085/project/convergence_tests/castep_data")  # <-- destination root
DEST_ROOT.mkdir(parents=True, exist_ok=True)

# If True, overwrite any existing destination directory with the same name.
OVERWRITE = False

for name, src in mapping.items():
    srcp = Path(src)
    dst = DEST_ROOT / name

    if not srcp.is_dir():
        print(f"SKIP {name}: source not found or not a dir -> {src}")
        continue

    if dst.exists():
        if OVERWRITE:
            shutil.rmtree(dst)
        else:
            print(f"SKIP {name}: destination exists -> {dst}")
            continue

    shutil.copytree(srcp, dst)
    print(f" COPIED {srcp} -> {dst}")
