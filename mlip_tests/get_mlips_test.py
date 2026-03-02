from jobflow_remote.jobs.jobcontroller import JobController
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]

jc = JobController.from_project_name("autoplex_project")

database_ids = [
    db_id
    for f in jc.get_flows_info()
    for db_id in f.db_ids
]
# print(len(database_ids))
# print(jc.get_job_info(db_id=database_ids[0]))

ml_fit_job_db_ids=[]
output_directories=[]

for db_id in database_ids:
    info = jc.get_job_info(db_id=str(db_id))
    name = re.search(r"name='([^']+)'", str(info)).group(1)
    state = str(info.state)
    if name=="machine_learning_fit" and state=='JobState.COMPLETED':
        run_dir = re.search(r"run_dir='([^']+)'", str(info)).group(1)
        output_directories.append(run_dir)
        ml_fit_job_db_ids.append(db_id)

print(len(ml_fit_job_db_ids)==25)

for i,run_dir in enumerate(output_directories[:4]):
    #Path(str(i+1)).mkdir(parents=True, exist_ok=True)
    print(run_dir)