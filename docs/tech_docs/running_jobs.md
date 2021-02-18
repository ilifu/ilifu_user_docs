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

**NOTE:** interactive sessions make use of the same resource pool as jobs submitted using `sbatch`. If you are experiencing delays acquiring an interactive session you can either try to reduce the number of resources (CPU, memory and run-time) that you are requesting, or use the parameter `--qos qos-interactive` when launching your interactive job. **This parameter provides increased priority but is limited to 1 job, 4 CPUs and 28 GB memory.**

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
The slurm documentation [on priority](https://slurm.schedmd.com/priority_multifactor.html) and [fairshare](https://slurm.schedmd.com/fair_tree.html) is very extensive, what follows here is a short summary of the principles behind priority and fairshare; and how to check what's going on with your jobs on ilifu.

### Multifactor Priority
Our slurm is configured to use multifactor priority scheduling which uses a number of factors to determine a job's priority. For each job that's submitted to the cluster, these factors are used to calculate that job's priority. The weighting of these factors can change if they're found not to be giving a fair usage to all users of the cluster. At any time the weights of the factors can be checked as follows:
```shell
$ scontrol show config | grep PriorityWeight
PriorityWeightAge       = 500
PriorityWeightAssoc     = 0
PriorityWeightFairShare = 100000
PriorityWeightJobSize   = 12500
PriorityWeightPartition = 0
PriorityWeightQOS       = 20000
PriorityWeightTRES      = (null)
```
A description of each these factors can be found [here](https://slurm.schedmd.com/priority_multifactor.html#mfjppintro) however the most important factors are:
1. **JobSize**: This factor gives priority to jobs based on their size. In particular our cluster is configured to give priority to larger jobs; This can be checked by running `scontrol show config | grep PriorityFavorSmall`. A job that requests all the nodes in cluster will receive the maximum priority weighting here: `1.0 × 12500` while a single node job would receive a priority weighting of `0.02 × 12500` (assuming there were 50 nodes in the cluster).
2. **QOS**: The Quality of Service weighting is used to give interactive jobs a higher priority. Please note the [limits of the qos-interactive](tech_docs/running_jobs?id=interactive-slurm-sessions) QOS option.
3. **Age**: The age factor is intentionally set very small so that as jobs age their priority increases only slightly. This is so that the _FairShare_ factor is dominant in most cases.
4. **FairShare**: The fairshare factor is the primary means of making cluster usage fair amongst our users and is described in more detail below. The idea is that the ilifu cluster is funded in different proportions by various groups and they should be given proportional access to the cluster. Further, within the funding groups there are separate projects, and these projects can also be allocated proportional access through a hierarchical description. Finally, within each project the individual users can be found, where once again they can be assigned a different proportion of access.

If one needs to check the priority of your jobs you can see this, together with the individual factors, using the `sprio` command as follows:
<details>
<summary><code>sprio -u userA,userB,userC</code></summary>

```shell
sprio -u userA,userB,userC
          JOBID PARTITION     USER   PRIORITY       SITE        AGE  FAIRSHARE    JOBSIZE        QOS
        1019947 Main         userC      56778          0         83      56545        151          0
        1021758 Main         userA        502          0        143        209        151          0
        1021776 Main         userA        492          0        132        209        151          0
        1022250 Main         userC      56774          0         80      56545        151          0
        1022891 Main         userB        886          0        108        628        151          0
```

</details>


### Fairshare
Proportional access of the cluster is described using a hierarchy of shares given to funders, projects and users. Once the shares have been allocated, actual usage is taken into account. This considers all of an account's usage relative to other accounts and uses this to calculate a final FairShare value.

#### Shares
As noted before the shares on the cluster are described in a hierarchical fashion, where at the top level there are funders, followed by projects and finally the users themselves.

The fairshare shares associated within the funder-level accounts is set to reflect the proportion of money invested in ilifu. In terms of ilifu's primary funders these values can be checked as follows:

<details>
<summary><code>sshare --format="Account,RawShares"</code></summary>

```shell
$ sshare --format="Account,RawShares" | grep " a\|Raw"
             Account  RawShares 
 a01-idia-ag                 33 
 a02-cbio-ag                 20 
 a03-dirisa-ag               42 
 a04-cchem-ag                 5
```
i.e. funding currently of ilifu is in the ratio IDIA:CBIO:DIRISA:CCHEM = 33:20:42:5.
</details>

The fairshare shares associated within projects are usually all the same, i.e. all the projects falling under a given funder have equal access to the cluster. This can be seen looking at say the first few idia projects as follows:

<details>
<summary><code>sshare --format="Account,RawShares" | head -n 30</code></summary>

```shell
$ sshare --format="Account,RawShares" | head -n 30
             Account  RawShares 
-------------------- ---------- 
root                            
 a01-idia-ag                 33 
  b01-ska-ag                  1 
  b02-mhongoose-ag            1 
  b03-idia-ag                 1 
   b03-idia-ag                1 
  b04-lensed-hi-ag            1 
  b05-pipelines-ag            1 
  b08-fornax-ag               1 
  b09-mightee-ag              1 
  b10-intensitymap-+          1 
  b11-vlbi-ag                 1 
  b15-pink-ag                 1 
  b17-mightee-ukzn-+          1 
  b19-meerlicht-ag            1 
  b20-mals-ag                 1 
  b21-ulx1-ag                 1 
  b23-smc-ag                  1 
  b24-thunderkat-ag           1 
  b26-laduma-ag               1 
  b27-m64-ngc151-ag           1 
  b28-hippo-ag                1 
  b32-mhishaps-ag             1 
  b34-admins-ag               1 
   b34-admins-ag              1 
  b36-vela-ag                 1 
  b37-rhodes-ratt-ag          1 
  b40-healy-a2626-ag          1
```

**Note**: One can see the hierarchical nature of the shares here.
</details>

CBIO has chosen however to give a higher priority to their primary project:

<details>
<summary><code>sshare --format="Account,RawShares | grep cbio</code></summary>

```shell
$ sshare --format="Account,RawShares" | grep cbio
 a02-cbio-ag                 20 
  b16-cbio-ag                 1 
   b16-cbio-ag                1 
  b56-cbio-001-ag            12 
  b57-cbio-002-ag             1 
  b58-cbio-003-ag             1 
  b67-cbio-004-ag             1 
  b70-cbio-005-ag             1 
  b83-cbio-006-ag             1 
  b85-cbio-007-ag             1 
  b88-cbio-008-ag             1 
  b89-cbio-009-ag             1 
  b90-cbio-010-ag             1 
  b93-cbio-011-ag             1 
  b99-cbio-012-ag             1
```

</details>

Finally all users within projects (on ilifu) have equal access within their projects.

<details>
<summary><code>sshare -a --format="Account,User,RawShares" | head -n 40</code></summary>

```shell
$ sshare -a --format="Account,User,RawShares" | head -n 40
             Account       User  RawShares 
-------------------- ---------- ---------- 
root                                       
 root                      root          1 
 a01-idia-ag                            33 
  b01-ska-ag                             1 
   b01-ska-ag             frank          1 
   b01-ska-ag              ianh          1 
   b01-ska-ag          isabella          1 
  b02-mhongoose-ag                       1 
   b02-mhongoose-ag    athomson          1 
   b02-mhongoose-ag        blok          1 
   b02-mhongoose-ag    djpisano          1 
   b02-mhongoose-ag       frank          1 
   b02-mhongoose-ag      gheald          1 
   b02-mhongoose-ag      grange          1 
   b02-mhongoose-ag  rontrompe+          1 
  b03-idia-ag                            1 
   b03-idia-ag         abonaldi          1 
   b03-idia-ag            adams          1 
   b03-idia-ag         adrianna          1 
   b03-idia-ag              afg          1 
   b03-idia-ag           aikema          1 
   b03-idia-ag          ajbaker          1 
   b03-idia-ag        ajvdhorst          1 
   b03-idia-ag          aleloni          1 
   b03-idia-ag       amirkazem+          1 
   b03-idia-ag        anastasia          1 
   b03-idia-ag             ando          1 
   b03-idia-ag             andy          1 
   b03-idia-ag            angus          1 
   b03-idia-ag             anke          1 
   b03-idia-ag          aparikh          1 
   b03-idia-ag          ascaife          1 
   b03-idia-ag       athanaseus          1 
   b03-idia-ag         athomson          1 
   b03-idia-ag            aycha          1 
   b03-idia-ag       bengelbre+          1 
   b03-idia-ag           bester          1 
   b03-idia-ag             blok          1
```

</details>

#### Usage
Once the shares have been allocated the actual usage by users/accounts is considered. take for example two of the projects running on the cluster:

<details>
<summary><code>sshare -a --format="Account,User,RawUsage,FairShare,LevelFS"</code></summary>

```shell
$ sshare -a --format="Account,User,RawUsage,FairShare,LevelFS" | grep -v "inf" | grep "User\|b24\|b19"
             Account       User    RawUsage  FairShare    LevelFS 
  b19-meerlicht-ag                239670481              0.188518 
   b19-meerlicht-ag        andy         429   0.082723 1.5085e+04 
   b19-meerlicht-ag      nblago      350752   0.079581  18.467596 
   b19-meerlicht-ag         pmv   239299739   0.078534   0.027069 
   b19-meerlicht-ag    simdewet        2715   0.081675 2.3857e+03 
   b19-meerlicht-ag  sumedhabi+       16844   0.080628 384.545736 
  b24-thunderkat-ag               493709909              0.091516 
   b24-thunderkat-ag     bright    10095018   0.007330   1.086806 
   b24-thunderkat-ag      dante        4697   0.017801 2.3358e+03 
   b24-thunderkat-ag francesco+        3061   0.019895 3.5840e+03 
   b24-thunderkat-ag       ianh    42273760   0.003141   0.259531 
   b24-thunderkat-ag jakobvand+     2392664   0.011518   4.585403 
   b24-thunderkat-ag   jcollier        4272   0.018848 2.5677e+03 
   b24-thunderkat-ag    jgirard        1401   0.023037 7.8256e+03 
   b24-thunderkat-ag   jkersten     4417718   0.009424   2.483483 
   b24-thunderkat-ag    jmoldon        5039   0.016754 2.1769e+03 
   b24-thunderkat-ag   julioanj    16789261   0.005236   0.653473 
   b24-thunderkat-ag kelebogil+        2339   0.020942 4.6886e+03 
   b24-thunderkat-ag laurenrho+     3995881   0.010471   2.745660 
   b24-thunderkat-ag  madzimest        5670   0.015707 1.9347e+03 
   b24-thunderkat-ag    mcoriat           0   0.025131 1.9313e+08 
   b24-thunderkat-ag reikantse+      248307   0.013613  44.184462 
   b24-thunderkat-ag      retha        1884   0.021990 5.8216e+03 
   b24-thunderkat-ag     robbie     1290421   0.012565   8.502129 
   b24-thunderkat-ag sarahchas+   284738897   0.001047   0.038531 
   b24-thunderkat-ag        sem    86446084   0.002094   0.126915 
   b24-thunderkat-ag     tremou     6597117   0.008377   1.663049 
   b24-thunderkat-ag     wenfei         363   0.024084 3.0165e+04 
   b24-thunderkat-ag  williamsd    19899115   0.004188   0.551348 
   b24-thunderkat-ag       xian      227163   0.014660  48.297169 
   b24-thunderkat-ag      zwang    14269763   0.006283   0.768852
```

Here we see that the one project has approximately twice the usage of the other project, resulting in the users within the projects having dramatically different FairShare values.

</details>

A note on **LevelFS**: This gives an indication whether an account is using more or less than is allocated to it via the shares. A value of 1 indicates a perfect usage, less than 1 indicates more usage than allocated and more than 1 means it is underused. It is very unlikely that these values will be exactly 1, however over a long period of time, assuming all users/groups are active, they should tend towards 1.

<details>
<summary><code>sshare --format="Account,RawShares,RawUsage,LevelFS" | grep -v "inf" | grep "Shares\|a0</code></summary>

```shell
$ sshare --format="Account,RawShares,RawUsage,LevelFS" | grep -v "inf" | grep "Shares\|a0"
             Account  RawShares    RawUsage    LevelFS 
 a01-idia-ag                 33  2078039237   0.423716 
 a02-cbio-ag                 20   578477684   0.922482 
 a03-dirisa-ag               42    37792325  29.652425 
 a04-cchem-ag                 5       27631 4.8281e+03
```

</details>

And lastly we consider [PriorityDecayHalfLife](https://slurm.schedmd.com/priority_multifactor.html#config). This indicates how long past usage counts towards the fairshare calculation. On ilifu this is currently set to a half life of 14 days, i.e. every 14 days the accumulated usage is halved. This value can be checked in the configuration using:

<details>
<summary><code>scontrol show config | grep Decay</code></summary>

```shell
$ scontrol show config | grep Decay
PriorityDecayHalfLife   = 14-00:00:00
```
This is calculated every 5 minutes.
```shell
$ scontrol show config | grep PriorityCalcPeriod
PriorityCalcPeriod      = 00:05:00
```

</details>
