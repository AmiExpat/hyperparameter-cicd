# kubernetes/generate_jobs.py
import os
import yaml
from itertools import product

# Define hyperparameter ranges
param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [3, 5],
    'learning_rate': [0.1, 0.01],
    'subsample': [0.8, 1.0]
}

# Load job template
with open('kubernetes/job-template.yaml', 'r') as file:
    job_template = yaml.safe_load(file)

# Generate combinations
combinations = list(product(
    param_grid['n_estimators'],
    param_grid['max_depth'],
    param_grid['learning_rate'],
    param_grid['subsample']
))

# Generate job files
for idx, (n_estimators, max_depth, learning_rate, subsample) in enumerate(combinations):
    job = job_template.copy()
    job_id = f"{idx}"
    job['metadata']['name'] = job['metadata']['name'].replace('{{JOB_ID}}', job_id)
    container = job['spec']['template']['spec']['containers'][0]
    for env_var in container['env']:
        if env_var['name'] == 'N_ESTIMATORS':
            env_var['value'] = str(n_estimators)
        elif env_var['name'] == 'MAX_DEPTH':
            env_var['value'] = str(max_depth)
        elif env_var['name'] == 'LEARNING_RATE':
            env_var['value'] = str(learning_rate)
        elif env_var['name'] == 'SUBSAMPLE':
            env_var['value'] = str(subsample)

    # Save the job file
    job_filename = f'kubernetes/job_{job_id}.yaml'
    with open(job_filename, 'w') as outfile:
        yaml.dump(job, outfile)

    print(f"Generated {job_filename} with parameters:")
    print(f"  n_estimators: {n_estimators}")
    print(f"  max_depth: {max_depth}")
    print(f"  learning_rate: {learning_rate}")
    print(f"  subsample: {subsample}")
