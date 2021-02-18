# Submitting jobs to be run on the ilifu cluster

There are several methods to run jobs on Ilifu.

1. Users may access a JupyterLab environment on the cluster. This provides a JupyterLab environment where users select what size compute node they need to run. This is a good environment for users to experiment with code and visualise certain results. This environment is available at [jupyter.ilifu.ac.za](https://jupyter.ilifu.ac.za)

2. Users may access the Ilifu SLURM cluster login-node and submit tasks to the SLURM queue. This environment is available at [slurm.ilifu.ac.za](https://slurm.ilifu.ac.za).

---

## Jupyter Spawner

The jupyter spawner can be accessed via web browser at `https://jupyter.ilifu.ac.za`.  This system allows the user to spawn a virtual machine on the Ilifu cloud running Jupyter Lab. Since the VM is launched for each user it allows for better management of resources, and provides a reliable environment for developing and running analyses, since users are not competing for resources on one or more shared nodes.

After logging into the jupyter node, one must select the type of node on which to run jupyter.  The user is presented with a drop-down list with various options, and should choose the smallest node that will provide sufficient resources for the task at hand:
![dropdown](http://docs.ilifu.ac.za/_media/profile_dropdown_options.png)

Each node will be terminated after a preset interval of time, however the user's jupyter environment is saved in their home directory, so when a new jupyter server is spawned the workspace is recreated. Some data is also persisted in the notebook file. A user can terminate the server in order to free up resources on the cloud, or to choose a different node type.  This is done by choosing `File > Hub Control Panel` option from the top menu bar of JupyterLab,

<img src="http://docs.ilifu.ac.za/_media/hub_selection.png" alt="menu bar options" width=500 />

This will bring you to the page with the `Stop My Server` option, where you can stop your current session, freeing up the resources that have been allocated to your Jupyter session. You are also able to use this process to change the size of the resources allocated to you. Once you have stopped your session you are able to choose a smaller or larger node size.

<img src="http://docs.ilifu.ac.za/_media/stop_server_button.png" alt="stop server button" width=600 />

Once you have logged into JupyterLab and selected a node size you will be placed on the main launch page of your Jupyter session. On the left sidebar you will find a directory navigation panel. On the right of the screen you will find the launch panel which provides a list of kernels to choose from. The different kernels provide the software environment within which your Jupyter notebook is run.

There are kernels for both Python and R languages. The different kernels include different software stacks, such as the `CASA-#` kernels that contain Python wrapped CASA tasks which can be executed within the notebook, or the `ASTRO-PY3` kernel which contains an assortment of astronomy related software and Python packages. Once you have selected a kernel a notebook will be created. You can change the kernel from within the notebook by going `Kernel > Change Kernel...` from the top menu bar, or by clicking the kernel name on the top right side of the notebook panel, next to the kernel indicator circle.

The kernels themselves are in fact Singularity software containers. All the additional software packages installed in the container, beyond the Python packages, are also available to use from within the Jupyter notebook. You can make calls to these other software packages or to the underlying operating system by prefixing the relevant command with `!` in the Jupyter notebook, for example:

```
[ ]: !pwd
```
will provide you with the path of your current work directory.

The following table lists the available kernels and their related Singularity containers:

| Kernel name                 | Container                                 |
|-----------------------------|-------------------------------------------|
| ASTRO-PY3                   | ASTRO-PY3.simg                            |
| ASTRO-R                     | ASTRO-R.simg                              |
| CASA-5                      | jupyter-casa-latest.simg                  |
| CASA-6 Alpha                | casa-6-dev.simg                           |
| KERN-2                      | kern-2.img                                |
| KERN-5                      | kern5.simg                                |
| PY2                         | python-2.7.img                            |
| PY3                         | python-3.6.img                            |
| Python 3                    | System Python (not a container)           |
| SF-PY2                      | source-finding.img                        |
| SF-PY3                      | ASTRO-PY3.simg                            |

Details of the python libraries, software and other libraries available within the different containers can be found in the [Available containers](tech_docs/software_environments?id=available-containers) section. An alternative way to view the available Python packages included in the kernel is to run the command `!pip freeze` in your Jupyter notebook. This command will list all the python packages available in the currently active kernel. To create a custom kernel for use in your Jupyter session, see [Using a custom container as a Jupyter kernel](tech_docs/software_environments?id=using-a-custom-container-as-a-jupyter-kernel).

## Slurm Batch Scheduler

Slurm is a general purpose job scheduling system which is highly versatile.  There are numerous resources available online as to how to submit batch jobs and how to control the execution, concurrency, and dependencies of jobs.  This page provides instructions for connecting to the batch scheduler and a simple example to submit and run a SLURM batch job.

The SLURM batch system can be accessed via `ssh` with private key to `slurm.ilifu.ac.za`. Note that this node should only be used to submit and manage batch jobs and not for running code or software directly.  This node does not have significant resources and will likely crash under heavy usage.  From this node you can submit jobs to a queue where it subsequently allocated to the computing cluster such that it uses resources in an optimal manner.

To do so, we must create a submit script.  In this example we will assume that the user is executing their analysis or data processing code using python.  We thus create a python script for each compute job called `casa_job_N.py`, where N represents the job number.  If you were working directly on your laptop you could run this script by running `python -c casa_job_N.py`.  However, since our script will be run on a worker node, we use a singularity container to encapsulate our environment and requisite software.  The simplest way to execute our python script is by prepending the `singularity exec` command:

```bash
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

```bash
sbatch casaslurm_N.sh
```

To check the progress of the jobs, use the `squeue` command or check the `logs` directory...

## Interactive SLURM sessions

**No software should be run on the SLURM login node.** A shell terminal can be run on a compute node allowing for an interactive job on the cluster. Interactive jobs are useful for testing and developing code.

**NOTE:** interactive sessions are volatile and may be lost if you lose connection to the ilifu cluster. Persistent terminals, such as `tmux` or `screen` may help to reduce this volatility, however, in the event that the SLURM login node is restarted, the persistent terminal sessions will be lost. We therefore recommend that users submit jobs using `sbatch`, particularly for jobs with run times of greater than 3 hrs.

**NOTE:** interactive sessions make use of the same resource pool as jobs submitted using `sbatch`. If you are experiencing delays acquiring an interactive session you can either try to reduce the number of resources (CPU, memory and run-time) that you are requesting, or use the parameter `--qos qos-interactive` when launching your interactive job. This parameter provides increased priority but is limited to 1 job, 4 CPUs and 28 GB memory.

### Interactive session without X11 support

For an interative session on the SLURM cluster the `srun` command can be used as follows, from the SLURM login node:

```bash
	$ srun --pty bash
```

This will place you in an interactive shell (bash) session on a compute node. The `--pty` parameter provides a psuedo-terminal which allows interactivity. The default resources allocated by the `srun` command are 1 task, 1 CPU and 8 GB RAM. Run the `srun --help` command to see additional parameters. Similar parameters to the sbatch script above can be used to define the resources allocated to your interactive session. From the shell session, you are able to run interactive tasks, such as opening a Singularity container and loading an interactive CASA session, or utilizing Nextflow.

You are able to directly run Singularity containers or software within containers using the srun command, for example:

```bash
	$ srun --pty singularity shell /idia/software/containers/ASTRO-PY3.simg
```

This will open an interactive session on a compute node and open the ASTRO-PY3.simg container which includes a large suite of astronomy software. Alternatively, the following command will open an interactive CASA session on a compute node using the casa-stable.img container:

```bash
	$ srun --pty singularity exec /idia/software/containers/casa-stable.img casa --log2term --nologger
```

Incidently, you can also submit non-interactive jobs to SLURM using the `srun` command without the `--pty` parameter, for example:

```bash
	$ srun singularity exec /idia/software/containers/ASTRO-PY3.simg python myscript.py
```

This will run the Python script `myscript.py` using the `ASTRO-PY3` container on a compute node, similar to the `sbatch` command, however the job will not be run in the background, but will utilize your current terminal.

Note that when using an interactive shell on SLURM by using the `srun` command, your interactive session may be vulnerable to being killed if you lose network connectivity. To avoid this, you can use `tmux` for a persistent terminal that can be reaccessed after the loss of the ssh session. In order to use this feature, `tmux` should be run from the login node before running `srun`. However, when using `tmux`, please make sure to exit the `tmux` session once your interactive session is complete in order to release the resources back to the SLURM pool. Basic `tmux` commands include:

| Syntax/keyboard shortcut               | Action                                    |
|----------------------------------------|-------------------------------------------|
| tmux                                   | start new tmux session                    |
| tmux ls                                | list currently active tmux sessions       |
| tmux attach -t &#60;session_name&#62;| attach to an active tmux session          |
| ctrl/cmd-b + d                         | detach from current tmux session          |
| ctrl/cmd-b + [                         | scroll current terminal                   |

An example work flow for an interactive session can be described as follows:
* login in to slurm login node
* run tmux (or screen)
* use the srun command to allocate yourself a compute node, describing your required resources
* open a Singularity container and run your software.

### Interactive session with X11 support

In the event that you wish to use software which provides a GUI, such as `CASA plotms`, you can start an interactive session with `X11 forwarding`. You must `ssh` into the SLURM login node with the `-Y` parameter which sets your DISPLAY variable for trusted `X11 forwarding`, for example:

```bash
	$ ssh -Y <username>@slurm.ilifu.ac.za
```

From there, you must use `--x11` to allocate a SLURM worker node to yourself with `X11 forwarding` as follows:

```bash
	$ srun --x11 --pty bash
```

This will place you in an interactive shell (bash) session on a compute node with `X11 forwarding` enabled. The default resources allocated by the `srun` command are 1 task, 1 CPU and ~7 GB RAM. You can again adjust what resources are allocated to your interactive session using the parameters such as `--cpus-per-task`, or `--mem`, for example:

```bash
	$ srun --cpus-per-task=2 --mem=16GB --x11 --pty bash
```

You are then able to run a Singularity container and run software that provides a GUI.

<!--
### Interactive session with salloc

You can directly SSH onto a node to start an interactive session using `salloc`. You must `ssh` into the SLURM login node with the `-Y` parameter which sets your DISPLAY variable for trusted `X11 forwarding` and the `-A` parameter for authentication-forwarding to the SLURM login node, for example:

```bash
	$ ssh -YA <username>@slurm.ilifu.ac.za
```

From there, you must use `salloc` to allocate a SLURM worker node to yourself using the `--qos qos-interactive` parameter, as follows:

```bash
	$ salloc --qos qos-interactive
```

When attempting to run `salloc` for an interactive session, you may experience a **Permission denied (publickey)** error. This suggests that that authentication-forwarding is not working correctly. If this is the case, you may need to add your ssh key to your authentication profile on your personal computer. To do this, run the following command from the terminal (not logged onto ilifu), for Ubuntu/Linux operating systems:

```bash
	$ ssh-add -k
```

or for Mac OS:

```bash
	$ ssh-add -K
``` -->

## Specifying Resources when running jobs on SLURM

When running a job using an `sbatch` script or using `srun` for an interactive job, a user is able to specify the resources required for their job. A single node consists of `32 CPUs` and `232 GB RAM`. These are the maximum number of resources that can be requested per node.

If you are running a normal job on SLURM, **without** `MPI` or `OpenMP`, your job will only require `1 CPU`, `1 task` and `1 node`. These values are default values when running a job, however you are able to specify additional memory for your job using the `--mem` parameter.

Parallelism on the cluster can be achieved on a single node or over multiple nodes. Parallelism on a single node distributes work over multiple CPUs and is typically implemented using `OpenMP`. If you are running a job with software that utilizes `OpenMP` on SLURM, you can increase the number of CPUs for your job to > 1 CPU, while still using `1 task` and `1 node`. You may need to `export OMP_NUM_THREADS=<N>` to specify the number of threads the software will utilize.

Parallelism on the cluster can also occur by distributing work over many tasks that operate on 1 or more nodes. This type of parallelism is typically implemented using `MPI`. If you are running a job with software that utilizes `MPI` on SLURM, you can increase the number of `tasks` your job uses, `> 1 task`, while `nodes` and `CPUs` can be 1. The number of CPUs per task can be specified. You can increase the number of nodes if you want more than `32 CPUs` or `232 GB RAM`.

The following table lists the parameters that can be used to describe the required resources for your job:

<summary id='slurm-job-parameters'></summary>

| Syntax                                                                               | Meaning                                         			|
|--------------------------------------------------------------------------------------|----------------------------------------------------	|
| --time=&#60;minutes&#62;<sup>1</sup>                                                 | Walltime for job (default is 3 hrs)               	|
| --mem=&#60;number&#62;<sup>2,11</sup>                                                | Maximum amount of memory per node (default is ~7 GB)	|
| --mem-per-cpu=&#60;number&#62;<sup>2,3,11</sup>                                      | Memory per processor core (CPU)											|
| --cpus-per-task=&#60;number&#62;<sup>3,4,11</sup>                                    | Number of CPUs per task (default is 1)             	|
| --ntasks=&#60;number&#62;<sup>4</sup>                                                | Number of processes to run (default is 1)          	|
| --nodes=&#60;number&#62;<sup>5,11</sup>                                              | Number of nodes on which to run (default is 1)     	|
| --ntasks-per-node=&#60;number&#62;<sup>4,5</sup>                                     | Number of tasks to invoke on each node            		|
| --partition=&#60;partition_name&#62;<sup>6</sup>                                     | Request specific partition/queue (default Main)    	|
| --account=&#60;account_name&#62;<sup>7</sup>                                         | The account that will be charged for the job       	|
| --gres=&#60;resource_type&#62;:&#60;resource_name&#62;:&#60;number&#62;<sup>8</sup>  | Specify type and number of generic resources       	|
| --output=&#60;file_name&#62;<sup>9</sup>                                             | File to write standard output to                   	|
| --error=&#60;file_name&#62;<sup>9</sup>                                              | File to write standard error output to             	|
| --mail-user=&#60;email_address&#62;<sup>10</sup>                                     | email address where notifications should be sent   	|
| --mail-type=&#60;event_types&#62;<sup>10</sup>                                       | list of events that should send email notification 	|
<!-- also include row for array jobs -->

*default parameters, if not specified, include: 1 node; 1 task; 1 CPU and ~7 GB RAM (7424 MB or 7.25 GB); running on the Main partition for 3 hrs.*

1. While the default for specifying the wall-time for a job is in minutes, it can also be specified as `mm:ss`, `hh:mm:ss` and even `days-hh:mm:ss`. Wall-time is the estimated amount of time that you expect your job to run. It is important for the scheduler to know this parameter so that it can make realistic estimates on when jobs are due to start and end. This is especially critical for your short jobs as it can allow them to run earlier when a node would otherwise be idle waiting for a large job to start. Note, however, that underestimating wall-time means that once your job has exceeded its limit, it will be killed. So it’s better to slightly overestimate the amount of time, especially taking into account that the runtime of jobs can vary a bit due to overall system load.
2. The default units for memory is MB, but can be specified explicitly in GB, for example `--mem=16GB`. This parameter is especially important in jobs where you are not using the whole node, i.e. jobs using fewer than 32 cores, as this allows other jobs to run alongside yours and make more efficient use of the resources.
3. CPUs refers to the the number of CPUs associated with your job.
4. a task is an instance of a running program, and generally you will only want one task, unless you use software with MPI support (for example MPICASA), SLURM works with MPI to manage parallelised processing of data.
5. nodes refers to a single compute node or SLURM worker, i.e. one node that has 32 CPUs and 232 GB RAM
6. The partition is the specific part of the cluster your job will run. You will only set this if you are [running a GPU job](/getting_started/submit_job_slurm?id=notes-for-gpu-jobs).
7. To find your default account you can run the command `sacctmgr show User -p | grep ${USER}`, while the command `sacctmgr show Associations User=${USER} -p | cut -f 2 --d="|"` will show all your valid accounts. Note that it is only important that you set the account parameter if you are associated with more than one project on the cluster. You can change your default account using `sacctmgr modify user name=${USER} set DefaultAccount=<account>`, where `<account>` is one of your valid accounts.
8. Request generic resource (per node). You will only use this if you are [running a GPU job](/getting_started/submit_job_slurm?id=notes-for-gpu-jobs).
9. The filename can include `%j`, which will be substituted with the job's ID.
10. Email notifications can optionally be sent when a job's state changes. Create a comma-separated list with at least one of the following notification types: `NONE`; `BEGIN`; `END`; `FAIL`; `REQUEUE`; `ALL` (equivalent to `BEGIN,END,FAIL,REQUEUE,STAGE_OUT); STAGE_OUT`; `TIME_LIMIT`; `TIME_LIMIT_90` (reached 90 percent of time limit); `TIME_LIMIT_80` (reached 80 percent of time limit); `TIME_LIMIT_50` (reached 50 percent of time limit); and `ARRAY_TASKS`. ARRAY_TASKS will mean that a notification will be sent for each task in a job array (the default is only for the job array as a whole.)
11. **Note that if you specify more memory or cores than is available on the nodes, or more nodes than are available on the cluster, _your job will never start but it will sit in the queue!_**

## Understanding Priority and Fairshare
The slurm documentation [on priority](https://slurm.schedmd.com/priority_multifactor.html) and [fairshare](https://slurm.schedmd.com/fair_tree.html) is very extensive, what follows here is a short summary of what's going on and how to check what's going on with jobs on ilifu.

### Multifactor Priority
Our slurm is configured to use priority scheduling which uses a number of factors to determine a job's priority

### Fairshare
Blah