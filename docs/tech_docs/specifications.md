# System Specifications

The Ilifu infrastructure includes the following compute and storage resources:

## Compute
    * 111 x compute nodes, 32 CPUs, 256 GB RAM
    * 2 x compute nodes, 32 CPUs, 512 GB RAM
    * 3 x GPU nodes, 32 CPUs, 256 GB RAM, 2 x Tesla P100 16 GB GPU

## Storage
    * 400 TB BeeGFS (fast storage mounted as /scratch)
    * 2.9 PB CephFS.


Of the 111 compute nodes, 88 nodes are included in the Ilifu SLURM cluster, with 76 nodes in the main partition and 12 nodes in the Jupyter partition. The number of nodes within the cluster and allocated to partitions is subject to change as the nodes are moved between partitions and other services as needs demand. Additional CephFS storage of approximately 2.8 PB will be available by October 2020. The CephFS storage values indicate usable storage and are calculated as 70% of raw available storage to allow for redundancy and file-system overheads. Usable storage is intended to operate at below 80% capacity for the storage to operate efficiently.