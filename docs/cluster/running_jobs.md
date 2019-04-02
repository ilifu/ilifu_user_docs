# Submitting jobs to be run on the Ilifu cluster

There are several methods to run jobs on Ilifu.

1. Users may get access to a Jupyter Lab spawner mechanism on the cluster. This provides a Jupyter lab environment where users select what size compute node they need to run. This is a good environment for users to experiment with code and visualise certain results. This environment will be made available at [jupyter.ilifu.ac.za](https://jupyter.ilifu.ac.za)

2. Users can login to the SLURM headnode at and submit tasks to the SLURM queue. This environment will be made available at [slurm.ilifu.ac.za](https://slurm.ilifu.ac.za).

3. Selected users will be given access to the OpenStack dashboard in order to have full control over the setup of a computing environment. This is available at [dashboard.ilifu.ac.za](https://dashboard.ilifu.ac.za)

---

## 1. Jupyter Spawner

The jupyter spawner can be accessed via web browser at `https://jupyter.ilifu.ac.za`.  This system allows the user to spawn a virtual machine on the Ilifu cloud running Jupyter Lab. Since the VM is launched for each user it allows for better management of resources, and provides a reliable environment for developing and running analyses, since users are not competing for resources on one or more shared nodes.

After logging in to the jupyter node, one must select the type of node on which to run jupyter.  The user is presented with a drop-down list with various options, and should choose the smallest node that will provide sufficient resources for the task at hand:
![dropdown](http://docs.ilifu.ac.za/_media/profile_dropdown_options.png)

Each node will be terminated after a preset interval of time, however the user's jupyter environment is saved in their home directory, so when a new jupyter server is spawned the workspace is recreated. Some data is also persisted in the notebook file. A user can terminate the server in order to free up resources on the cloud, or to choose a different node type.  This is done by choosing the 'hub' option from the top menu bar of JupyterLab,

<img src="http://docs.ilifu.ac.za/_media/hub_selection.png" alt="menu bar options" width=500 />

Choose the 'control panel' option to view or stop your server,

<img src="http://docs.ilifu.ac.za/_media/stop_server_button.png" alt="stop server button" width=600 />

## 2. Slurm Batch Scheduler

Slurm is a general purpose job scheduling system which is highly versatile.  There are numerous resources available online as to how to submit batch jobs and how to control the execution, concurrency, and dependencies of jobs.  This page provides instructions for connecting to the batch scheduler and a simple example to submit and run a SLURM batch job.

The SLURM batch system can be accessed via `ssh` with private key to `slurm.ilifu.ac.za`. Note that this node should only be used to submit and manage batch jobs and not for running code or software directly.  This node does not have significant resources and will likely crash under heavy usage.  From this node you can submit jobs to a queue where it subsequently allocated to the computing cluster such that it uses resources in an optimal manner.

To do so, we must create a submit script.  In this example we will assume that the user is executing their analysis or data processing code using python.  We thus create a python script for each compute job called `casa_job_N.py`, where N represents the job number.  If you were working directly on your laptop you could run this script by running `python -c casa_job_N.py`.  However, since our script will be run on a worker node, we use a singularity container to encapsulate our environment and requisite software.  The simplest way to execute our python script is by prepending the `singularity exec` command:

```console
singularity exec /data/exp_soft/containers/casa-stable.img python -c casa_job_N.py
```

To execute our (set of) scripts using the SLURM batch scheduler, you must create an additional SLURM submit script. This is a bash script that contains the above command, along with a set of parameters that instruct SLURM how to run the jobs:

```bash
#!/bin/bash
#file: casaslurm_N.sh:
#SBATCH --job-name='casa-job-%J'
#SBATCH --ntasks=1
#SBATCH --time=00:20:00
#SBATCH --output=logs/casalog_%J.log

echo "Submitting SLURM job"
singularity exec /data/exp_soft/containers/casa-stable.img casa -c casa_job_N.py
sleep 10
```

The commented lines beginning with _#SBATCH_ are parsed by the SLURM to determine how to run the jobs.  The above script creates a log file for each job, these scripts are located in the 'logs' directory, so make sure that such a directory exists relative to the location where you submit the script.

To submit this script to the job queue, run

```console
sbatch casaslurm_N.sh
```

To check the progress of the jobs, use the `squeue` command or check the `logs` directory...

## 3. Interactive Sessions

No software or process should be run on the slurm headnode. For an interative session on the slurm cluster, without the use of a Jupyter notebook, the `srun` command can be used as follows:

```console
srun -N 1 --pty bash
```

This will allocate a number of compute nodes specified by the `-N` parameter, and will ssh you into one of the allocated worker nodes. A bash terminal session will be loaded from where you are able to run interactive tasks, such as opening a Singularity container and loading an interactive CASA session or utilizing Nextflow.

For an interactive session with X11 forwarding, in the event you wish to use CASA tasks with their GUIs, you must `ssh` into slurm with the `-XY` parameters which sets your DISPLAY variable for X11 forwarding, for example:

```console
ssh -XY <username>@slurm.ilifu.ac.za
```

From there, you can use `salloc` to allocate a slurm worker node to yourself, or you can use the above `srun` command to allocate a slurm worker node. In both cases, you can check the name of the worker node that has been allocated to you by running:

```console
squeue
```

Once you have deteremined the correct name of the worker node, you must ssh into the worker node with the `-XY` parameters, for example:

```console
ssh -XY slwrk-020
```

You are then able to run a Singularity container and run an interactive CASA session with access to the GUIs. The `casa-stable` and `casameer` Singularity container images contain the X11 tools required for X11 forwarding.

Please exit the worker node once you have finished the interactive session in order to return the resources to the slurm pool.

## 4. Openstack Cloud Dashboard

The Openstack dashboard is available for certain users at [dashboard.ilifu.ac.za](https://dashboard.ilifu.ac.za) which provides a cloud computing environment, allowing users or groups to create, modify, and remove virtual machines or even entire computing clusters.

<img src="http://docs.ilifu.ac.za/_media/dashboard_view.png" alt="openstack dashboard" width=600 />
