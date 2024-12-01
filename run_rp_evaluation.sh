#!/bin/bash
#SBATCH --job-name=main_job_0           # Job name
#SBATCH --time=12:00:00              # Maximum wall time (HH:MM:SS)
#SBATCH --ntasks=1                   # Number of tasks (1 task for main.py)
#SBATCH --cpus-per-task=4            # Number of CPUs per task (adjust as needed)
#SBATCH --mem=64G                     # Memory required (adjust as needed)
#SBATCH --account=chaijy2 # cse595s001f24_class

# Load Python environment (if using a module or virtualenv)
module load python/3.11.5           # Adjust the Python module version if necessary
source venv/bin/activate        # Activate virtualenv if needed (optional)

python role_play_eval.py --model 'llama_70b'