# Submitting jobs to be run on the ilifu cluster

The Ilifu facility has two main services for accessing compute resources:

1. **Jupyter** Users may access a JupyterLab session on the cluster. The Ilifu Jupyter service allows users to select their desired compute resources and dynamically spawn a Jupyter session. This is a good environment to experiment with code and visualise results. This Jupyter service is available at [jupyter.ilifu.ac.za](https://jupyter.ilifu.ac.za)

2. Users may access the Ilifu Slurm cluster login-node and submit tasks to the Slurm queue. This environment is available at [slurm.ilifu.ac.za](https://slurm.ilifu.ac.za).

---

## Jupyter Spawner

The Jupyter spawner can be accessed via web browser at `https://jupyter.ilifu.ac.za`. This system allows the user to spawn a virtual machine on the Ilifu cloud running Jupyter Lab. Since the VM is launched for each user it allows for better management of resources, and provides a reliable environment for developing and running analyses, since users are not competing for resources on one or more shared nodes.

After logging into the Jupyter node, the user is presented with a drop-down menu with a list of options for compute resources. Please select the smallest node that will provide sufficient resources for the task at hand:
![dropdown](http://docs.ilifu.ac.za/_media/profile_dropdown_options.png)

Each node will be terminated after a preset interval of time, however the user's jupyter environment is saved in their home directory, so when a new jupyter server is spawned their workspace and notebooks will be recreated. Some data is also persisted in the notebook file, however any long-running processes will be terminated when the jupyter session is stopped, or when it reaches its time limit. The Jupyter service is designed for interactive development and analysis, not for high performance computing. For long running or resource heavy tasks, please refer to the Slurm Batch Scheduler section below). A user can terminate the Jupyter session in order to free up resources on the cloud, or to choose a different node type. This is done by choosing `File > Hub Control Panel` option from the top menu bar of JupyterLab,

<img src="/_media/hub_selection.png" alt="menu bar options" width=500 />

This will bring you to the page with the `Stop My Server` option, where you can stop your current session, freeing up the resources that have been allocated to your Jupyter session. You are also able to use this process to change the size of the resources allocated to you. Once you have stopped your session you are able to choose a smaller or larger node size.

<img src="/_media/stop_server_button.png" alt="stop server button" width=600 />

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

Slurm is a general purpose job scheduling system which is highly versatile. There are numerous resources available online as to how to submit batch jobs and how to control the execution, concurrency, and dependencies of jobs. This page provides instructions for connecting to the batch scheduler and a simple example to submit and run a Slurm batch job.

The Slurm batch system can be accessed via `ssh` with private key to `slurm.ilifu.ac.za`. Note that this node should only be used to submit and manage batch jobs and not for running code or software directly. The login node does not have significant resources and will likely crash under heavy usage. From this node you can submit jobs to a queue where it is subsequently allocated to the computing cluster such that it uses resources in an optimal manner.

To do so, we must create a job submit script. In this example, we will assume that the user is executing their analysis or data processing code using python. We also assume that your code is contained in a set of python script called `casa_job_N.py`, where N represents the job number. If you were working directly on your laptop, you could run this script by running `python -c casa_job_N.py`. However, since our script will be run on a worker node, we need to use a singularity container to encapsulate our system environment and requisite software. To execute our python script on the Ilifu cluster using a singularity container, we prepend `singularity exec` to this command:

```bash
singularity exec /data/exp_soft/containers/casa-stable.img python -c casa_job_N.py
```

To execute our (set of) scripts using the Slurm batch scheduler, you must create an additional Slurm submit script. This is a bash script that contains the above command, along with a set of parameters that instruct Slurm how to run the jobs:

```bash
#!/bin/bash
#file: casaslurm_N.sh:
#SBATCH --job-name='casa-job-%J'
#SBATCH --ntasks=1
#SBATCH --time=00:20:00
#SBATCH --output=logs/casalog_%J.log

echo "Submitting Slurm job"
singularity exec /data/exp_soft/containers/casa-stable.img casa -c casa_job_N.py
sleep 10
```

The commented lines beginning with _#SBATCH_ are parsed by the Slurm to determine how to run the jobs. The above script creates a log file for each job, these scripts are located in the 'logs' directory, so make sure that such a directory exists relative to the location where you submit the script.

To submit this script to the job queue, run

```bash
sbatch casaslurm_N.sh
```

To check the progress of the jobs, use the `squeue` command or check the `logs` directory.

## Interactive Slurm Sessions

An interactive session allows you to connect to a computing node and work on that node directly. There are several ways to use an interactive session on Ilifu. If you need to do work that you would normally do on a dedicated node, without waiting in the queue, the simplest option is to use the `sinteractive` command. To use `sinteractive`, please see the Interactive Session Quick Start section below. 

For more sophisticated interactive usage, the `srun` command accommodates a variety of modes and options. See the Interactive Session Features section below for common features of the `srun` command.

Please note the following before starting an interactive job:

**Note:** Interactive sessions may be lost if you lose connection to the ilifu cluster. Persistent terminals, such as `tmux` or GNU `screen` can help to reduce volatility. See the section Persistent Terminals for instructions. 

**Note:** In order is to ensure that resources are available in an optimal way for all users, interactive jobs are limited by time and compute resources. For work that uses significant compute resources, or that takes longer than three hours, we recommend that users submit jobs to the batch queue using `sbatch`. 

**Note:** No software should be run on the Slurm login node (slurm.ilifu.ac.za). It should only be used to start, stop and monitor Slurm jobs. 

### Interactive Session Quick Start

If you need to do interactive work and don't want to wait in the queue, the `sinteractive` command aims to provide on-demand access to resources on the `Devel` partition. This partition is designed to elimiate wait time by sharing resources between mulitple users. The `sinteractive` is a wrapper around the `srun` command that allows you to quickly start a job on the `Devel` partition, connect to the appropriate server, and work on that server directly with minimal configuration. 

For example, run the following command on the login node to start an interactive session with four cores and X11 support:

```bash
	$ sinteractive --x11 -c 4
```

After entering this command, you will be presented with a new prompt on a compute node where you can work directly.

Most options that can be used with `sbatch` or `srun` can also be passed to the `sinteractive` command. We recommend specifying the flags for the number of CPUs (`-c` or `--cpus-per-core`) and for job time (`--time=`). The default time limit for the Devel partition is three hours. The job will only remain active until the terminal is exited. Therefore, it is recommended to use `sinteractive` together with a persistent connection tool such as `tmux` or `GNU screen`. See the Persistent Terminals section below for instructions.

In order to minimize wait time for interactive sessions, resources on the `Devel` partition are shared between all users -- memory is not tracked by Slurm and the cpus are oversubscribed. Also, job time is limited to a maximum of twelve hours. Please only request the number of cores and time that you need for the task at hand and be aware of your memory usage. If you need an interactive job with additional features and options, with a dedicated allocation of compute resources, or that lasts longer than twelve hours, please use `srun` command, which is documented in the following section. 

### Interactive Session Features

If you need an interative session with more time, resouces or options, the `srun` command can be used. From the Slurm login node, run the command:

```bash
	$ srun --pty bash
```

This will place you in an interactive (bash) shell on a compute node in the Main partition. The `--pty` parameter provides a psuedo-terminal that allows for interactivity. The default resources allocated by the `srun` command are 1 task, 1 CPU and ~7 GB RAM. Run the `srun --help` command to see additional parameters. Similar parameters to the sbatch command can be used to define the resources and other options of your interactive session. From the shell session, you are able to run interactive tasks, such as opening a Singularity container to load an interactive CASA session, or to utilizing Nextflow.

To start an interactive session without waiting in the queue, the `Devel` partition can be used for an on-demand session on a resource-shared node.

```bash
	$ srun -p Devel --pty bash -i
```

Note that, as memory is not tracked in the `Devel` partition, specifying any memory argument (e.g. the -m or --mem flags) with the `Devel` partition will yeild an error stating that "Memory required by task is not available".

You can directly run a Singularity containers or other software using the srun command, for example:

```bash
	$ srun --pty singularity shell /idia/software/containers/ASTRO-PY3.simg
```

This will start an interactive session on a compute node and open a shell in the `ASTRO-PY3` container, which contains a large suite of astronomy software. 

Alternatively, the following command will open an interactive CASA session on a compute node using the casa-stable.img container:

```bash
	$ srun --pty singularity exec /idia/software/containers/casa-stable.img casa --log2term --nologger
```

Incidently, you can submit non-interactive jobs to Slurm using the `srun` command without the `--pty` parameter, for example:

```bash
	$ srun singularity exec /idia/software/containers/ASTRO-PY3.simg python myscript.py
```

This will run the Python script `myscript.py` using the ASTRO-PY3 container on a compute node, similar to the `sbatch` command, however the job will not be run in the background, but will utilize your current terminal.

**Note:** Interactive sessions using `srun` make use of the same resource pool as jobs submitted using `sbatch`. If you are experiencing delays acquiring an interactive session you can either try to reduce the number of resources (CPU, memory and run-time) that you are requesting, or use the parameter `--qos qos-interactive` when launching your interactive job. This parameter provides increased priority but is limited to 1 job, 4 CPUs and 28 GB memory. Alternatively, you can use the `Devel` partition (`srun -p Devel`) or the `sinteractive` command for on-demand access to a shared node.

### Persistent Terminals

As with any ssh connection, when using an interactive shell via the `srun` or `sinteractive` command, your session is vulnerable to being killed if you lose network connectivity. To avoid this, you can use a persistent terminal tool such as GNU's `screen` or `tmux` for an interactive session that can be reaccessed after the loss of the ssh session. In order to use this feature, `tmux` should be run from the login node before running `srun`. However, when using `tmux`, please make sure to exit the `tmux` session once your interactive session is complete in order to release the resources back to the Slurm pool. Basic `tmux` commands include:

| Syntax/keyboard shortcut               | Action                                    |
|----------------------------------------|-------------------------------------------|
| tmux                                   | start new tmux session                    |
| tmux ls                                | list currently active tmux sessions       |
| tmux attach -t &#60;session_name&#62;  | attach to an active tmux session          |
| ctrl/cmd-b + d                         | detach from current tmux session          |
| ctrl/cmd-b + [                         | scroll current terminal                   |

An example work flow for an interactive session can be described as follows:
* login in to Slurm login node
* run tmux (or screen)
* use the srun or sinteractive command to allocate yourself a compute node, describing your required resources
* open a Singularity container and run your software.

Note: In the rare occasion that the Slurm login node is restarted, even persistent terminal sessions will be lost.

### Interactive Session with X11 Support

In the event that you wish to use software that provides a GUI, such as `CASA plotms`, you can start an interactive session with `X11 forwarding`. You must `ssh` into the Slurm login node with the `-Y` parameter, which sets your DISPLAY variable for trusted `X11 forwarding`, for example:

```bash
	$ ssh -Y <username>@slurm.ilifu.ac.za
```

From there, you must use `--x11` to allocate a Slurm compute node to yourself with `X11 forwarding` as follows:

```bash
	$ sinteractive --x11
```

or,

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

## Specifying Resources when Running Jobs on SLURM

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





