# Submitting a job on SLURM

Two common ways to run jobs on SLURM include submitting jobs using a batch script, and running jobs interactively. Submitting jobs using a batch script allows for multiple jobs to be submitted in parallel, or for a series of jobs to be submitted, where one job may depend on the output of a previous job. Interactive jobs are useful for developing workflows or scripts, or working with software interactively. **Please note that no software should be run on the SLURM login node (login node).**

## Submitting a Job using a Batch Script

After `sshing` into `slurm.ilifu.ac.za`, you can submit a job to SLURM using a shell script. The script must describe the application/software you wish to run as well as the resources that you wish to allocate to the job.

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

echo "Submitting SLURM job"
singularity exec /idia/software/containers/ASTRO-PY3.simg python myscript.py
```

The parameters that follow `#SBATCH` indicate the requested resources and other job parameters such as the job name and logging information. The `%j` in the output log file names is a placeholder for the job number or `jobid`. Run the  `sbatch --help` command from the terminal to see additional parameters or see the [table of parameters below](/getting_started/submit_job_slurm?id=slurm-job-parameters).

In the shell script above, the application you wish to run during the job is described by `singularity exec /data/exp_soft/containers/ASTRO-PY3.simg python myscript.py`. Here `python` is being used to run `myscript.py` using the python executable within the container `ASTRO-PY3.simg`. This is a `singularity` container that is called with the `exec` command to execute the script.

The next step is to run the shell script using the SLURM `sbatch` command:

```bash
	$ sbatch my_slurm_script.sh
```

This will submit the job to the SLURM queue. If the requested resources are available the job will be initiated. You can see the status of all jobs in the SLURM queue by using the command:

```bash
	$ squeue
```

To see the status of the jobs in the SLURM queue associated with your account use:

```bash
	$ squeue -u <username>
```

If any errors occur while running the job, you can view the logs in the `testjob-<jobid>-stderr.log`, and any text output can be found in `testjob-<jobid>-stdout.log`, as described by the shell script. This is useful for debugging any issues with your job.

## Interactive SLURM Sessions

**No software should be run on the SLURM login node.** A shell terminal can be run on a compute node allowing for an interactive job on the cluster. Interactive jobs are useful for testing and developing code.

**NOTE:** interactive sessions are volatile and may be lost if you lose connection to the ilifu cluster. Persistent terminals, such as `tmux` or `screen` may help to reduce this volatility, however, in the event that the SLURM login node is restarted, the persistent terminal sessions will be lost. We therefore recommend that users submit jobs using `sbatch`, particularly for jobs with run times of greater than 3 hrs.

**NOTE:** interactive sessions make use of the same resource pool as jobs submitted using `sbatch`. If you are experiencing delays acquiring an interactive session you can either try to reduce the number of resources (CPU, memory and run-time) that you are requesting, or use the parameter `--qos qos-interactive` when launching your interactive job. This parameter provides increased priority but is limited to 1 job, 4 CPUs and 28 GB memory.

### Quick Interactive Session

If you need to do interactive work and don't want to wait in the queue, the `sinteractive` command provides on-demand access to an allocation of resources in the `Devel` partition. It is designed to elimiate wait time by sharing resources between mulitple users. The `sinteractive` command can often be used in cases where a dedicated server would otherwise be used. That is, when testing scripts, developing code, compiling, or for other tasks that are difficult to accomplish with a batch queue system and which cannot be done on the login node.

The following command will launch a job in the `Devel` partition with four cores, X11 support, and will automatically open a virtual terminal (`--pty` by default) on the appropriate node:

```bash
	$ sinteractive --x11 -c 4
```

Most options that can be used with `sbatch` or `srun` can also be passed to the `sinteractive` command. We recommend specifying the flags for CPU (`-c` or `--cpus-per-core`) and for time (`--time=`), if you need more than the default time limit of three hours. The job will only remain active until the terminal is exited. Therefore, it is recommended to use `sinteractive` together with a tool such as `tmux` or `GNU screen` in order to maintain a persistent connection. See the instructions for `tmux` in the following section.

In order to provide immediate access for interactive tasks, resources are shared between all users on the `Devel` partition -- memory is not tracked and the CPUs are oversubscribed. Please only request the number of cores that you need for the task at hand and be aware of your memory usage. 

For more features of interactive jobs, refer to the following sections. 


### Interactive Session without X11 Support

For an interative session on the SLURM cluster the `srun` command can be used. The difference between `srun` & `sinteractive` is that with `srun`, by default, the session will run on the `Main` partition and the resources allocated to the session will not be shared with other users, however, the session may be queued if the requested resources are not available.

You can start a simple interactive session from the SLURM login node as follows:

```bash
	$ srun --pty bash
```

This will place you in an interactive shell (bash) session on a compute node. The `--pty` parameter provides a psuedo-terminal which allows interactivity. The default resources allocated by the `srun` command are 1 task, 1 CPU and ~7 GB RAM. Run the `srun --help` command to see additional parameters. Similar parameters to the sbatch script above can be used to define the resources allocated to your interactive session. From the shell session, you are able to run interactive tasks, such as opening a Singularity container and loading an interactive CASA session, or utilizing Nextflow.

You are able to directly run Singularity containers or software within containers using the srun command, for example:

```bash
	$ srun --pty singularity shell /idia/software/containers/ASTRO-PY3.simg
```

This will open an interactive session on a compute node and open the `ASTRO-PY3` container which includes a large suite of astronomy software. Alternatively, the following command will open an interactive CASA session on a compute node using the casa-stable.img container:

```bash
	$ srun --pty singularity exec /idia/software/containers/casa-stable.img casa --log2term --nologger
```

Incidently, you can also submit non-interactive jobs to SLURM using the `srun` command without the `--pty` parameter, for example:

```bash
	$ srun singularity exec /idia/software/containers/ASTRO-PY3.simg python myscript.py
```

This will run the Python script `myscript.py` using the ASTRO-PY3 container on a compute node, similar to the `sbatch` command, however the job will not be run in the background, but will utilize your current terminal.

Note that when using an interactive shell on SLURM by using the `srun` command, your interactive session may be vulnerable to being killed if you lose network connectivity. To avoid this, you can use `tmux` for a persistent terminal that can be reaccessed after the loss of the ssh session. In order to use this feature, `tmux` should be run from the login node before running `srun`. However, when using `tmux`, please make sure to exit the `tmux` session once your interactive session is complete in order to release the resources back to the SLURM pool. Basic `tmux` commands include:

| Syntax/keyboard shortcut               | Action                                    |
|----------------------------------------|-------------------------------------------|
| tmux                                   | start new tmux session                    |
| tmux ls                                | list currently active tmux sessions       |
| tmux attach -t &#60;session_name&#62;  | attach to an active tmux session          |
| ctrl/cmd-b + d                         | detach from current tmux session          |
| ctrl/cmd-b + [                         | scroll current terminal                   |

An example work flow for an interactive session can be described as follows:
* login in to slurm login node
* run tmux (or screen)
* use the srun command to allocate yourself a compute node, describing your required resources
* open a Singularity container and run your software.

### Interactive Session with X11 Support

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
	$ srun --pty --cpus-per-task=2 --mem=16GB --x11 bash
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

| Syntax                                       | Meaning                                        |
|----------------------------------------------|------------------------------------------------|
| --time=&#60;minutes&#62;                     | Walltime for job (default is 3 hrs)            |
| --mem=&#60;number&#62;*                      | Maximum amount of memory (default is ~7 GB)    |
| --mem-per-cpu=&#60;number&#62;*              | Memory per processor core (CPU)                |
| --cpus-per-task=&#60;number&#62;             | Number of CPUs per task (default is 1)         |
| --ntasks=&#60;number&#62;                    | Number of processes to run (default is 1)      |
| --nodes=&#60;number&#62;                     | Number of nodes on which to run (default is 1) |
| --ntasks-per-node=&#60;number&#62;           | Number of tasks to invoke on each node         |
| --partition=&#60;partition_name&#62;         | Request specific partition/queue               |
| --account=&#60;account_name&#62;<sup>7</sup> | The account that will be charged for the job   |

**Note** default units for memory is MB, but can be specified explicitly in GB, example `--mem=16GB`.

* a nodes refer to a single compute node or SLURM worker, i.e. one node has 32 CPUs and 232 GB RAM
* a task is an instance of a running program, generally you will only want one task, unless you use software with MPI support (for example CASA), SLURM works with MPI to manage parallelised processing of data.
* CPUs refers to the the number of CPUs associated with your job.
* default parameters, if not specified, include: 1 node; 1 task; 1 CPU and ~7 GB RAM (7424 MB or 7.25 GB); running on the Main partition for 3 hrs.
* to find your default account you can run the command `sacctmgr show User -p | grep ${USER}`, while the command `sacctmgr show Associations User=${USER} cluster=ilifu-slurm2021 -p | cut -f 2 --d="|"` will show all your valid accounts. Note that it is only important that you set the account parameter if you are associated with more than one project on the cluster. You can change your default account using `sacctmgr modify user name=${USER} set DefaultAccount=<account>`, where `<account>` is one of your valid accounts.
* for more information, see [advanced usage](tech_docs/running_jobs#_4-specifying-resources-when-running-jobs-on-slurm)

### Notes for GPU jobs.

If you wish to run a job on the GPU node you need to specify the `GPU` partition, i.e. your sbatch script will have something like the following lines in the header:
<!-- and you need to specify the number of GPU resources you require with the `--gres` option.
```code bash
#SBATCH --partition=GPU
#SBATCH --gres=gpu:p100:1
``` -->
```code bash
#SBATCH --partition=GPU
```

<!-- Note that the 3 GPU nodes only have 2 GPUs each, so you must use either `--gres=gpu:p100:1` or `--gres=gpu:p100:2`. -->

