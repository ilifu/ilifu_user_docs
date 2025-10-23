# Resource allocation

Resources on the ilifu Research Facility are shared amongst all members of our user community. In order to support our users and the diverse range of projects that we host, it is important to make efficient use of these resources. The three primary compute resources available on the cluster include CPUs<sup>1</sup> , memory and wall-time<sup>2</sup> . These resources are allocated when running a job on Slurm or using the Jupyter service.

*Notes: 1. The majority of ilifu Slurm nodes have two CPUs (sockets), each with 16 cores, giving 32 cores overall. However, Slurm tends to just call these CPUs instead of cores, which we adopt from here on. 2. The wall-time or elapsed time is the total run time of your job according to a clock on the wall. When using more than one CPU, it differs from the CPU time, measured in CPU hours.*

Efficient use of resources essentially means only using what you require. Accurately determining your resource requirements will avoid wasting resources that are allocated but not used, allowing those resources to be used by other users, increasing resource availability, and potentially reducing your job wait time. Accurate resource allocation also improves the efficiency of the Slurm scheduler and its ability to assign resources to jobs. Furthermore, resource usage on the cluster is charged against your user account and affects your job priority (see information on [fairshare](tech_docs/fairshare)). By accurately specifying your job resources you can ensure a higher priority for your job submissions.

The process of accurately determining the resource requirements for a job can be broken down into three measures:
* profiling resource usage of previous similar jobs;
* running a small test job and determining how your job performance scales with resources;
* determining whether the software you want to run uses parallel computing, and in what form (detailed in CPU allocation section below).
 
When allocating resources to a job, it is important to consider the requirements, and check the resource usage of previous similar jobs. Profiling resources usage of past jobs is detailed in the sections below. 

A good starting point when considering how to allocate resources is to start with a small test job (e.g. a small resource allocation on a small subset of your data), test the wall-time, run again with increased resources (e.g. CPUs/tasks and possibly memory), and repeat this process to see how the wall-time scales with resources. By the end, you should have a good idea of an efficient use of resources for your full data set. 

Most processes do not scale linearly (or even close to it), so it is important to find a middle ground between performance and efficient use of resources. In most cases, the maximum performance (i.e. shortest wall-time) is not an efficient choice, given the large allocation necessary for such performance. Even larger allocations for MPI jobs (multi-node jobs) may end up taking longer due to the scatter/gather overhead associated with partitioning the data/work. In general, breaking your process up into many small independent jobs (a high-throughput computing approach) is most efficient.

## Maximum allocation
As outlined in the [ilifu documentation](tech_docs/running_jobs#specifying-resources-when-running-jobs-on-slurm), nodes in the Slurm cluster are grouped under different partitions, with different resources and purposes for each partition. Below is a summary of the resources available in each partition, showing the maximum values that can be allocated to a job, as well as the default values. This information can also be listed with:

```bash
scontrol show partition
```
*Table 1. The different Slurm partitions and their resources, listing the default and maximum allocations. Default memory scales with the number of CPUs allocated. Jobs submitted to the Devel partition cannot allocate memory.*

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

The GPU nodes include NVIDIA P100 (gpu-[001-004]), V100 (gpu-005), A40 (gpu-006) and A100 (gpu-007). To submit a job on a specific GPU node, the `-w` or `--nodelist` parameter may be used, with a list of the relevant `Node names`. Alternatively, the `-C` or `--constraint` parameter may be used, with the list of constraints or tags, as indicated in the table below:

*Table 2. Available GPUs and their resources.*

| Partition | Node names        | GPU type    | Constraint/Tag | Number of GPUs per node | GPU Memory (GiB) |
|-----------|-------------------|-------------|----------------|-------------------------|------------------|
| GPU       | gpu-[001-004]     | P100        | P100,p100      | 2                       | 12               |
| GPU       | gpu-005           | V100        | V100,v100      | 1                       | 32               |
| GPU       | gpu-006           | A40         | A40,a40        | 1                       | 45               |
| GPU       | gpu-007           | A100        | A100,a100      | 1                       | 40               |
| GPU       | highmem-008       | A40         | A40,a40        | 1                       | 45               |

Note that if a job uses all the CPUs or all the available memory on a node, that node becomes fully allocated and no other jobs can be run on the node for the duration of the job. This means that any unused CPU or memory resources cannot be used by another job, including your own. Therefore, if you have a job that has a high CPU requirement and a low memory footprint, or a large memory requirement but a low CPU requirement, consider not allocating the maximum available CPU or memory, respectively, and allow a little headroom for other jobs to be allocated to the node.

## Finding your job ID

In order to profile your previous jobs when submitting a similar job, you may need to find the ID of a previous job to display the usage statistics. Firstly, check if any logs were written into your working directory, which typically include the job ID. Otherwise, search for your job ID within the time range that you submitted the job, using sacct. For example:

```bash
sacct -X --name=my-job --starttime=YYYY-MM-DD --endtime=YYYY-MM-DD
```

This will display one line for every job with that name submitted during that time range, including the job ID, which can then be used to display other usage statistics. The `--name` parameter can be omitted to view all jobs that were run between the specified start and end time. To query very old jobs from the previous ilifu Slurm cluster builds, add the `--cluster=ilifu-slurm20` or `--cluster=ilifu-slurm` parameter.

## Memory allocation

When allocating memory, run one of the scaling tests mentioned above, or check the memory usage of previous similar jobs. Once you have determined your memory requirements, you should allocate this amount of memory to future jobs with a small (~10-20%) buffer, to avoid your job resulting in an out-of-memory (`OOM`) error. You should avoid allocating excessive memory, as this is an inefficient use of resources and reduces resource availability on the cluster. 

The maximum memory usage of a job, as sampled every 20 seconds, is given by the `MaxRSS` statistic. For a job (e.g. `jobID 123456`) that is running, this can be listed with

```bash
sstat -j 123456 -o MaxRSS
```

Which is given in units of kB. To calculate this in GB, divide the value by 1024<sup>2</sup>. 

For jobs that have been previously run, you can list the `MaxRSS` with
```bash
sacct -j <jobid> --unit=G -o JobID,JobName,MaxRSS,ReqMem
```

This will also list your requested memory (`ReqMem`) and the unit (e.g. `12 Gn` = 12 GB per node, or `7.25c` = 7.25 GB per core), for comparison to the used memory. By default, if the memory is unset (or `--mem=0`), it will use the default memory per CPU (`DefMemPerCPU`), which is 7.25 GB for a Main node, and 15 GB for a `HighMem` node. For a job with 32 CPUs, this uses all of the memory.

## CPU allocation

When selecting the number of  CPUs for a job, the first thing to consider is whether the software your job uses makes use of any parallelism. Many / most packages do not use any parallelism and require only a single CPU. In this case, only a single CPU should be allocated to your job. Some software packages make use of CPU-level parallelism on a single node (with software like OpenMP). In this case multiple CPUs can be allocated, but a single node should be used. Other packages make use of task-level parallelism over one or more nodes, using MPI, in which case multiple tasks/nodes can be allocated. Some specialised software makes use of both, allowing for the use of multiple CPUs and multiple tasks/nodes. For more information, such as the syntax for setting these parameters, please read our [Slurm documentation](tech_docs/running_jobs#specifying-resources-when-running-jobs-on-slurm).

To determine CPU requirements, for running jobs, you can ssh onto the node(s) where the job is running (listed with `squeue -u $USER`) and run the following command:

```bash
htop -u $USER
```

This gives a dashboard of computing resources for your different (e.g. master and spawned) processes that are running on the node, and allows you to monitor how the resource usage of your job progresses in real time. To ssh onto the node, you must have a job running on that node, and you must enable authentication forwarding when you first ssh onto the cluster using the `-A` parameter (`ssh -A <username>@slurm.ilifu.ac.za`).

Similar to sacct, for jobs that have been previous run, you can list the efficiency of your job’s use of compute resources with

```bash
seff <jobid>
```

This will display the CPU and memory efficiency as a percentage between allocated/requested and used resources. The used memory within this calculation is taken from the MaxRSS. 

## Wall-time allocation

Using an accurate wall-time improves the efficiency of the scheduler and how it allocates jobs to cluster resources. While wall-time can be  difficult to estimate, a good starting point, similar to the scaling tests mentioned above, is to test your job with a large allocation, see the resulting wall-time, and then run future equivalent jobs with a reduced wall-time, allowing for a ~20-30% buffer. Accurately specifying job wall-time may decrease your job wait time, but may result in your job timing out (hence the suggested buffer). If you under-estimate your wall-time and need your job wall-time to be increased, please contact ilifu Support to see if it is possible to increase the time limit of your running job. 

## Account allocation
Each project supported on ilifu has a corresponding Slurm accounting group, against which resource usage is charged. If you are a member of multiple projects on the ilifu cluster, it is important to select the correct project accounting group when submitting a job. A project’s Slurm accounting group affects the priority and therefore the scheduling of jobs (based on [fairshare](tech_docs/fairshare)), and allows accurate recording of job data within the Slurm database and ilifu reporting database. For example, if you belong to multiple projects, but charge all your resource usage to a single project, that project’s fairshare value will decrease and further jobs submitted under that project’s accounting group will have reduced priority in the Slurm queue. If accounting groups are correctly specified, fairshare values accurately reflect project resource usage, and access to resources is more fairly distributed amongst projects and users.

You can list your accounting groups, corresponding to the different ilifu projects in which you’re involved, using the following:

```bash
sacctmgr show user $USER cluster=ilifu-slurm2021 -s format=account%25
```

Your default account, used when no accounting group is specified, can be viewed with:

```bash
sacctmgr show user $USER
```

You can change your default account using:

```bash
sacctmgr modify user name=${USER} set DefaultAccount=<account>
```

When submitting a job, your account can be specified within the Slurm parameter `--account` (following `#SBATCH` within sbatch jobs). For example: `--account=b05-pipelines-ag`
