# Submitting a job on SLURM

Two common ways to run jobs on SLURM include submitting jobs using a batch script, and running jobs interactively. Submitting jobs using a batch script allows for multiple jobs to be submitted in parallel, or for a series of jobs to be submitted, where one job may depend on the output of a previous job. Interactive jobs are useful for developing workflows or scripts, or working with software interactively. **Please note that no software should be run on the SLURM head node (login node).**

## Submitting a job using a batch script

After `sshing` into `slurm.ilifu.ac.za`, you can submit a job to SLURM using a shell script. The script must describe the application/software you wish to run as well as the resources that you wish to allocate to the job.

Let us assume that you are trying to run a python script, `myscript.py` with the following contents:

```python
import time
print('Hello world')
time.sleep(20)
```

Create a shell script, `my_slurm_script.sh` with the following:

```shell
#!/bin/bash

#SBATCH --job-name='testjob'
#SBATCH --cpus-per-task=2
#SBATCH --mem=16GB
#SBATCH --output=testjob-%j-stdout.log
#SBATCH --error=testjob-%j-stderr.log
#SBATCH --time=00:05:00

echo "Submitting SLURM job"
singularity exec /idia/software/containers/SF-PY3-bionic.simg python myscript.py
```

The parameters that follow `#SBATCH` indicate the requested resources and other job parameters such as the job name and logging information. The `%j` in the output log file names is a placeholder for the job number or `jobid`. Run the  `sbatch --help` command from the terminal to see additional parameters or see the [table of parameters below](/getting_started/submit_job_slurm?id=slurm-job-parameters). 

In the shell script above, the application you wish to run during the job is described by `singularity exec /data/exp_soft/containers/SF-PY3-bionc.simg python myscript.py`. Here `python` is being used to run `myscript.py` using the python executable within the container `SF-PY3-bionic.simg`. This is a `singularity` container that is called with the `exec` command to execute the script.

The next step is to run the shell script using the SLURM `sbatch` command:

```shell
	$ sbatch my_slurm_script.sh 
```

This will submit the job to the SLURM queue. If the requested resources are available the job will be initiated. You can see the status of all jobs in the SLURM queue by using the command:

```shell
	$ squeue
```

To see the status of the jobs in the SLURM queue associated with your account use:

```shell
	$ squeue -u <username>
```

If any errors occur while running the job, you can view the logs in the `testjob-<jobid>-stderr.log`, and any text output can be found in `testjob-<jobid>-stdout.log`, as described by the shell script. This is useful for debugging any issues with your job.

## Interactive SLURM session

**No software should be run on the SLURM head node.** A shell terminal can be run on a compute node allowing for an interactive job on the cluster. Interactive jobs are useful for testing and developing code.

**NOTE:** interactive sessions are volatile and may be lost if you lose connection to the ilifu cluster. Persistent terminals, such as `tmux` or `screen` may help to reduce this volatility, however, in the event that the SLURM login node is restarted, the persistent terminal sessions will be lost. We therefore recommend that users submit jobs using `sbatch`, particularly for jobs with run times of greater than 3 hrs.

### Interactive session without X11 support

For an interative session on the SLURM cluster the `srun` command can be used as follows, from the SLURM head node:

```shell
	$ srun --pty bash
```

This will place you in an interactive shell (bash) session on a compute node. The `--pty` parameter provides a psuedo-terminal which allows interactivity. The default resources allocated by the `srun` command are 1 task, 1 CPU and 8 GB RAM. Run the `srun --help` command to see additional parameters. Similar parameters to the sbatch script above can be used to define the resources allocated to your interactive session. From the shell session, you are able to run interactive tasks, such as opening a Singularity container and loading an interactive CASA session, or utilizing Nextflow.

You are able to directly run Singularity containers or software within containers using the srun command, for example: 

```shell
	$ srun --pty singularity shell /idia/software/containers/SF-PY3-bionic.simg
```

This will open an interactive session on a compute node and open the SF-PY-bionic.simg container which includes a large suite of astronomy software. Alternatively, the following command will open an interactive CASA session on a compute node using the casa-stable.img container:

```shell
	$ srun --pty singularity exec /idia/software/containers/casa-stable.img casa --log2term --nologger
```

Incidently, you can also submit non-interactive jobs to SLURM using the `srun` command without the `--pty` parameter, for example:

```shell
	$ srun singularity exec /idia/software/containers/SF-PY3-bionic.simg python myscript.py
```

This will run the Python script `myscript.py` using the SF-PY3-bionic container on a compute node, similar to the `sbatch` command, however the job will not be run in the background, but will utilize your current terminal.

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

### Interactive session with X11 support

In the event that you wish to use software which provides a GUI, such as `CASA plotms`, you can start an interactive session with `X11 forwarding`. You must `ssh` into the SLURM head node with the `-Y` parameter which sets your DISPLAY variable for trusted `X11 forwarding` and the `-A` parameter for authentication-forwarding to the SLURM head node, for example:

```bash
	$ ssh -YA <username>@slurm.ilifu.ac.za
```

From there, you must use `salloc` to allocate a SLURM worker node to yourself using the `--qos qos-interactive` parameter, as follows:

```bash
	$ salloc --qos qos-interactive
```

This will place you in an interactive shell (bash) session on a compute node with `X11 forwarding` enabled. The default resources allocated by the `salloc` command are 1 task, 1 CPU and 8 GB RAM. You can again adjust what resources are allocated to your interactive session using the parameters such as `--cpus-per-task`, or `--mem`, for example:

```bash
	$ salloc --cpus-per-task=2 --mem=16GB --qos qos-interactive
```

You are then able to run a Singularity container and run software that provides a GUI.

When attempting to run `salloc` for an interactive session, you may experience a **Permission denied (publickey)** error. This suggests that that authentication-forwarding is not working correctly. If this is the case, you may need to add your ssh key to your authentication profile on your personal computer. To do this, run the following command from the terminal (not logged onto ilifu), for Ubuntu/Linux operating systems:

```bash
	$ ssh-add -k
```

or for Mac OS:

```bash
	$ ssh-add -K
```

## Specifying Resources when running jobs on SLURM

When running a job using an `sbatch` script or using `srun` or `salloc` for an interactive job, a user is able to specify the resources required for their job. A single node consists of `32 CPUs` and `236 GB RAM`. These are the maximum number of resources that can be requested per node.

If you are running a normal job on SLURM, **without** `MPI` or `OpenMP`, your job will only require `1 CPU`, `1 task` and `1 node`. These values are default values when running a job, however you are able to specify additional memory for your job using the `--mem` parameter.

Parallelism on the cluster can be achieved on a single node or over multiple nodes. Parallelism on a single node distributes work over multiple CPUs and is typically implemented using `OpenMP`. If you are running a job with software that utilizes `OpenMP` on SLURM, you can increase the number of CPUs for your job to > 1 CPU, while still using `1 task` and `1 node`. You may need to `export OMP_NUM_THREADS=<N>` to specify the number of threads the software will utilize.

Parallelism on the cluster can also occur by distributing work over many tasks that operate on 1 or more nodes. This type of parallelism is typically implemented using `MPI`. If you are running a job with software that utilizes `MPI` on SLURM, you can increase the number of `tasks` your job uses, `> 1 task`, while `nodes` and `CPUs` can be 1. The number of CPUs per task can be specified. You can increase the number of nodes if you want more than `32 CPUs` or `236 GB RAM`. 

The following table lists the parameters that can be used to decribe the required resources for your job:

<summary id='slurm-job-parameters'></summary>

| Syntax                                                                              | Meaning                                         | 
|--------------------------------------------------------------------------------------|----------------------------------------------------|
| --time=&#60;minutes&#62;<sup>1</sup>                                                 | Walltime for job (default is 3 days)               |
| --mem=&#60;number&#62;<sup>2,10</sup>                                                | Minimum amount of memory (default is 8 GB)         |
| --mem-per-cpu=&#60;number&#62;<sup>2,3,11</sup>                                      | Memory per processor core                          | 
| --cpus-per-task=&#60;number&#62;<sup>3,4,11</sup>                                    | Number of CPUs per task (default is 1)             |
| --ntasks=&#60;number&#62;<sup>4</sup>                                                | Number of processes to run (default is 1)          |
| --nodes=&#60;number&#62;<sup>5,11</sup>                                              | Number of nodes on which to run (default is 1)     |
| --ntasks-per-node=&#60;number&#62;<sup>4,5</sup>                                     | Number of tasks to invoke on each node             |
| --partition=&#60;partition_name&#62;<sup>6</sup>                                     | Request specific partition/queue (default Main)    |
| --account=&#60;account_name&#62;<sup>7</sup>                                         | The account that will be charged for the job       |
| --gres=&#60;resource_type&#62;:&#60;resource_name&#62;:&#60;number&#62;<sup>8</sup>  | Specify type and number of generic resources       |
| --output=&#60;file_name&#62;<sup>9</sup>                                             | File to write standard output to                   |
| --error=&#60;file_name&#62;<sup>9</sup>                                              | File to write standard error output to             |
| --mail-user=&#60;email_address&#62;<sup>10</sup>                                     | email address where notifications should be sent   |
| --mail-type=&#60;event_types&#62;<sup>10</sup>                                       | list of events that should send email notification |

*default parameters, if not specified, include: 1 node; 1 task; 1 CPU and 8GB RAM; running on the Main partition for 3 days.*

1. While the default for specifying the wall-time for a job is in minutes, it can also be specified as `mm:ss`, `hh:mm:ss` and even `days-hh:mm:ss`. Wall-time is the estimated amount of time that you expect your job to run. It is important for the scheduler to know this parameter so that it can make realistic estimates on when jobs are due to start and end. This is especially critical for your short jobs as it can allow them to run earlier when a node would otherwise be idle waiting for a large job to start. Note, however, that underestimating wall-time means that once your job has exceeded its limit, it will be killed. So it’s better to slightly overestimate the amount of time, especially taking into account that the runtime of jobs can vary a bit due to overall system load.
2. The default units for memory is MB, but can be specified explicitly in GB, example `--mem=16GB`. This parameter is especially important in jobs where you are not using the whole node, i.e. jobs using fewer than 32 cores, as this allows other jobs to run alongside yours and make more efficient use of the resources. 
3. CPUs refers to the the number of CPUs associated with your job.
4. a task is an instance of a running program, generally you will only want one task, unless you use software with MPI support (for example CASA), SLURM works with MPI to manage parallelised processing of data.
5. nodes refers to a single compute node or SLURM worker, i.e. one node has 32 CPUs and 236 GB RAM
6. The partition is the specific part of the cluster your job will run. You will only use this if you are [running a GPU job](/getting_started/submit_job_slurm?id=notes-for-gpu-jobs).
7. To find your default account you can run the command `sacctmgr show User -p | grep ${USER}`, while the command `sacctmgr show Associations User=${USER} -p | cut -f 2 --d="|"` will show all your valid accounts.
8. Request generic resource (per node). You will only use this if you are [running a GPU job](/getting_started/submit_job_slurm?id=notes-for-gpu-jobs).
9. The filename can include `%j` which will be substituted with the job's ID.
10. Email notifications can optionally be sent when a job's state changes. Create a comma-separated list with at least one of the following notification types: `NONE`; `BEGIN`; `END`; `FAIL`; `REQUEUE`; `ALL` (equivalent to `BEGIN,END,FAIL,REQUEUE,STAGE_OUT); STAGE_OUT`; `TIME_LIMIT`; `TIME_LIMIT_90` (reached 90 percent of time limit); `TIME_LIMIT_80` (reached 80 percent of time limit); `TIME_LIMIT_50` (reached 50 percent of time limit); and `ARRAY_TASKS`. ARRAY_TASKS will mean that a notification will be sent for each task in a job array (the default is only for the job array as a whole.)
11. **Note that if you specify more memory or cores than is available on the nodes, or more nodes than are available on the cluster, _your job will never start but it will sit in the queue!_**


### Notes for GPU jobs.

If you wish to run a job on the GPU node you need to specify both the `GPU` partition and you need to specify the number of GPU resources you require with the `--gres` option. i.e. your sbatch script will have something like the following lines in the header:
```code bash
#SBATCH --partition=GPU
#SBATCH --gres=gpu:p100:1
```

Note that the 3 GPU nodes only have 2 GPUs each, so you must use either `--gres=gpu:p100:1` or `--gres=gpu:p100:2`.

