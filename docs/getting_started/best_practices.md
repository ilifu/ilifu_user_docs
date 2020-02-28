# Best Practices

Please take note of the following best practices while using the ILIFU cloud computing services.

1. The head node must only be used for submitting jobs to SLURM.
2. Do not store large files in your $HOME directory
3. The /scratch mount is for data processing only. Files must be removed from your /scratch folder once data processing is complete.
4. Help the SLURM job scheduler by accurately identifying your job's resource requirements.
5. Help the SLURM job scheduler by accurately determining you job's wall-time.
6. Use job arrays where possible.
7. Use Singularity containers on shared storage for your software.

## Do not run software on the SLURM head node.

When you ssh into the SLURM cluster you will be on the SLURM head node. The purpose of the head node is to manage job submissions. Please do not run any software on the SLURM head node as this can reduce performance of the SLURM service and affect performance for other users. 

To submit jobs to the SLURM job queue use either [srun](https://docs.ilifu.ac.za/#/tech_docs/running_jobs?id=_3-interactive-sessions) or [sbatch](https://docs.ilifu.ac.za/#/tech_docs/running_jobs?id=_2-slurm-batch-scheduler) commands, or use the [srun](https://docs.ilifu.ac.za/#/tech_docs/running_jobs?id=_3-interactive-sessions) command to allocate a worker node for an interactive session.

## Do not store large files in your home directory

Your home directory is located at `/users/`. This directory is part of a mount that is only 20 TB which is shared between all users. Do not store large files or data in your home directory. Your home directory is for small files and scripts only. Filling up the `/users/` mount can prevent jobs from running and may prevent users accessing the cluster. Please see information on the ilifu [directory structure](https://docs.ilifu.ac.za/#/data/directory_structure).

## Do not leave files in your /scratch folder

The `/scratch` mount is used for data processing. Files should only be in your `/scratch/users` folder while you are processing data. Once you have finished processing data on the `/scratch` mount, please remove files that you do not need, and move files that you wish to keep to your relevant project folder.

## Identify the minimum resources that are required for your job

The SLURM resource pool consists of a finite number of CPUs and memory. Please make sure to use the minimum resources required to run your task or job. This will ensure that more resources are available for yourself and other users at any given time. The `sbatch` and `srun` commands can be used to customise the number of resources used when submitting a job. You may have to experiment with the number of resource you allocate to a job to gain insight into the minimum resources required.

## Identify the minimum wall-time that is required for your job

When submitting a job, the default wall-time is set to 3 days. It is important to assign a wall-time for your job that is accurate to the length of time you expect your job to run. Setting an accurate wall-time will improve the performance of the cluster scheduler and will reduce overall wait time for jobs. Wall-time for a job can be set using the `-t` parameter (units in minutes or hours:minutes:seconds or days-hours:minutes:seconds).

## When submitting multiples of the same job, consider using a SLURM job array

A SLURM job array is useful if you are submitting multiple jobs at a time and the initial input for each job is the same, or can be indexed in some manner (such as a series of files like file_001, file_002, etc). Using an sbatch script, the `#SBATCH --array 0-100%10` parameter can be used. This creates an array of 100 jobs and submits the jobs in batches of 10. The environmental variable `{SLURM_ARRAY_TASK_ID}` can be used as an index in your script to differentiate between job inputs.

The main benefit of using a job array is that once resources have been allocated to the job array the resources will remain dedicated until all the jobs are complete. This will remove the overhead of waiting in the SLURM queue for resources.

## You cannot install software on the nodes

As ILIFU users, for the sake of data security, you do not have root access on any of the available nodes. This means that you are unable to install software on the nodes. Available software packages are encapulated in Singularity containers located in `/data/exp_soft/containers` and `/cbio/images`. The software containers allow for the software to be available across all nodes, rather than having to install software on individual nodes.  Additional information about the containers and how to use them can be found [here](https://docs.ilifu.ac.za/#/tech_docs/software_environments?id=singularity-containers) and the lists of the included software packages in the supported containers can be found [here](https://docs.ilifu.ac.za/#/tech_docs/software_environments?id=available-containers). You are also able to [create custom Singularity containers](https://docs.ilifu.ac.za/#/tech_docs/software_environments?id=building-your-own-container) and migrate them to the ILIFU cluster for use, and many of the supported projects have their own specialised containers.
