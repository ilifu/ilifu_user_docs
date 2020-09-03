# Directory structure

The following describes the directory structure as related to the ilifu data policies.

Users' home directories are located in `/users/`. This directory is for users' scripts. No large files should be stored in `/users/`. It is recommended that users make use of a repository such as Github to backup scripts and files.

`/scratch` and `/scratch2` are the primary directories for data processing. These directories are for **short-term** storage only. Only temporary data required for processing should be copied here. After processing, data products should be moved to the relevant project or group directory, and intermediate data products should be removed **immediately**. **No files or data should remain in the scratch directories when not actively working.**

`/scratch/users/<username>` is a users' specific directory for data processing.

`/scratch/projects/<project_name>` is for data processing related to a project where multiple users will be involved in the data processing. `/scratch/projects/` directories are created on request.

`/software` contains common software packages needed for workflows, including containers and modules.

There are a number of groups within the ilifu cloud computing community, including IDIA, CBIO and SANBI among others. For **medium- and long-term storage**, the directory structure has been broken down by group.

### IDIA directory structure

* `/idia/` - the base directory for all IDIA related projects.

* `/idia/users` - user's personal workspace. **Limited to 10TB**. For storing longer-term data and data products.

* `/idia/projects/` - project specific directories. These directories are for sharing data and resources within project groups. Project archive data, data products, intermediate data and project specific resources, such as script or software containers, are stored here. Raw data associated with a project will also be available from the project folder. Raw data folders should always be read-only.

* `/idia/raw/` - raw data (read-only data) is stored here. Raw data, from SARAO is moved into access controlled project directories within `/idia/raw/`. This data is retrievable from SARAO and therefore will not be included in backup procedures. Symbolic links to the raw data will be accessible from the project directory.

* `/idia/software/` - astronomy [software containers](tech_docs/software_environments?id=singularity-containers) and the [IDIA Pipelines](https://idia-pipelines.github.io/) software is stored here.

* `/idia/data/public` - public data and data products available to all users are stored here.

### CBIO directory structure

Users' home directories are in `/users/`. This is not currently backed up.

CBIO users will be using the CephFS parallel file partition — our space is in `/cbio/`. Directories that have been setup:
* `/cbio/users` - user's personal workspace. **Limited to 10TB**. Working in a project space allows storage space to be used more efficiently. Please see the [Data Management Form](/bioinformatics/cbio#data-management-plan-for-projects) in regard to data management plan for projects.
* `/cbio/projects` - project specific directories. These directories are for sharing data and resources within project groups. Project archive data, data products, intermediate data and project specific resources, such as scripts , are stored here.
* `/cbio/dbs` - general-purpose annotation and reference databases are stored here. Most `dbs` will be open but some may be accessed controlled e.g in `/cbio/dbs/refpanels/`.
* `/cbio/datasets` - Access controlled datasets are stored here e.g. SAHGP, Baylor, AGVP.
* `/cbio/soft` - Software that is needed to run workflows is installed here; most of our other software will be encapsulated into singularity images.
* `/cbio/images` - shared singularity images are stored here.

Please note the [restrictions](/bioinformatics/cbio#restrictions).

### ilifu directory structure (excluding IDIA and CBIO projects)

* `/ilifu/` - the base directory for all ilifu related projects.

* `/ilifu/users` - user's personal workspace.

* `/ilifu/astro/projects/` and `ilifu/bio/projects` - project specific directories. These directories are for sharing data and resources within project groups. Project raw data, data products, intermediate data and project specific resources, such as script or software containers, are stored here. It is recommended that raw data folders should always be read-only.

* `/ilifu/software/` - Software not in containers can be installed here.

* `/ilifu/software/containers` - [software containers](tech_docs/software_environments?id=singularity-containers) can be stored here. Note there is a symbolic link here to the IDIA astronomy containers in `/idia/software/containers`.


