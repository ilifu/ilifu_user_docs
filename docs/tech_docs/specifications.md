# System Specifications

The Ilifu infrastructure includes the following compute and storage resources:

## Compute
    * 110 x compute nodes, 32 CPUs, 256 GB RAM
    * 2 x compute nodes, 32 CPUs, 512 GB RAM
    * 5 x compute nodes, 48 CPUs, 256 GB RAM
    * 4 x GPU nodes, 32 CPUs, 256 GB RAM, 2 x Tesla P100 16 GB GPU
    * 1 x GPU node, 24 CPUs, 256 GB RAM, 1 x Tesla V100 32 GB GPU
    * 1 x GPU node, 48 CPUs, 348 GB RAM, 1 x NVIDIA A40 48 GB GPU
    * 1 x GPU node, 32 CPUs, 1024 GB RAM, 1 x NVIDIA A40 48 GB GPU
    * 1 x GPU node, 48 CPUs, 348 GB RAM, 1 x NVIDIA A100 40 GB GPU
    * 1 x compute node, 96 CPUs, 1.5 TB RAM

## Storage
    * 8.8 PiB CephFS

Of the 110 compute nodes, 95 nodes are included in the Ilifu Slurm cluster, with 82 nodes in the main partition and 13 nodes in the Jupyter partition. The number of nodes within the cluster and allocated to partitions is subject to change as the nodes are moved between partitions and other services as needs demand. The CephFS storage values indicate usable storage and are calculated as 65% of raw available storage to allow for redundancy and file-system overheads.