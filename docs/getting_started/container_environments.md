# Singularity Containers

Containers are unit software packages that contain all the software, files, libraries, dependencies and environmental variables necessary to run a particular task or workflow. Containers are encapsulated software environments and abstract the software and applications from the underlying operating system. This allows users to run workflows in customized environments, switch between environments, and to share these environments with colleagues and research teams.

The container images that are maintained by the support team can be found at `/idia/software/containers/`. There are a number of ways one can use a Singularity container, including both interactive and non-interactive sessions, as detailed below.

**Note:** singularity is not installed on the SLURM headnode and therefore containers can only be accessed from worker nodes, either through job submissions using `sbatch` or using the `srun` command for interactively running a job on a worker node.

## Interactive shell command

A user is able to open a Singularity container as an interactive shell and issue command line tasks within the environment that the container provides. To do this a user calls the Singularity container using the `shell` command.

From the SLURM login node, first allocate a compute node to yourself using the following:
```shell
$ srun --pty bash
```

Singularity is then available from the compute node. You can open a session within an available container using the following:

```shell
$ singularity shell /idia/software/containers/casa-stable.img
Singularity: Invoking an interactive shell within container...

Singularity casa-stable-5.1.1.img:~>
```

This command will spawn a new shell inside the container, in this case the `casa-stable` container, allowing the user to interact with the container environment. The user can then run software that is housed in the container and develop workflows interactively.

## Exec command

A user is able to execute a script within the container environment using the singularity `exec` command.

```shell
$ singularity exec /idia/software/containers/sourcefinding_py3.simg python myscript.py
hello world!
$
```

This command will execute the script, `myscript.py`, using Python within the `sourcefinding_py3` container. The script will have access to all the Python libraries that have been included in the container.

Similary,

```shell
$ singularity exec /idia/software/containers/casa-stable.img casa --log2term --nologger -c "print 'hello world'"

=========================================
The start-up time of CASA may vary
depending on whether the shared libraries
are cached or not.
=========================================

IPython 5.1.0 -- An enhanced Interactive Python.

CASA 5.1.1-5   -- Common Astronomy Software Applications

2019-04-01 13:49:49     INFO    ::casa  CASA Version 5.1.1-5
--> CrashReporter initialized.
hello world
$
```

will execute `print 'hello world'` using the CASA software package that is contained in the `casa-stable` container. Note that once the script has been run successfully the container session is closed automatically. The `singularity exec` command is widely used to submit jobs on SLURM. 

The `exec` command can also be used to initiate an interative session. For example:

```shell
$ singularity exec /idia/software/containers/casa-stable.img casa --log2term --nologger

=========================================
The start-up time of CASA may vary
depending on whether the shared libraries
are cached or not.
=========================================

IPython 5.1.0 -- An enhanced Interactive Python.

CASA 5.1.1-5   -- Common Astronomy Software Applications

2019-04-01 13:51:39     INFO    ::casa  CASA Version 5.1.1-5
--> CrashReporter initialized.
Enter doc('start') for help getting started with CASA...
Using matplotlib backend: TkAgg

CASA <1>:

```

The above command will run the CASA software within the `casa-stable` container environment and will allow the user to use the environment interactively. However, the primary use of the `exec` command is to execute scripts without interaction, for example on the SLURM cluster.

For further information on the software environments available on ilifu please see the [Supported software environments](tech_docs/software_environments.md) documents.
