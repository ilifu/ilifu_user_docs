# Logging into the ilifu services

There are two main ways to access ilifu services, either by using SSH via a terminal to access a service, or using a web browser for access to web-based applications. 

The Slurm batch scheduler is the primary service accessed via SSH. Other services accessed via SSH include the [transfer node](data/data_transfer?id=transfer-using-scp-and-rsync).

 Web-based applications include [Jupyter](https://jupyter.ilifu.ac.za/), [CARTA](https://carta.idia.ac.za/) and a [reports](https://reports.ilifu.ac.za/) portal, where users can manage their profile information, review usage data and manage the SSH public keys associated with their account. Web-based services are accessible through the dashboard on the [IDIA Gateway](https://gateway.idia.ac.za/), or directly via their URL linked above.

## Slurm batch scheduler

Slurm is a job scheduling system. It consists of a single login node and many compute nodes. The login node is likened to a controller and manages the cluster resources and job submissions.

The Slurm system can be accessed via `SSH` at `slurm.ilifu.ac.za`.

```
$ ssh <username>@slurm.ilifu.ac.za
```

This will place the user on the login node. Note that this node should only be used to submit and manage jobs and not for running code or software directly. The compute nodes are where jobs are run, either through submitting a batch script that describes the job to be executed, or interactively running applications on a compute node. See [Submitting a job on Slurm](getting_started/submit_job_slurm.md) for more information on how to do this.

**Note** some activities require direct access to Slurm compute nodes via ssh, such as running htop to monitor your running job. In order to achieve this you must use authentication forwarding when sshing onto the Slurm login node using the `-A` parameter, for example:

```bash
$ ssh -A <username>@slurm.ilifu.ac.za
```
See a summary of the Slurm partitions and their use cases [below](getting_started/access_ilifu?id=summary-of-ilifu-services-or-partitions-and-their-use-case).

## IDIA Gateway

The IDIA gateway is accessible at `https://gateway.idia.ac.za`. The IDIA gateway provides access to public data downloads and an application dashboard.

<div style="text-align:center"><img src="/_media/idia_gateway.png" alt="idia gateway" width=500 /></div>

 The application dashboard utilises Single Sign-on (SSO) to ilifu web-based applications, including Jupyter, CARTA, account usage data, SSH key management, amongst other services.

<div style="text-align:center"><img src="/_media/open_ondemand.png" alt="application dashboard" width=500 /></div>

## Jupyter

The Jupyter service can be accessed via a web browser, either through the [IDIA Gateway](https://gateway.idia.ac.za/) application dashboard, or directly at `https://jupyter.ilifu.ac.za`. This service allows the user to spawn a job on the ilifu cluster running JupyterLab, providing a development space for writing, testing and debugging new code, software, workflows or routines, within a highly interactive Jupyter notebook environment that enables tab-completion, viewing doc strings (i.e. documentation from Python functions and modules), and running subroutines within different notebook cells. Jupyter may also be the primary interface for stable workflows that aren’t necessary to submit to the Slurm cluster, such as short analysis routines or other highly interactive workflows.

After logging into the JupyterLab service, the user is presented with a breakdown of the available session sizes and a drop-down menu with a list of options for compute resources. **Please select the smallest session size that will provide sufficient resources for the task at hand.**

<div style="text-align:center"><img src="/_media/jupyter_spawner_dropdown.png" alt="drop-down menu" width=800 /></div>

Each node will be terminated after a preset interval of time (currently set to terminate after 18 hours of inactivity or 5 days), however the user's Jupyter environment is saved in their home directory, so when a new jupyter server is spawned their workspace and notebooks will be recreated. Some data also persists in the notebook file, however any long-running processes will be terminated when the jupyter session is stopped, or when it reaches its time limit. The Jupyter service is designed for interactive development and analysis, not for high performance computing. For long running or resource heavy tasks, please refer to the [Slurm Batch Scheduler](http://docs.ilifu.ac.za/#/tech_docs/running_jobs?id=slurm-batch-scheduler) section). 

**Please shut down your Jupyter server if you are not planning to use it for more than a few hours.** We encourage you to be especially vigilant about shutting down your unused server if you have selected a "Max" or "Half-max" server option. To shut down your session, navigate in your browser to the Jupyter menu and select "File" > "Hub Control Panel":

<div style="text-align:center"><img src="/_media/hub_selection.png" alt="menu bar options" width=500 /></div>

This will bring you to the page with the `Stop My Server` option, where you can stop your current session, freeing up the resources that have been allocated to your Jupyter session. You are also able to use this process to change the size of the resources allocated to you. Once you have stopped your session you are able to choose a smaller or larger node size.

<div style="text-align:center"><img src="/_media/stop_server_button.png" alt="stop server button" width=600 /></div>

Whenever possible, **please submit your work via the Slurm batch queue rather than running it in a Jupyter session.** Any non-interactive work that requires an execution time longer than a few minutes, or that requires a high amount of resources, should be submitted to the batch queue.

## Summary of ilifu services or partitions and their use case

Ilifu offers a number of different services, compute partitions and environments. Each of these has a different purpose, and can be considered within a variety of use cases. 

### Login node
The Slurm login node, where you land when logging into the ilifu Slurm cluster (`slurm.ilifu.ac.za`), is for running basic bash commands (`cd`, `mkdir`, `ls`, etc), and running Slurm commands to submit and interact with your jobs (`srun`, `sbatch`, `scancel`, `squeue`, `sacct`, etc). 

### Jupyter
Jupyter (`jupyter.ilifu.ac.za`) is a development space for writing, testing and debugging new code, software, workflows or routines, within a highly interactive Jupyter notebook environment that enables tab-completion, viewing doc strings (i.e. documentation from Python functions and modules), and running subroutines within different notebook cells. Jupyter may also be the primary interface for stable workflows that do not need to be submitted to the Slurm cluster, such as short analysis routines or other highly interactive workflows. For more information visit our Jupyter documentation page.

### Devel
Similarly, the `Devel` partition within the Slurm cluster is for development of computational routines within a shared resource environment, enabling users to submit jobs instantly / quickly, but with resources shared, rather than solely allocated to your jobs (as is the case in other Slurm partitions). This allows interactivity via a shell, and is generally for testing higher level workflows and pipelines compared to those run on Jupyter. This can be simply accessed using the `sinteractive` command.

### Main
The `Main` partition within Slurm is generally for stable, computationally-heavy workflows and pipelines (e.g. many small jobs allocated few resources or a few large jobs allocated many resources), which have first been tested on one of the services mentioned above where applicable.

### HighMem
The `HighMem` partition within Slurm is for single high-memory jobs that cannot be split into multiple jobs using MPI.

### GPU
The `GPU` (and `GPUV100`) partition within Slurm (and Jupyter) is for jobs making use of GPUs. Please do not use the GPU partition for jobs that only require CPU resources.

### Transfer node
The ilifu transfer node (`transfer.ilifu.ac.za`) is for internal and external copying of data (`cp`, `scp`, `rsync`, etc), for smaller or less frequent transfers that do not require Globus. It may also be used for other bash commands inappropriate for the Slurm login node (`wget`, `rm`, etc), although these may also be run on a compute node using a small allocation (e.g. 1 CPU with 1 GB RAM).