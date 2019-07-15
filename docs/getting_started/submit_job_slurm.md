# Submitting a job on SLURM

Two common ways to run jobs on SLURM include submitting jobs using a batch script, and running jobs interactively.

## Submitting a job using a batch script.

After `sshing` in to `slurm.ilifu.ac.za`, you can submit a job to SLURM using a shell script. The script must describe the application/software you wish to run as well as the resources that you wish to allocate to the job.

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
#SBATCH --ntasks=1
#SBATCH --output=logs/testjob.log

echo "Submitting SLURM job"
singularity exec /data/exp_soft/containers/SF-PY3-bionic.simg python myscript.py
```

The parameters that follow `#SBATCH` indicate the requested resources and other job parameters such as the job name and logging information. Other useful parameters include (run the  **man sbatch** command to see additional parameters):

| Syntax                      | Meaning                                   | 
|-----------------------------|-------------------------------------------|
| --ntasks=<number>           | Number of processes to run (default is 1) | 
| --mem=<number>              | Total memory per node                     | 
| --mem-per-cpu=<number>      | Memory per processor core                 | 
| --partition=<partition_name>| Request specific partition/queue          | 

In the shell script above, the application you wish to run during the job is described by `singularity exec /data/exp_soft/containers/SF-PY3-bionc.simg python myscript.py`. Here `python` is being used to run `myscript.py` using the python executable within the container `SF-PY3-bionic.simg`. This is a `singularity` container that is called with the `exec` command to execute the script.

The next step is to run the shell script using the SLURM `sbatch` command:

```shell
	$ sbatch my_slurm_script.sh 
```

This will submit the job to the SLURM queue. If the requested resources are available the job will be initiated. You can see the status of your job using the command:

```shell
	$ squeue
```

If any errors occur while running the job, you can view the logs in the `logs/testjob.log`, as described by the shell script, to debug.

## Interactive SLURM session

No software or process should be run on the SLURM headnode. Interactive jobs are useful for testing and developing code. For an interative session on the SLURM cluster the `srun` command can be used as follows:

```shell
	username@slurm-login:~$ srun -N 1 --pty bash
	username@slwrk-027:~$
```

This will allocate a number of compute nodes specified by the `-N` parameter (default is 1), and will ssh you into one of the allocated worker nodes. Run the **man srun** command to see additional parameters.  A bash terminal session will be loaded from where you are able to run interactive tasks, such as opening a Singularity container and loading an interactive CASA session or utilizing Nextflow.

For an interactive session with `X11 forwarding`, in the event you wish to use CASA tasks with their GUIs, you must `ssh` into SLURM with the `-Y` parameter which sets your DISPLAY variable for trusted `X11 forwarding`, and the `-A` parameter for forwarding the authentication agent connection, for example:

```bash
	$ ssh -AY <username>@slurm.ilifu.ac.za
```

From there, you can use `salloc` to allocate a SLURM worker node to yourself, or you can use the above `srun` command to allocate a SLURM worker node. In both cases, you can check the name of the worker node that has been allocated to you by running:

```bash
	$ squeue
```

This will show a list of the current jobs running. You should be able to see the name of the SLURM worker node that has been allocated to your username. Once you have determined the correct name of the worker node, you must ssh into the worker node with the `-Y` parameter to carry the X11 forwarding to the SLURM worker node, for example:

```bash
	$ ssh -Y slwrk-020
```

You are then able to run a Singularity container and run an interactive CASA session with access to the GUIs. The `casa-stable` and `casameer` Singularity container images contain the X11 tools required for X11 forwarding.

Note that the forwarding of the authentication agent connection will not work from within the worker node when using the `srun` command as this breaks the agent forwarding pipe. You will need an alternative terminal to ssh into the worker node.

Please only use this method for viewing GUI and visualization tools, and do not run any heavy processing within the ssh session on the worker node. Please exit the worker node once you have finished the interactive session in order to return the resources to the SLURM pool.

Note that when using an interactive shell in SLURM by using the `srun` command, your interactive session may be vulnerable to being killed if you lose your network connection. To avoid this, you can use `tmux` for a persistent terminal that can be reaccessed after the loss of the ssh session. However, when using `tmux`, please make sure to exit the `tmux` session in order to release the resources back to the SLURM pool. Basic `tmux` commands include: 

| Syntax/keyboard shortcut      | Action                                    | 
|-------------------------------|-------------------------------------------|
| tmux                          | start new tmux session                    | 
| tmux ls                       | list currently active tmux sessions       | 
| tmux attach -t <session_name> | attach to an active tmux session          | 
| ctrl/cmd-b + d                | detach from current tmux session          | 
| ctrl/cmd-b + [                | scroll current terminal                   |


