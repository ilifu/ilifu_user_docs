
# Data Policies

The following describes the directory structure as related to the ilifu data policies.

## Directory structure

Users' home directories are located in `/users/`. This directory is for users' scripts. No large files should be stored in `/users/`. It is recommended that users make use of a repository such as Github to backup scripts and files.

`/scratch/` is the primary directory for data processing. `/scratch/` is for **short-term** storage only. Only temporary data required for processing should be copied here. After processing, data products should be moved to the relevant project or group directory, and intermediate data products should be removed **immediately**.

`/scratch/users/<username>` is a users' specific directory for data processing.

`/scratch/projects/<project_name>` is for data processing related to a project where multiple users will be involved in the data processing. `/scratch/projects/` directories are created on request.

There are a number of groups within the ilifu cloud computing community, including IDIA, CBIO and SANBI among others. For **medium- and long-term storage**, the directory structure has been broken down by group.

Information relating to the CBIO group directory structure can be found [here](https://docs.ilifu.ac.za/#/cbio/setup).

### IDIA directory structure

`/idia/` - the base directory for all IDIA related projects.

`/idia/projects/` - project specific directories. These directories are for sharing data and resources within project groups. Project archive data, data products, intermediate data and project specific resources, such as script or software containers, are stored here. 

`/idia/raw/` - raw data (read-only data) is stored here. Raw data, from SARAO is moved into access controlled project directories within `/idia/raw/`. This data is retrievable from SARAO and therefore will not be included in backup procedures.

`/idia/software/` - [software containers](https://docs.ilifu.ac.za/#/cluster/software_environments?id=singularity-containers) and the [IDIA Pipelines](https://idia-pipelines.github.io/) software is stored here.

`/idia/public` - data and data products available to all users are stored here.


