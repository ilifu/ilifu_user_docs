# Supported software environments

The software environments on ilifu are provided principally through [Singularity](https://docs.sylabs.io/guides/latest/user-guide/) containers and [environment modules](tech_docs/software_environments?id=environment-modules). Additional software environments include virtual environments, either [Python virtual environments](tech_docs/software_environments?id=python-virtual-environments), or [Conda](tech_docs/software_environments?id=anaconda) -- these are generally created and managed by the user or project group. 

Below we provide an introduction to using Singularity containers which will be helpful when using containerised software when submitting jobs to Slurm. For further information on the software environments available on ilifu, including [modules](tech_docs/software_environments?id=environment-modules) and [virtual environments](tech_docs/software_environments?id=python-virtual-environments), please see the supported [Software environments](tech_docs/software_environments.md) documentation.

## Singularity containers

Containers are unit software packages that contain all the software, files, libraries, dependencies and environmental variables necessary to run a particular task or workflow. Containers are encapsulated software environments and abstract the software and applications from the underlying operating system, however, have access to the same filesystem as a user would have access to. This allows users to run workflows in customised environments, switch between environments, and to share these environments with colleagues and research teams.

### Using a container

The container images that are maintained by the support team can be found at different paths, depending on the group that you belong to: `/idia/software/containers/`, `/cbio/images` and `/ilifu/software/containers`, as well as common areas `/software/<astro|bio|common>/containers`. There are a number of ways one can use a Singularity container, including executing the software inside a container or interactively using a shell session in the container environment, as detailed below.

**Note:** singularity is not installed on the Slurm login node and therefore containers can only be accessed from worker nodes, either through job submissions using `sbatch` or using the `sinteractive`/`srun` command for interactively running a job on a worker node.

#### 1. Execute software in a container

A user is able to execute a script using the software from the container environment using the singularity `exec` command. From the Slurm login node, if you want to try the commands, you'll first need to allocate some resources on a compute node to yourself using the following:
```bash
$ sinteractive
```
This will place you on the development node `compute-001`. Singularity is then available and you could execute a Python script using the `python` software in a container, for example:
```bash
$ singularity exec /idia/software/containers/ASTRO-PY3.10.sif python myscript.py
hello world!
$
```
This command will execute the script, `myscript.py`, using the Python software that is contained within the `ASTRO-PY3.10.sif` container. The script will have access to all the Python libraries that have been included in the container.

Similary, the following will execute `print("hello world!")` using the CASA software package that is contained in the `casa-stable-v6.sif` container. Note that once the script has been run successfully the container session is closed automatically. **The `singularity exec` command is widely used to run commands in jobs submitted on Slurm**.

```bash
$ singularity exec /idia/software/containers/casa-stable-v6.sif casa --log2term --nologger -c 'print("hello world!")'

optional configuration file not found, continuing CASA startup without it

No event loop hook running.
Using matplotlib backend: agg
CASA 6.7.0.31 -- Common Astronomy Software Applications [6.7.0.31]
...
hello world!
```

#### 2. Interactive shell command

A user is able to open a Singularity container as an interactive shell and issue command line tasks within the environment that the container provides. To do this a user calls the Singularity container using the `shell` command. You can open a shell session within an available container using the following:
```bash
$ singularity shell /idia/software/containers/SoFiA2v2.5.1.sif 
SoFiA2v2.5.1.sif:~$ sofia
____________________________________________________________________________

 Pipeline started
____________________________________________________________________________

  Using:    Source Finding Application (SoFiA)
  Version:  2.5.1 (24-Jun-2022)
  CPU:      1 thread available
  Time:     Tue Oct 21 11:36:38 2025
```

This command will spawn a new shell inside the container, in this case the `SoFiA2v2.5.1.sif` container, allowing the user to interact with the container environment. The user can then run software that is housed in the container and develop workflows interactively.

For further information on the software environments available on ilifu, including [modules](tech_docs/software_environments?id=environment-modules) and [virtual environments](tech_docs/software_environments?id=python-virtual-environments), please see the supported [Software environments](tech_docs/software_environments.md) documentation.