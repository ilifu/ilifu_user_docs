# Specifying Resources when Running Jobs on Slurm

See the [Submitting a job on Slurm](getting_started/submit_job_slurm) section for information on how to [submit a batch job](getting_started/submit_job_slurm?id=submitting-a-job-using-a-batch-script), or how to start an [interactive job](getting_started/submit_job_slurm?id=interactive-slurm-sessions) in the ilifu Slurm cluster. See a [Summary of ilifu services or partitions and their use case](getting_started/access_ilifu?id=summary-of-ilifu-services-or-partitions-and-their-use-case) for information about the different partitions.

This section provides more details on [available resources](#available-resources) in Slurm, including the default and resource limits, and how to [customise your jobs with Slurm job parameters](#customising-your-job-using-sbatchsrun-parameters). Information on [parallel computing](#parallel-computing-on-the-cluster) and [GPUs](#notes-for-gpu-jobs), as well as the use of [temporary files](#temporary-files), is included below.

### Available resources

When running a job using `sbatch` or `srun`, a user is able to specify the resources required for their job. The following table lists the different node sizes in the cluster and indicates the maximum number of resources that can be requested for the different node types.

| Partition | Node names        | Default CPUs| Max CPUs| Default Memory (GiB) | Max Memory (GiB) | Default wall-time | Max wall-time |
|-----------|-------------------|-------------|---------|----------------------|------------------|-------------------|---------------|
| Main      | compute-[002-021] | 1           | 32      | 3                    | 232              | 3 hours           | 14 days       |
| Main      | compute-[101-105] | 1           | 48      | 3                    | 232              | 3 hours           | 14 days       |
| Main      | compute-[201-260] | 1           | 32      | 3                    | 251              | 3 hours           | 14 days       |
| HighMem   | highmem-[001-002] | 1           | 32      | 15                   | 503              | 3 hours           | 14 days       |
| HighMem   | highmem-003       | 1           | 96      | 15                   | 1508             | 3 hours           | 14 days       |
| HighMem   | highmem-[004-007] | 1           | 32      | 15                   | 503              | 3 hours           | 14 days       |
| HighMem   | highmem-008       | 1           | 32      | 15                   | 1007             | 3 hours           | 14 days       |
| GPU       | gpu-[001-004]     | 1           | 32      | 7                    | 232              | 3 hours           | 14 days       |
| GPU       | gpu-005           | 1           | 24      | 7                    | 232              | 3 hours           | 14 days       |
| GPU       | gpu-006           | 1           | 48      | 7                    | 354              | 3 hours           | 14 days       |
| GPU       | gpu-007           | 1           | 48      | 7                    | 354              | 3 hours           | 14 days       |
| GPU       | highmem-008       | 1           | 32      | 7                    | 1007             | 3 hours           | 14 days       |
| Devel     | compute-001       | 1           | 32      | -                    | -                | 3 hours           |  5 days       |

*Note jobs submitted to the Devel partition cannot allocate memory.*

The GPU nodes include NVIDIA P100 (gpu-[001-004]), V100 (gpu-005), two A40s (gpu-006, highem-008) and A100 (gpu-007). To submit a job on a specific GPU node, the `-w` or `--nodelist` parameter may be used, with a list of the relevant `Node names`. Alternatively, the `-C` or `--constraint` parameter may be used, with the list of constraints or tags, as indicated in the table below:

| Partition | Node names        | GPU type    | Constraint/Tag | Number of GPUs per node | GPU Memory (GiB) |
|-----------|-------------------|-------------|----------------|-------------------------|------------------|
| GPU       | gpu-[001-004]     | P100        | P100,p100      | 2                       | 12               |
| GPU       | gpu-005           | V100        | V100,v100      | 1                       | 32               |
| GPU       | gpu-006           | A40         | A40,a40        | 1                       | 45               |
| GPU       | gpu-007           | A100        | A100,a100      | 1                       | 40               |
| GPU       | highmem-008       | A40         | A40,a40        | 1                       | 45               |

### Parallel computing on the cluster

If you are running a normal job on Slurm, **without** `MPI` or `OpenMP`, your job will only require `1 CPU`, `1 task` and `1 node`. These values are default values when running a job, however you are able to specify additional memory for your job using the `--mem` parameter.

Parallelism on the cluster can be achieved on a single node or over multiple nodes. Parallelism on a single node distributes work over multiple CPUs and is typically implemented using `OpenMP`. If you are running a job with software that utilizes `OpenMP` on Slurm, you can increase the number of CPUs for your job to > 1 CPU, while still using `1 task` and `1 node`. You may need to `export OMP_NUM_THREADS=<N>` to specify the number of threads the software will utilize.

Parallelism on the cluster can also occur by distributing work over many tasks that operate on 1 or more nodes. This type of parallelism is typically implemented using `MPI`. If you are running a job with software that utilizes `MPI` on Slurm, you can increase the number of `tasks` your job uses, `> 1 task`, while `nodes` and `CPUs` can be 1. The number of CPUs per task can be specified. You can increase the number of nodes if you want more than the maximum available resources on a single node.

When using MPI, you must wrap your software call (including Singularity) in an MPI wrapper, such as mpirun, for example:

```bash
#!/bin/bash
#SBATCH --job-name='MPI-job-%J'
#SBATCH --ntasks=16
#SBATCH --cpus-per-task=1

module load openmpi/4.1.0
mpirun -n <number of processes to run> singularity exec <path/to/container> </path/to/binary/within/container>
```

It is important to note that when running jobs in parallel using a container, the container must also have `MPI` installed in it and the version and implementation inside the container must be the same as the version used on the cluster. Please keep this in mind if building a new container intended for parallel jobs, and select an `MPI` implemtation this is supported on ilifu. There are a number of versions of `openmpi` supported, as well as a single version of `mpich`. View available versions by running `module avail`.

A detailed guide on parallelism on the cluster can be found in the [ilifu User Training video](https://www.ilifu.ac.za/latest-training/#training-advanced2) and [presentation slides](https://docs.ilifu.ac.za/training/2025/ilifu_online_training_session3_20250916_presentation1.pdf). 

### Customising your job using sbatch/srun parameters

The following table lists the parameters that can be used to describe the required resources for your job. Additional parameters can be found by running `sbatch --help` or `srun --help`.

<summary id='slurm-job-parameters'></summary>

| Syntax                                                                               | Meaning                                         		      |
|--------------------------------------------------------------------------------------|--------------------------------------------------------------|
| --time=&#60;minutes&#62;<sup>1</sup>                                                 | Walltime for job (default is 3 hrs)                          |
| --mem=&#60;number&#62;<sup>2,11</sup>                                                | Maximum amount of memory per node                            |
| --mem-per-cpu=&#60;number&#62;<sup>2,3,11</sup>                                      | Memory per processor core (CPU)						      |
| --cpus-per-task=&#60;number&#62;<sup>3,4,11</sup>                                    | Number of CPUs per task (default is 1)                       |
| --ntasks=&#60;number&#62;<sup>4</sup>                                                | Number of processes to run (default is 1)          	      |
| --nodes=&#60;number&#62;<sup>5,11</sup>                                              | Number of nodes on which to run (default is 1)     	      |
| --ntasks-per-node=&#60;number&#62;<sup>4,5</sup>                                     | Number of tasks to invoke on each node            		      |
| --partition=&#60;partition_name&#62;<sup>6</sup>                                     | Request specific partition/queue (default Main)    	      |
| --account=&#60;account_name&#62;<sup>7</sup>                                         | The account that will be charged for the job       	      |
| --gres=&#60;resource_type&#62;:&#60;resource_name&#62;:&#60;number&#62;<sup>8</sup>  | Specify type and number of generic resources       	      |
| --output=&#60;file_name&#62;<sup>9</sup>                                             | File to write standard output to                   	      |
| --error=&#60;file_name&#62;<sup>9</sup>                                              | File to write standard error output to             	      |
| --mail-user=&#60;email_address&#62;<sup>10</sup>                                     | email address where notifications should be sent   	      |
| --mail-type=&#60;event_types&#62;<sup>10</sup>                                       | list of events that should send email notification 	      |
<!-- also include row for array jobs -->

*default parameters, if not specified, include: 1 node, 1 task, 1 CPU, 3 hrs, and the Main partition. Default memory scales with the number of CPUs specified, and by default (for 1 CPU), is 7.25 GB on Main nodes, 15 GB on HighMem nodes, and unallocated the Devel node.*

1. While the default for specifying the wall-time for a job is in minutes, it can also be specified as `mm:ss`, `hh:mm:ss` and even `days-hh:mm:ss`. Wall-time is the estimated amount of time that you expect your job to run. It is important for the scheduler to know this parameter so that it can make realistic estimates on when jobs are due to start and end. This is especially critical for your short jobs as it can allow them to run earlier when a node would otherwise be idle waiting for a large job to start. Note, however, that underestimating wall-time means that once your job has exceeded its limit, it will be killed. So it’s better to slightly overestimate the amount of time, especially taking into account that the runtime of jobs can vary a bit due to overall system load.
2. The default units for memory is MB, but can be specified explicitly in GB, for example `--mem=16GB`. This parameter is especially important in jobs where you are not using the whole node, i.e. jobs using fewer than 32 cores, as this allows other jobs to run alongside yours and make more efficient use of the resources.
3. CPUs refers to the the number of CPUs associated with your job.
4. a task is an instance of a running program, and generally you will only want one task, unless you use software with MPI support (for example MPICASA), Slurm works with MPI to manage parallelised processing of data.
5. nodes refers to a single compute node or Slurm worker, i.e. one node that has 32 CPUs and 232 GB RAM
6. The partition is the specific part of the cluster your job will run. You will only set this if you are [running a GPU job](#notes-for-gpu-jobs).
7. To find your default account you can run the command `sacctmgr show User -p | grep ${USER}`, while the command `sacctmgr show Associations User=${USER} -p | cut -f 2 --d="|"` will show all your valid accounts. Note that it is only important that you set the account parameter if you are associated with more than one project on the cluster. You can change your default account using `sacctmgr modify user name=${USER} set DefaultAccount=<account>`, where `<account>` is one of your valid accounts.
8. Request generic resource (per node). You will only use this if you are [running a GPU job](#notes-for-gpu-jobs).
9. The filename can include `%j`, which will be substituted with the job's ID.
10. Email notifications can optionally be sent when a job's state changes. Create a comma-separated list with at least one of the following notification types: `NONE`; `BEGIN`; `END`; `FAIL`; `REQUEUE`; `ALL` (equivalent to `BEGIN,END,FAIL,REQUEUE,STAGE_OUT); STAGE_OUT`; `TIME_LIMIT`; `TIME_LIMIT_90` (reached 90 percent of time limit); `TIME_LIMIT_80` (reached 80 percent of time limit); `TIME_LIMIT_50` (reached 50 percent of time limit); and `ARRAY_TASKS`. ARRAY_TASKS will mean that a notification will be sent for each task in a job array (the default is only for the job array as a whole.)
11. **Note that if you specify more memory or cores than is available on the nodes, or more nodes than are available on the cluster, _your job will never start but it will sit in the queue!_**

### Notes for GPU jobs

If you wish to run a job on a GPU node you need to specify the `GPU` partition using `--partition=GPU`; as well as indicate the number of GPU resources you require using `--gres=gpu:<number_of_gpus>`. The number of GPUs you can request depends on the GPU node type you are using — some have a single GPU while others have two. The following example requests one GPU on a GPU node:

```bash
#SBATCH --partition=GPU
#SBATCH --gres=gpu:1
``` 

You can also get the properties of the GPU node using `scontrol show node <node_name>`, which will show you the number of GPUs available on that node, as well as the GPU type and memory available. For example, to get the properties of the `gpu-001` node, you would run:

```bash
$ scontrol show node gpu-001
NodeName=gpu-001 Arch=x86_64 CoresPerSocket=16 
   CPUAlloc=24 CPUEfctv=32 CPUTot=32 CPULoad=24.00
   AvailableFeatures=p100,P100
   ActiveFeatures=p100,P100
   Gres=gpu:2(S:0-31)
   NodeAddr=gpu-001 NodeHostName=gpu-001 Version=23.11.6
   OS=Linux 5.15.0-91-generic #101-Ubuntu SMP Tue Nov 14 13:30:08 UTC 2023 
   RealMemory=237568 AllocMem=178176 FreeMem=221788 Sockets=2 Boards=1
   State=MIXED ThreadsPerCore=1 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
   Partitions=GPU 
   BootTime=2025-05-30T05:41:42 SlurmdStartTime=2025-05-30T05:44:29
   LastBusyTime=2025-06-24T07:17:18 ResumeAfterTime=None
   CfgTRES=cpu=32,mem=232G,billing=1763704832,gres/gpu=2
   AllocTRES=cpu=24,mem=174G,gres/gpu=1
   CapWatts=n/a
   CurrentWatts=0 AveWatts=0
   ExtSensorsJoules=n/a ExtSensorsWatts=0 ExtSensorsTemp=n/a
```

Two lines of interest here are:
```
   Gres=gpu:2(S:0-31)
```
which shows that there are two GPUs available on this node, and that they are available on all 32 cores of the node (S:0-31); and
```
   AvailableFeatures=p100,P100
```
which shows that this node has two P100 GPUs available.

Note that one can select nodes based on the GPU type using the `--constraint` parameter, for example:

```bash
#SBATCH --partition=GPU
#SBATCH --gres=gpu:1
#SBATCH --constraint=p100
```

This will select a node with a P100 GPU. Alternatively if you prefer a specific type of GPU but are open to other types one can use `--prefer=p100` which will preferentially choose a p100 nodes, however if none are available then something else may be used. Please see the [Available resources](#available-resources) section above for more information on the available GPU nodes and their properties.

### Temporary files

Temporary files are files that are not intended to be kept permanently. They are often used for intermediate data, temporary storage, or caching purposes. In the context of ilifu, temporary files can be created during data processing, job execution, or other operations and should be managed carefully to avoid unnecessary storage usage.

In addition to the scratch storage described in the [Directory structure](data/directory_structure.md#scratch-storage) section, many applications and jobs will, by default, create temporary files in the user's home directory, in the job's working directory and in the `/tmp/` system directory. These files can accumulate over time and consume significant disk space. It is important to regularly clean up these temporary files to maintain a healthy storage environment. `/tmp/` is especially important to clean up as it is shared by all users and can fill up quickly, leading to system issues and should be avoided if at all possible.

#### Using `/dev/shm/` for temporary files
The `/dev/shm/` directory is a temporary filesystem (tmpfs) that is used for shared memory in Linux. It is often used for storing temporary files that need to be accessed quickly. The advantage of using `/dev/shm/` is that it is stored in RAM, which makes it much faster than disk-based storage. But in order to use it effectively, you need to ensure that the size of `/dev/shm/` is sufficient for your needs — and this will come out of your memory allocation for the job. So if you are running a job that requires a lot of temporary storage, you should ensure that the job is allocated enough memory to accommodate the size of `/dev/shm/` in addition to the memory required for the job itself.

Below is an example of how to use `/dev/shm/` for temporary files in a Slurm job script:

```bash
#!/bin/bash
#SBATCH --job-name=my_temp_job
#SBATCH --mem=8G

TMPDIR=`mktemp /dev/shm/${USER}.XXXXX -d`  # this creates a temporary directory in /dev/shm and stores the path in TEMPDIR
TMP=${TMPDIR}
TEMP=${TMPDIR}
export TMPDIR TMP TEMP  # this exports variables for jobs that may use them

# Your job commands go here
# For example, running a command that allows you to specify the temporary directory
my_command --temp-dir ${TMPDIR} some_input_file

# Clean up the temporary directory after the job is done
rm -rf ${TMPDIR}
```

This script creates a temporary directory in `/dev/shm/`, sets the necessary environment variables, runs a command that uses the temporary directory, and then cleans up the temporary directory after the job is done.