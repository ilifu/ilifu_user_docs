# Logging into the ilifu services

There are two main ways to access ilifu services, either by using SSH via a terminal to access a service, or using a web browser for access to web-based applications. 

The Slurm batch scheduler is the primary service accessed via SSH. Other services accessed via SSH include the [transfer node](data/data_transfer?id=transfer-using-scp-and-rsync).

 Web-based applications include [Jupyter](https://jupyter.ilifu.ac.za/), [CARTA](https://carta.idia.ac.za/) and a [usage](https://usage.ilifu.ac.za/) portal, where users can manage their profile information, review usage data and manage the SSH public keys associated with their account. Web-based services are accessible through the dashboard on the [IDIA Science Gateway](https://gateway.idia.ac.za/), or directly via their URL linked above.

## Slurm batch scheduler

Slurm is a job scheduling system. It consists of a single login node and many compute nodes. The login node is the access point to the ilifu Slurm cluster, and allows the user to view available resources, current activity (queued and running jobs) and to submit jobs to the cluster.

The ilifu Slurm cluster can be accessed via `ssh` at `slurm.ilifu.ac.za`.

```
$ ssh <username>@slurm.ilifu.ac.za
```

This will place the user on the login node. Note that this node should only be used to submit and manage jobs and not for running code or software directly. The compute nodes are where jobs are run, either through submitting a batch script that describes the job to be executed, or interactively running applications on a compute node. See [Submitting a job on Slurm](getting_started/submit_job_slurm.md) for more information on how to do this.

**Note** some activities require direct access to Slurm compute nodes via ssh, such as running `htop` to monitor your running job. In order to achieve this you must use authentication forwarding when sshing onto the Slurm login node using the `-A` parameter, for example:

```bash
$ ssh -A <username>@slurm.ilifu.ac.za
```
See a summary of the Slurm partitions and their use cases [below](getting_started/access_ilifu?id=summary-of-ilifu-services-or-partitions-and-their-use-case).

## IDIA Science Gateway

The [IDIA Science Gateway](https://gateway.idia.ac.za) is accessible at `https://gateway.idia.ac.za`. The IDIA Science Gateway provides access to public data downloads and an application dashboard.

<div style="text-align:center"><img src="/_media/idia_gateway.png" alt="idia science gateway" width=500 /></div>

 The application dashboard utilises Single Sign-on (SSO) to ilifu web-based applications, including [Jupyter](getting_started/access_ilifu?id=jupyter), [CARTA](astronomy/astronomy_software?id=carta), [Visual Studio Code](tech_docs/software_environments?id=visual-studio-code), account usage data, SSH key management, amongst other services.

<div style="text-align:center"><img src="/_media/open_ondemand.png" alt="application dashboard" width=500 /></div>

## Jupyter

The Jupyter service can be accessed via a web browser, either through the [IDIA Science Gateway](https://gateway.idia.ac.za/) application dashboard, or directly at `https://jupyter.ilifu.ac.za`. This service allows the user to spawn a job on the ilifu Slurm cluster running JupyterLab, providing a development space for writing, testing and debugging new code, software, workflows or routines, within a highly interactive Jupyter notebook environment that enables tab-completion, viewing doc strings (i.e. documentation from Python functions and modules), and running subroutines within different notebook cells. Jupyter may also be the primary interface for stable workflows that aren’t necessary to submit to the Slurm cluster, such as short analysis routines or other highly interactive workflows.

After logging into the JupyterLab service, the user is presented with a breakdown of the available session sizes and a drop-down menu with a list of options for compute resources. **Please select the smallest session size that will provide sufficient resources for the intended task.**

<div style="text-align:center"><img src="/_media/jupyter_spawner_dropdown.png" alt="drop-down menu" width=800 /></div>

The **Jupyter development session** type is aimed at lightweight development and testing of workflows that don't require dedicated resources (i.e. CPU and RAM). Instead, the sessions make use of shared resources (CPU cores) and are allocated `2 CPU cores`, `3GB RAM` and have a `14 day` lifespan (with an 18 hour idle timeout). We recommend that users should initially use the development session type for new sessions, and only select a larger session size if it is found that additional memory resources or dedicated resources are required (e.g. for running an intensive workflow).

Each node will be terminated after a preset interval of time (currently set to terminate after 18 hours of inactivity or 5 days), however the user's Jupyter environment is saved in their home directory, so when a new jupyter server is spawned their workspace and notebooks will be recreated. Some data also persists in the notebook file, however any long-running processes will be terminated when the jupyter session is stopped, or when it reaches its time limit. The Jupyter service is designed for interactive development and analysis, not for high performance computing. For long running or resource heavy tasks, please refer to the [Slurm Batch Scheduler](getting_started/submit_job_slurm?id=submitting-a-job-using-a-batch-script) section. 

## Summary of ilifu services or partitions and their use case

Ilifu offers a number of different services, compute partitions and environments. Each of these has a different purpose, and can be considered within a variety of use cases. 

### Login node
The Slurm login node, where you land when logging into the ilifu Slurm cluster (`slurm.ilifu.ac.za`), is for running basic bash commands (`cd`, `mkdir`, `ls`, etc), and running Slurm commands to submit and interact with your jobs (`srun`, `sbatch`, `scancel`, `squeue`, `sacct`, etc). 

### Jupyter
Jupyter (`jupyter.ilifu.ac.za`) is a development space for writing, testing and debugging new code, software, workflows or routines, within a highly interactive Jupyter notebook environment that enables tab-completion, viewing doc strings (i.e. documentation from Python functions and modules), and running subroutines within different notebook cells. Jupyter may also be the primary interface for stable workflows that do not need to be submitted to the Slurm cluster, such as short analysis routines or other highly interactive workflows. For more information visit our [Jupyter documentation](getting_started/using_jupyterlab.md) page.

### Devel
Similarly, the `Devel` partition within the Slurm cluster is for development of computational routines within a shared resource environment, enabling users to submit jobs instantly / quickly, but with resources shared, rather than solely allocated to your jobs (as is the case in other Slurm partitions). This allows interactivity via a shell, and is generally for testing higher level workflows and pipelines compared to those run on Jupyter. This can be simply accessed using the `sinteractive` command.

### Main
The `Main` partition within Slurm is generally for stable, computationally-heavy workflows and pipelines (e.g. many small jobs allocated few resources or a few large jobs allocated many resources), which have first been tested on one of the services mentioned above where applicable.

### HighMem
The `HighMem` partition within Slurm is for single high-memory jobs that cannot be split into multiple jobs using MPI.

### GPU
The `GPU` partition within Slurm (and Jupyter) is for jobs making use of GPUs. Please do not use the GPU partition for jobs that only require CPU resources.

### Transfer node
The ilifu transfer node (`transfer.ilifu.ac.za`) is for internal and external copying of data (`cp`, `scp`, `rsync`, etc), for smaller or less frequent transfers that do not require Globus. It may also be used for other bash commands inappropriate for the Slurm login node (`wget`, `rm`, etc), although these may also be run on a compute node using a small allocation (e.g. 1 CPU with 1 GB RAM).