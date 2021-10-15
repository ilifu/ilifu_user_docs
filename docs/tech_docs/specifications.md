# System Specifications

The Ilifu infrastructure includes the following compute and storage resources:

## Compute
    * 110 x compute nodes, 32 CPUs, 256 GB RAM
    * 2 x compute nodes, 32 CPUs, 512 GB RAM
    * 5 x compute npdes, 48 CPUs, 256 GB RAM
    * 4 x GPU nodes, 32 CPUs, 256 GB RAM, 2 x Tesla P100 16 GB GPU
    * 1 x GPU node, 24 CPUs, 256 GB RAM, 1 x Tesla V100 32 GB GPU

## Storage
    * 400 TiB BeeGFS (fast storage mounted as /scratch2)
    * 6.6 PiB CephFS


Of the 110 compute nodes, 94 nodes are included in the Ilifu Slurm cluster, with 84 nodes in the main partition and 14 nodes in the Jupyter partition. The number of nodes within the cluster and allocated to partitions is subject to change as the nodes are moved between partitions and other services as needs demand. The CephFS storage values indicate usable storage and are calculated as 80% of raw available storage to allow for redundancy and file-system overheads. Usable storage is intended to operate at below 85% capacity for the storage to operate efficiently.