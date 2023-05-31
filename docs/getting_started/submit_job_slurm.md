# Submitting a job on Slurm

Two common ways to run jobs on Slurm include submitting jobs using a batch script, and running jobs interactively. Submitting jobs using a batch script allows for multiple jobs to be submitted in parallel, or for a series of jobs to be submitted, where one job may depend on the output of a previous job. Interactive jobs are useful for developing workflows or scripts, or working with software interactively. 

**Note: No software should be run on the Slurm login node.** The login node (slurm.ilifu.ac.za) should only be used to start and interact with Slurm jobs, or other low-resource tasks. For any other work, please start an interactive job as described below. 

## Submitting a Job using a Batch Script

After `sshing` into `slurm.ilifu.ac.za`, you can submit a job to Slurm using a shell script. The script must describe the application/software you wish to run as well as the resources that you wish to allocate to the job.

Let us assume that you are trying to run a python script, `myscript.py` with the following contents:

```python
import time
print('Hello world')
time.sleep(20)
```

Create a shell script, `my_slurm_script.sh` with the following:

```bash
#!/bin/bash

#SBATCH --job-name='testjob'
#SBATCH --cpus-per-task=2
#SBATCH --mem=16GB
#SBATCH --output=testjob-%j-stdout.log
#SBATCH --error=testjob-%j-stderr.log
#SBATCH --time=00:05:00

echo "Submitting Slurm job"
singularity exec /idia/software/containers/ASTRO-PY3.simg python myscript.py
```

The parameters that follow `#SBATCH` indicate the requested resources and other job parameters such as the job name and logging information. The `%j` in the output log file names is a placeholder for the job number or `jobid`. Run the `sbatch --help` command from the terminal to see additional parameters or see the [table of parameters below](/getting_started/submit_job_slurm?id=slurm-job-parameters).

In the shell script above, the application you wish to run during the job is described by `singularity exec /data/exp_soft/containers/ASTRO-PY3.simg python myscript.py`. Here `python` is being used to run `myscript.py` using the python executable within the container `ASTRO-PY3.simg`. This is a `singularity` container that is called with the `exec` command to execute the script.

The next step is to run the shell script using the Slurm `sbatch` command:

```bash
	$ sbatch my_slurm_script.sh
```

This will submit the job to the Slurm queue. If the requested resources are available the job will be initiated. You can see the status of all jobs in the Slurm queue by using the command:

```bash
	$ squeue
```

To see the status of the jobs in the Slurm queue associated with your account use:

```bash
	$ squeue -u <username>
```

If any errors occur while running the job, you can view the logs in the `testjob-<jobid>-stderr.log`, and any text output can be found in `testjob-<jobid>-stdout.log`, as described by the shell script. This is useful for debugging any issues with your job.

## Interactive Slurm Sessions

An interactive session allows you to connect to a computing node and work on that node directly. There are several ways to use an interactive session on Ilifu. If you need to do work that you would normally do on a dedicated node, without waiting in the queue, the simplest option is to use the `sinteractive` command. To use `sinteractive`, please see the Interactive Session Quick Start section below. 

For more sophisticated interactive usage, the `srun` command accommodates a variety of modes and options. See the Interactive Session Features section below for common features of the `srun` command.

Please note the following before starting an interactive job:

**Note:** Interactive sessions may be lost if you lose connection to the ilifu cluster. Persistent terminals, such as `tmux` or GNU `screen` can help to reduce volatility. See the section Persistent Terminals for instructions. 

**Note:** In order is to ensure that resources are available in an optimal way for all users, interactive jobs are limited by time and compute resources. For work that uses significant compute resources, or that takes longer than three hours, we recommend that users submit jobs to the batch queue using `sbatch`. 

**Note:** No software should be run on the Slurm login node (slurm.ilifu.ac.za). The Slurm login node should only be used to start, stop and monitor Slurm jobs. 

### Interactive Session Quick Start

If you need to do interactive work and don't want to wait in the queue, the `sinteractive` command aims to provide on-demand access to resources on the `Devel` partition. This partition is designed to elimiate wait time by sharing resources between mulitple users. The `sinteractive` is a wrapper around the `srun` command that allows you to quickly start a job on the `Devel` partition, connect to the appropriate server, and work on that server directly with minimal configuration. 

For example, run the following command on the login node to start an interactive session with four cores and X11 support:

```bash
	$ sinteractive --x11 -c 4
```

After entering this command, you will be presented with a new prompt on a compute node where you can work directly.

Most options that can be used with `sbatch` or `srun` can also be passed to the `sinteractive` command. We recommend specifying the flags for the number of CPUs (`-c` or `--cpus-per-core`) and for job time (`--time=`). The default time limit for the `Devel` partition is three hours. The job will only remain active until the terminal is exited. Therefore, it is recommended to use `sinteractive` together with a persistent connection tool such as `tmux` or `GNU screen`. See the Persistent Terminals section below for instructions.

In order to minimize wait time for interactive sessions, resources on the `Devel` partition are shared between all users -- memory is not tracked by Slurm and the CPUs are oversubscribed. Also, job time is limited to a maximum of twelve hours. Please only request the number of cores and time that you need for the task at hand and be aware of your memory usage. If you need an interactive job with additional features and options, with a dedicated allocation of compute resources, or that lasts longer than twelve hours, please use `srun` command, which is documented in the following section. 

### Interactive Session Features

If you need an interative session with more time and dedicated resources, the `srun` command can be used. The difference between `srun` & `sinteractive` is that with `srun`, by default, the session will run on the `Main` partition and the resources allocated to the session will not be shared with other users, however, the session may be queued if the requested resources are not available.

You can start a simple interactive session from the Slurm login node as follows:

```bash
	$ srun --pty bash
```

This will place you in an interactive (bash) shell on a compute node in the `Main` partition. The `--pty` parameter provides a psuedo-terminal that allows for interactivity. The default resources allocated by the `srun` command are 1 task, 1 CPU and ~7 GB RAM. Run the `srun --help` command to see additional parameters. Similar parameters to the sbatch command can be used to define the resources and other options of your interactive session. From the shell session, you are able to run interactive tasks, such as opening a Singularity container to load an interactive CASA session, or to utilizing Nextflow.

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

## Specifying Resources when Running Jobs on Slurm

### Available resources

When running a job using `sbatch` or `srun`, a user is able to specify the resources required for their job. The following table lists the different node sizes in the cluster and indicates the maximum number of resources that can be requested for the different node types.

| Partition | Node names        | Default CPUs| Max CPUs| Default Memory (GiB) | Max Memory (GiB) | Default wall-time | Max wall-time |
|-----------|-------------------|-------------|---------|----------------------|------------------|-------------------|---------------|
| Main      | compute-[002-021] | 1           | 32      | 3                    | 232              | 3 hours           | 14 days       |
| Main      | compute-[101-105] | 1           | 48      | 3                    | 232              | 3 hours           | 14 days       |
| Main      | compute-[201-260] | 1           | 32      | 3                    | 251              | 3 hours           | 14 days       |
| HighMem   | highmem-[001-002] | 1           | 32      | 15                   | 503              | 3 hours           | 14 days       |
| HighMem   | highmem-003       | 1           | 96      | 15                   | 1508             | 3 hours           | 14 days       |
| GPU       | gpu-[001-004]     | 1           | 32      | 7                    | 232              | 3 hours           | 14 days       |
| GPU       | gpu-005           | 1           | 24      | 7                    | 232              | 3 hours           | 14 days       |
| GPU       | gpu-006           | 1           | 48      | 7                    | 354              | 3 hours           | 14 days       |
| GPU       | gpu-007           | 1           | 48      | 7                    | 354              | 3 hours           | 14 days       |
| Devel     | compute-001       | 1           | 32      | -                    | -                | 3 hours           | 12 hours      |

*Note jobs submitted to the Devel partition cannot allocate memory.*

The GPU nodes include NVIDIA P100 (gpu-[001-004]), V100 (gpu-005), A40 (gpu-006) and A100 (gpu-007). To submit a job on a specific GPU node, the `-w` or `--nodelist` parameter may be used, with a list of the relevant `Node names`. Alternatively, the `-C` or `--constraint` parameter may be used, with the list of constraints or tags, as indicated in the table below:

| Partition | Node names        | GPU type    | Constraint/Tag | Number of GPUs per node | GPU Memory (GiB) |
|-----------|-------------------|-------------|----------------|-------------------------|------------------|
| GPU       | gpu-[001-004]     | P100        | P100,p100      | 2                       | 12               |
| GPU       | gpu-005           | V100        | V100,v100      | 1                       | 32               |
| GPU       | gpu-006           | A40         | A40,a40        | 1                       | 45               |
| GPU       | gpu-007           | A100        | A100,a100      | 1                       | 40               |

### Parallel computing on the cluster

If you are running a normal job on Slurm, **without** `MPI` or `OpenMP`, your job will only require `1 CPU`, `1 task` and `1 node`. These values are default values when running a job, however you are able to specify additional memory for your job using the `--mem` parameter.

Parallelism on the cluster can be achieved on a single node or over multiple nodes. Parallelism on a single node distributes work over multiple CPUs and is typically implemented using `OpenMP`. If you are running a job with software that utilizes `OpenMP` on Slurm, you can increase the number of CPUs for your job to > 1 CPU, while still using `1 task` and `1 node`. You may need to `export OMP_NUM_THREADS=<N>` to specify the number of threads the software will utilize.

Parallelism on the cluster can also occur by distributing work over many tasks that operate on 1 or more nodes. This type of parallelism is typically implemented using `MPI`. If you are running a job with software that utilizes `MPI` on Slurm, you can increase the number of `tasks` your job uses, `> 1 task`, while `nodes` and `CPUs` can be 1. The number of CPUs per task can be specified. You can increase the number of nodes if you want more than `32 CPUs` or `232 GiB RAM`.

When using MPI, you must wrap your software call (including Singularity) in an MPI wrapper, such as mpirun, for example:

```bash
#!/bin/bash
#SBATCH --job-name='MPI-job-%J'
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1

module load openmpi/4.1.0
mpirun -n <number of processes to run> singularity exec <path/to/container> </path/to/binary/within/container>
```

It is important to note that when running jobs in parallel using a container, the container must also have `MPI` installed in it and the version and implementation inside the container must be the same as the version used on the cluster. Please keep this in mind if building a new container intended for parallel jobs, and select an `MPI` implemtation this is supported on ilifu. There are a number of versions of `openmpi` supported, as well as a single version of `mpich`. View available versions by running `module avail`.

### Customising your job using sbatch/srun parameters

The following table lists the parameters that can be used to describe the required resources for your job. Additional parameters can be found by running `sbatch --help` or `srun --help`.

| Syntax                                       | Meaning                                                               |
|----------------------------------------------|-----------------------------------------------------------------------|
| --time=&#60;minutes&#62;                     | Walltime for job (default is 3 hrs)                                   |
| --mem=&#60;number&#62;*                      | Maximum amount of memory                                              |
| --mem-per-cpu=&#60;number&#62;*              | Memory per processor core (CPU – default is 3 GiB on Main partition ) |
| --cpus-per-task=&#60;number&#62;             | Number of CPUs per task (default is 1)                                |
| --ntasks=&#60;number&#62;                    | Number of processes to run (default is 1)                             |
| --nodes=&#60;number&#62;                     | Number of nodes on which to run (default is 1)                        |
| --ntasks-per-node=&#60;number&#62;           | Number of tasks to invoke on each node                                |
| --partition=&#60;partition_name&#62;         | Request specific partition/queue                                      |
| --account=&#60;account_name&#62;<sup>7</sup> | The account that will be charged for the job                          |

**Note** default units for memory is MiB, but can be specified explicitly in GiB, example `--mem=16G`.

* a nodes refer to a single compute node or Slurm worker, i.e. one node has 32 CPUs and 232 GiB RAM
* a task is an instance of a running program, generally you will only want one task, unless you use software with MPI support (for example CASA), Slurm works with MPI to manage parallelised processing of data.
* CPUs refers to the the number of CPUs associated with your job.
* default parameters, if not specified, include: 1 node; 1 task; 1 CPU and 3 GiB RAM; running on the Main partition for 3 hrs.
* to find your default account you can run the command `sacctmgr show User -p | grep ${USER}`, while the command `sacctmgr show Associations User=${USER} cluster=ilifu-slurm2021 -p | cut -f 2 --d="|"` will show all your valid accounts. Note that it is only important that you set the account parameter if you are associated with more than one project on the cluster. You can change your default account using `sacctmgr modify user name=${USER} set DefaultAccount=<account>`, where `<account>` is one of your valid accounts.
* for more information, see [advanced usage](tech_docs/running_jobs?id=specifying-resources-when-running-jobs-on-slurm)

