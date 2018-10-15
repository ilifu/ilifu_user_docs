# Submitting jobs to be run on the Ilifu cluster

There are several methods to run jobs on Ilifu.

1. Users may get access to a Jupyter Lab spawner mechanism on the cluster. This provides a Jupyter lab environment where users select what size compute node they need to run. This is a good environment for users to experiment with code and visualise certain results. This environment will be made available at [jupyter.ilifu.ac.za](https://jupyter.ilifu.ac.za)

2. Users can login to the SLURM headnode at and submit tasks to the SLURM queue. This environment will be made available at [batch.ilifu.ac.za](https://batch.ilifu.ac.za).

3. Selected users will be given access to the OpenStack dashboard in order to have full control over the setup of a computing environment. This is available at [dashboard.ilifu.ac.za](https://dashboard.ilifu.ac.za)

## Jupyter Spawner

## Slurm Batch Scheduler

Slurm is a general purpose job scheduling system which is highly versatile.  There are numerous resources available online as to how to submit batch systems.  The simplest procedure for submitting and running a SLURM batch job is as is detailed below.

We will create a python script for each job, say `casa_job_N.py`, where N represents the job number.  We could ordinarily run this script using `casa -c casa_job_N.py`, but since our script will be run on a worker node, we use a singularity container to execute the script.  The simplest way to do this is by using the `singularity exec` command:

	singularity exec /data/exp_soft/containers/casa-stable.img casa -c casa_job_N.py

To execute our set of scripts using the SLURM batch scheduler, you must create a SLURM submit script. This bash script contains our casa command along with a set of parameters to instruct SLURM how to run the jobs:

	#!/bin/bash
	#file: casaslurm_N.sh:
	#SBATCH --job-name='casa-job-%J'
	#SBATCH --ntasks=1
	#SBATCH --time=00:20:00
	#SBATCH --output=logs/casalog_%J.log

	echo "Submitting SLURM job"
	singularity exec /data/exp_soft/containers/casa-stable.img casa -c casa_job_N.py 
	sleep 10

The commented lines beginning with _#SBATCH_ are parsed by the SLURM to determine how to run the jobs.  The above script creates a log file for each job, these scripts are located in the 'logs' directory, so make sure that such a directory exists relative to the location where you submit the script. 

To submit this script to the job queue, run 

	sbatch casaslurm_N.sh

To check the progress of the jobs, use the `squeue` command or check the `logs` directory...


## Openstack Cloud Dashboard
