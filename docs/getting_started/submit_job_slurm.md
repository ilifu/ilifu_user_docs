# Submitting a job on Slurm

Two common ways to run jobs on Slurm include submitting jobs using a batch script, and running jobs interactively. Submitting jobs using a batch script allows for multiple jobs to be submitted in parallel, or for a series of jobs to be submitted, where one job may depend on the output of a previous job. Interactive jobs are useful for developing workflows or scripts, debugging errors, or working with software interactively. **Note that batch jobs are greatly preferred over interactive jobs,** as they don't require to be run in realtime or interaction with the user. Batch jobs are queued and are run when resources are available. Interactive jobs are inherently wasteful, as resources are often idle while waiting for user input. While we do understand the need to interactive sessions, **please submit jobs using batch jobs whenever possible**.

**Note: No software should be run on the Slurm login node.** The login node (slurm.ilifu.ac.za) should only be used to start and interact with Slurm jobs, or other low-resource tasks. For any other work, please start an interactive job as described below. 

## Submitting a job using a batch script

After sshing into `slurm.ilifu.ac.za`, you can submit a job to Slurm using a job submission script, or shell script. The script must describe the application or software you wish to run as well as the resources that you wish to allocate to the job.

Let us run a simple Python program, submitted to Slurm as a batch job. Create a python script, `myscript.py`, with the following contents:
```python
import time
print('Hello world')
time.sleep(20)
```

Create a shell script, `my_slurm_script.sh` with the following contents:
```bash
#!/bin/bash

module add python/3.11.2
python myscript.py
```

This is about the simplest script you can create to submit a batch job. The `#!` is called the hashbang or shebang and is used to indicate the shell interpreter that will be used to run the script, in this case `/bin/bash`. The second line, `module add python/3.11.2` is an instruction to load the Python 3.11.2 software module, which can be used to manage which version of Python is available in the job environment. Finally, the application and script that will be run by the job will be `python` and the script `myscript.py`.

You can now submit the job to the Slurm queue by running the `sbatch` command, followed by the job submission script:
```bash
	$ sbatch my_slurm_script.sh
```

If the requested resources are available the job will be initiated. To see the status of the jobs in the Slurm queue associated with your account run:
```bash
	$ squeue -u $USER
```

You can see the status of all jobs in the Slurm queue by using the command:
```bash
	$ squeue
```

**Note that, as we didn't specified any resources in the job submission script, the default resources will be used to run the job.** The defaults for a Slurm job are `1 CPU`, `3GB RAM`, a time limit of `3 hours`, and the job will be run on the `Main` partition. You can view the partition defaults, as well as the available resources and limits in the [Specifying resources for Slurm jobs](tech_docs/running_jobs?id=specifying-resources-when-running-jobs-on-slurm) section.

Let's now improve our job submission script by specifying some useful parameters. We may find that the default resources are not sufficient to run our job (for example, a 3 hours time limit may result in our job timing out), but in this case, the defaults are actually excessive for our test job, so lets be considerate and specify only the necessary resources required to run our small script. Update the `my_slurm_script.sh` to the following:

```bash
#!/bin/bash

#SBATCH --job-name='testjob'
#SBATCH --cpus-per-task=1
#SBATCH --mem=1GB
#SBATCH --time=00:05:00
#SBATCH --output=testjob-%j-stdout.log
#SBATCH --error=testjob-%j-stderr.log

echo "Submitting Slurm job"
singularity exec /idia/software/containers/ASTRO-PY3.simg python myscript.py
```

The parameters that follow `#SBATCH` indicate the requested resources and other job parameters, such as the job name and logging information. It's helpful to name your job, using a description of the software or process, so that you can refer back to the name when debugging or reviewing past jobs. In the script, we've also now defined the number of CPU (cores), amount of memory and the time limit for the job, using the appropriate parameters. We've also defined the log output for the job, both the standard output (what you would generally see written out to the terminal when running the commands in the script) as well as the error output. The `%j` in the output log file names is a placeholder for the job number or `jobid`. Run the `sbatch --help` command from the terminal to see additional parameters or see the table in the [Customising your job using sbatch/srun parameters](tech_docs/running_jobs?id=customising-your-job-using-sbatchsrun-parameters) section for more details. Very useful parameters to set are the `--mail-user` and `--mail-type` which you can use to receive email notifications on your job status, including if the job fails, completes or is at 80% of the allocated walltime.

In the shell script above, the other change that we have made is which Python binary we want use to run the `myscript.py`. Instead of using the Python software module as we did before, we've opted to use a `Singularity` container, called `ASTRO-PY3.simg`. This container includes a suite of astronomy related Python packages, and while not necessary to run the small script, it's a useful demonstration for an alternative to software modules. We've also included the `echo` command, the output of which will be written to the log file defined by `--output`. This is sometimes useful for debugging, but is also just a demonstration that you can run more than a single line in the job submission script.

Now that the new parameters have been configured, submit the job to Slurm again:
```bash
	$ sbatch my_slurm_script.sh
```

You can again see your job in the Slurm queue while it is queued or executing by running:
```bash
	$ squeue -u $USER
```
If any errors occur during the execution of the job, you can view the logs in the `testjob-<jobid>-stderr.log`, and any text output can be found in `testjob-<jobid>-stdout.log`, as described by the shell script. This is useful for debugging any issues with your job. You should see the output of the `echo` command and the output of the Python script in your log file.

## Interactive Slurm sessions

An interactive session allows you to connect to a computing node and work on that node directly. There are several ways to use an interactive session on Ilifu. If you need to do work that you would normally do on a dedicated node, without waiting in the queue, the simplest option is to use the `sinteractive` command. To use `sinteractive`, please see the [Interactive Session Quick Start](getting_started/submit_job_slurm?id=interactive-session-quick-start) section below. 

For more sophisticated interactive usage, the `srun` command accommodates a variety of modes and options. See the [Interactive Session Features](getting_started/submit_job_slurm?id=interactive-session-features) section below for common features of the `srun` command.

Please note the following before starting an interactive job:

**Note:** Interactive sessions may be lost if you lose connection to the ilifu cluster. Persistent terminals, such as `tmux` or GNU `screen` can help to reduce volatility. See the section [Persistent Terminals](getting_started/submit_job_slurm?id=persistent-terminals) for instructions. 

**Note:** In order is to ensure that resources are available in an optimal way for all users, interactive jobs are limited by time and compute resources. For work that uses significant compute resources, or that takes longer than three hours, we recommend that users submit jobs to the batch queue using `sbatch`. 

**Note:** No software should be run on the Slurm login node (slurm.ilifu.ac.za). The Slurm login node should only be used to start, stop and monitor Slurm jobs. 

### Interactive session quick start

If you need to do interactive work and don't want to wait in the queue, the `sinteractive` command aims to provide on-demand access to resources on the `Devel` partition. This partition is designed to elimiate wait time by sharing resources between mulitple users. The `sinteractive` command is a wrapper around the `srun` command that allows you to quickly start a job on the `Devel` partition, connect to the appropriate server, and work on that server directly with minimal configuration. By default, running `sinteractive` will allocate 1 CPU for 3 hours:
```bash
	$ sinteractive
```
Additional CPU cores can be assigned, and `X11` can also be used. For example, run the following command on the login node to start an interactive session with four cores and `X11` support:
```bash
	$ sinteractive --x11 -c 4
```

After entering this command, you will be presented with a new prompt on a compute node where you can work directly.

Most options that can be used with `sbatch` or `srun` can also be passed to the `sinteractive` command. We recommend specifying the flags for the number of CPUs (`-c` or `--cpus-per-task`) and for job time (`-t` or `--time`). The job will only remain active while the terminal connection is maintained. Therefore, it is recommended to use `sinteractive` together with a persistent connection tool such as `tmux` or `GNU screen`. See the [Persistent Terminals](getting_started/submit_job_slurm?id=persistent-terminals) section below for instructions.

In order to minimize wait time for interactive sessions, resources on the `Devel` partition are shared between all users -- memory is not tracked by Slurm and the CPUs are oversubscribed. Please only request the number of cores and time that you need for the task at hand and be aware of your memory usage. If you need an interactive job with additional features and options, with a dedicated allocation of compute resources, please use `srun` command, which is documented in the following section. 

### Interactive session features

If you need an interative session with more time and dedicated resources, the `srun` command can be used. The difference between `srun` & `sinteractive` is that with `srun`, by default, the session will run on the `Main` partition and the resources allocated to the session will not be shared with other users, however, the session may be queued if the requested resources are not available.

You can start a simple interactive session from the Slurm login node as follows:
```bash
	$ srun --pty bash
```

This will place you in an interactive (`bash`) shell on a compute node in the `Main` partition. The `--pty` parameter provides a psuedo-terminal that allows for interactivity. The default resources allocated by the `srun` command are `1 task`, `1 CPU` and `3GB RAM`. Run the `srun --help` command to see additional parameters. Similar parameters to the `sbatch` command can be used to define the resources and other options of your interactive session. From the shell session, you are able to run interactive tasks, such as opening a Singularity container to load an interactive CASA session, or to utilizing Nextflow.

To start an interactive session without waiting in the queue, the `Devel` partition can be used for an on-demand session on a resource-shared node.

```bash
	$ srun -p Devel --pty bash
```

Note that, as memory is not tracked in the `Devel` partition, specifying any memory argument (e.g. the `-m` or `--mem` flags) with the `Devel` partition will yield an error stating that "Memory required by task is not available".

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

This will run the Python script `myscript.py` using the ASTRO-PY3 container on a compute node, similar to the `sbatch` command, however the job will not be run in the background, but will utilise your current terminal.

**Note:** Interactive sessions using `srun` make use of the same resource pool as jobs submitted using `sbatch`. If you are experiencing delays acquiring an interactive session you can either try to reduce the number of resources (CPU, memory and run-time) that you are requesting, or use the parameter `--qos qos-interactive` when launching your interactive job. This parameter provides increased priority but is limited to 1 job, 4 CPUs and 28 GB memory. Alternatively, you can use the `Devel` partition (`srun -p Devel`) or the `sinteractive` command for on-demand access to a shared node.

### Persistent terminals

As with any `SSH` connection, when using an interactive shell via the `srun` or `sinteractive` command, your session is vulnerable to being killed if you lose network connectivity. To avoid this, you can use a persistent terminal tool such as GNU's `screen` or `tmux` for an interactive session that can be reaccessed after the loss of the `SSH` session. In order to use this feature, `tmux` should be run from the login node before running `srun`. However, when using `tmux`, please make sure to exit the `tmux` session once your interactive session is complete in order to release the resources back to the Slurm pool. Basic `tmux` commands include:

| Syntax/keyboard shortcut               | Action                                    |
|----------------------------------------|-------------------------------------------|
| tmux                                   | start new tmux session                    |
| tmux ls                                | list currently active tmux sessions       |
| tmux attach -t &#60;session_name&#62;  | attach to an active tmux session          |
| ctrl/cmd-b + d                         | detach from current tmux session          |
| ctrl/cmd-b + [                         | scroll current terminal                   |

An example work flow for an interactive session can be described as follows:
* login in to Slurm login node
* run `tmux` (or `screen`)
* use the `srun` or `sinteractive` command to allocate yourself a compute node, describing your required resources
* open a Singularity container and run your software.

Note: In the rare occasion that the Slurm login node is restarted, even persistent terminal sessions will be lost.


### Interactive session with X11 support

In the event that you wish to use software that provides a GUI, such as `CASA plotms`, you can start an interactive session with `X11 forwarding`. You must `ssh` into the Slurm login node with the `-Y` parameter, which sets your `DISPLAY` variable for trusted `X11 forwarding`, for example:

```bash
	$ ssh -Y <username>@slurm.ilifu.ac.za
```

From there, you must use `--x11` to allocate a Slurm compute node to yourself with `X11 forwarding` as follows:

```bash
	$ sinteractive --x11
```

or:

```bash
	$ srun --x11 --pty bash
```

This will place you in an interactive shell (`bash`) session on a compute node with `X11 forwarding` enabled. The default resources allocated by the `srun` command are `1 task`, `1 CPU` and `3GB RAM`. You can again adjust what resources are allocated to your interactive session using the parameters such as `--cpus-per-task`, or `--mem`, for example:

```bash
	$ srun --cpus-per-task=2 --mem=8GB --x11 --pty bash
```

You are then able to run a Singularity container and run software that provides a GUI. Note the GUIs over `SSH` are notoriously slow, so always try and interact with software using a input parameters or a parameter file, rather than a GUI, where possible.

## Useful Slurm monitoring commands

There are a number of Slurm commands that are useful for finding out information about the current state of the cluster or the status of queued or running jobs, as well as commands that can be used to review past jobs.

The table below provides a summary of these commands and indicates at which stage of a job the commands are useful.

| Slurm Commands | Before Running a Job | Starting a New Job | Monitoring a Running Job | After Jobs have Completed |
|----------------|----------------------|--------------------|--------------------------|---------------------------|
| sinfo          | X                    |                    |                          |                           |
| squeue         | X                    |                    | X                        |                           |
| sbatch         |                      | X                  |                          |                           |
| srun           |                      | X                  |                          |                           |
| scontrol       |                      |                    | X                        |                           |
| sacct          |                      |                    |                          | X                         |

To view the different Slurm partitions (also known as queues) and to get an indication of how busy the cluster is, run the [sinfo](https://slurm.schedmd.com/sinfo.html) command:
```bash
	$ sinfo
	PARTITION  AVAIL  TIMELIMIT  NODES  STATE NODELIST
	Main*         up 14-00:00:0      1   resv compute-020
	Main*         up 14-00:00:0     25    mix compute-[002,004,101-105,210-211,216-219,223-225,227,233,250-256]
	Main*         up 14-00:00:0     56  alloc compute-[003,005-019,021-022,201-209,212-215,220-222,226,228-232,234-249]
	Jupyter       up   infinite      1   resv compute-020
	Jupyter       up   infinite      7    mix jupyter-[002-003,005-007,010,012]
	Jupyter       up   infinite      6  alloc jupyter-[004,008-009,011,013-014]
	JupyterGPU    up 14-00:00:0      2    mix gpu-[003-004]
	JupyterDev    up   infinite      1  alloc jupyter-001
	HighMem       up 14-00:00:0      2    mix highmem-[002-003]
	HighMem       up 14-00:00:0      3  alloc highmem-[001,004-005]
	HighMem       up 14-00:00:0      3   idle highmem-[006-008]
	GPU           up 14-00:00:0      6    mix gpu-[001-006]
	GPU           up 14-00:00:0      2   idle gpu-007,highmem-008
	Devel         up 5-00:00:00      1  alloc compute-001
```
The number of nodes and state information are helpful indicators of how busy the cluster is for the different partitions. The `alloc` state indicates that all the resources (CPU cores and RAM) on these nodes are allocated to jobs, the `mix` state means that a portion of resources on these nodes are allocated to jobs, while some resources are free, and the `idle` nodes have no resources currently allocated to running jobs, and are available. The `resv` state indicates the node(s) is reserved for a particular purpose and are not available for use by the general user group.

While your job is queued or running, you can check on its status using `squeue` or `scontrol`. We've already covered `squeue` above, but there are additional parameters and customisations that are useful, for example listing the expected start time of your jobs. More information on [squeue](https://slurm.schedmd.com/squeue.html) can be found in the Slurm documentation.

[scontrol](https://slurm.schedmd.com/scontrol.html) can be used to look at individual jobs in more detail. You can use `squeue` to determine the relevant `jobid` and then use the following command to view detailed information for that job:
```bash
	$ scontrol show j <jobid>
```
This will show all the information associated with the job, including the job parameters you set, as well as the defaults that were used for parameters that you did not set. You can review a jobs timelimit this way and check if a long running jobs is at risk of timing out or not. **Note this command is only valid for pending or running jobs.**

Finally, you can view previously run jobs using [sacct](https://slurm.schedmd.com/sacct.html). This is helpful, for example, to find out what the error state was for a job that failed, or to find out how much CPU, RAM, or walltime resources a job used, so that you can more accurately allocate resources to similar jobs in the future. See the [Resource Allocation guide](tech_docs/resource_allocation) for more detailed information on determining what resources to allocate to jobs.

By default `sacct` will list information about the jobs that you ran since the start of the current day:
```bash
	$  sacct
```
If you know the jobid of the job you're interested in, you can do:
```bash
	$ sacct -j <jobid>
```
Otherwise, you can list all the jobs for your user after a certain date, or between dates using `--startime` and `--endtime`:
```bash
	$ sacct --starttime 2025-05-04 --endtime 2025-05-11
```
You can specify the information you want to view about the jobs using `-o` or `--format`. Have a look at all the possible column using:
```bash
	$ sacct -e
```
An example of some useful jobs information might be (modify the date ranges to be more sensible!):
```bash
sacct --starttime 2025-05-04 --endtime 2025-05-11 --format=JobID,Jobname,partition,state,start,end,time,elapsed,ReqMem,MaxRss,MaxVMSize,nnode,ncpus,nodelist
```
How much difference was there between the requested time and runtime of the job? How much memory was used versus what was requests?

## Further Slurm and job resources

When running a job using `sbatch` or `srun`, a user should specify the resources required for their job. See the [Available Resources](tech_docs/running_jobs?id=available-resources) section for more information about the different partitions and node sizes and specialised resources (high memory and GPU), as well as different defaults and limits.

Additional details on `sbatch` and `srun` parameter customisation can be found in the [Customising your job using sbatch/srun parameters](tech_docs/running_jobs?id=customising-your-job-using-sbatchsrun-parameters) section.

For making use of parallelism on the cluster, i.e. more than one CPU core or multiple nodes, the software being run must support `MPI` or `OpenMP`. See the [Parallel computing on the cluster](tech_docs/running_jobs?id=parallel-computing-on-the-cluster) for more information.

For making use of GPU resources see the [Notes for GPU jobs](tech_docs/running_jobs?id=notes-for-gpu-jobs).