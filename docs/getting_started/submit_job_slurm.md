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
#SBATCH --cpus-per-task=4
#SBATCH --mem=64GB
#SBATCH --output=testjob-%j-stdout.log
#SBATCH --error=testjob-%j-stderr.log

echo "Submitting SLURM job"
singularity exec /data/exp_soft/containers/SF-PY3-bionic.simg python myscript.py
```

The parameters that follow `#SBATCH` indicate the requested resources and other job parameters such as the job name and logging information. The `%j` in the output log file names is a placeholder for the job number or `jobid`. Run the  `sbatch --help` command from the terminal to see additional parameters. Other useful parameters include:

| Syntax                               | Meaning                                   | 
|--------------------------------------|-------------------------------------------|
| --ntasks=&#60;number&#62;            | Number of processes to run (default is 1) | 
| --mem-per-cpu=&#60;number&#62;       | Memory per processor core                 | 
| --partition=&#60;partition_name&#62; | Request specific partition/queue          | 

* a nodes refer to a single compute node or slurm worker, i.e. one node has 32 CPUs and 236 GB RAM
* a task is an instance of a running program, generally you will only want one task, unless you use software with MPI support (for example CASA), SLURM works with MPI to manage parallelised processing of data.
* CPUs refers to the the number of CPUs associated with your job.
* default parameters, if not specified, include 1 node, 1 task, 1 CPU and 8GB RAM.

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

**No software should be run on the SLURM head node.** Interactive jobs are useful for testing and developing code. 

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

In the event that you wish to use software which provides a GUI, such as `CASA plotms`, you can start an interactive session with `X11 forwarding`. You must `ssh` into the SLURM head node with the `-Y` parameter which sets your DISPLAY variable for trusted `X11 forwarding` for example:

```bash
	$ ssh -Y <username>@slurm.ilifu.ac.za
```

From there, you must use `salloc` to allocate a SLURM worker node to yourself using the `--qos qos-interactive` parameter, as follows:

```bash
	$ salloc --qos qos-interactive
```

This will place you in an interactive shell (bash) session on a compute node with `X11 forwarding` enabled. The default resources allocated by the `salloc` command are 1 task, 1 CPU and 8 GB RAM. You can again adjust what resources are allocated to your interactive session using the parameters such as `--cpus-per-task`, or `--mem`, for example:

```bash
	$ salloc --cpus-per-task=8 --mem=32GB --qos qos-interactive
```

You are then able to run a Singularity container and run software that provides a GUI.
