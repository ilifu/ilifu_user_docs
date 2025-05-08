# Directory structure

The following describes the directory structure as related to the ilifu data policies.

### User home directories

Users' home directories are located in `/users/`, **limited to 200GB**. This directory is for users' scripts. No large files should be stored in `/users/`. It is highly recommended that users make use of a repository such as Github to backup scripts and files.

### Scratch

The scratch mounts are the primary directories for data processing, where large intermediate data products are expected to be generated.
These directories are for **short-term** use only, and have a 90-day auto-deletion policy. This means that **once every month**, we will **automatically delete files from scratch mounts** that have not been accessed for more than 90 days. Only temporary data required for processing should therefore be copied here. After processing, data products should be moved to the relevant project or group directory, and intermediate data products should be removed **immediately**. **No files or data should remain in the scratch directories when not actively working.**.

**Folder locations:**  

`/scratch3/users/<username>` is a users' specific directory for data processing.

`/scratch3/projects/<project_name>` is for data processing related to a project where multiple users will be involved in the data processing. `/scratch3/projects/` directories are created on request.

**Auto-deletion process**

The `/scratch3` auto-deletion process performs a deletion of files that have not been accessed in more than 90 days. Usually the deletion process is run on the third or fourth tuesday of month. Affected users are notified with at least two weekly emails prior to the deletion date. The email includes a summary of files flagged for deletion, as well as a link to text file containing a list of all the flagged files. It is possible for users to request to be excluded from a specific `scratch3` deletion run, but this will have to be motivated in an email to support@ilifu.ac.za. In general exclusion from deletion runs will not be applied multiple months in a row.

### Group Directories

There are a number of groups within the ilifu cloud computing community, including IDIA, CBio and ilifu, among others. For **medium- and long-term storage**, the directory structure has been broken down by group.

**Summary of filesystem quotas:**

| Directory path      | Quota          |
|---------------------|----------------|
| /users ($HOME)      | 200GB          |
| /idia/users/        | 10TB           |
| /cbio/users/        | 10TB           |
| /ilifu/users/       | 2TB            |

`/software` contains common software packages needed for workflows, including containers and modules.


#### IDIA directory structure

* `/idia/` - the base directory for all IDIA related projects.

* `/idia/users` - user's personal workspace. **Limited to 10TB**. For storing longer-term data and data products that are not ready to be placed in shared project space.

* `/idia/projects/` - project specific directories. These directories are for sharing data and resources within project groups. Project long-term data, data products, intermediate data and project specific resources, such as script or software containers, are stored here. Raw data associated with a project will also be available from the project folder. Raw data folders should always be read-only.

* `/idia/raw/` - raw data (read-only data) is stored here. Raw data, from SARAO is moved into access controlled project directories within `/idia/raw/`. This data is retrievable from SARAO and therefore will not be included in backup procedures. Symbolic links to the raw data will be accessible from the project directory.

* `/idia/software/` - astronomy [software containers](tech_docs/software_environments?id=singularity-containers) and the [IDIA Pipelines](https://idia-pipelines.github.io/) software is stored here.

* `/idia/data/public` - public data and data products available to all users are stored here.

#### CBIO directory structure

Users' home directories are in `/users/`. This is not currently backed up.

CBIO users will be using the CephFS parallel file partition — our space is in `/cbio/`. Directories that have been setup:
* `/cbio/users` - user's personal workspace. **Limited to 10TB**. Working in a project space allows storage space to be used more efficiently. Please see the [Data Management Form](/bioinformatics/cbio#data-management-plan-for-projects) in regard to data management plan for projects.

* `/cbio/projects` - project specific directories. These directories are for sharing data and resources within project groups. Project long-term data, data products, intermediate data and project specific resources, such as scripts , are stored here.

* `/cbio/dbs` - general-purpose annotation and reference databases are stored here. Most `dbs` will be open but some may be accessed controlled e.g in `/cbio/dbs/refpanels/`.

* `/cbio/datasets` - Access controlled datasets are stored here e.g. SAHGP, Baylor, AGVP.

* `/cbio/soft` - Software that is needed to run workflows is installed here; most of our other software will be encapsulated into singularity images.

* `/cbio/images` - shared singularity images are stored here.

Please note the [restrictions](/bioinformatics/cbio#restrictions).

#### ilifu directory structure (excluding IDIA and CBIO projects)

* `/ilifu/` - the base directory for all ilifu related projects.

* `/ilifu/users` - user's personal workspace. **Limited to 2TB**. For storing longer-term data and data products that are not ready to be placed in shared project space.

* `/ilifu/astro/projects/` and `ilifu/bio/projects` - project specific directories. These directories are for sharing data and resources within project groups. Project raw data, data products, intermediate data and project specific resources, such as script or software containers, are stored here. It is recommended that raw data folders should always be read-only.

* `/ilifu/software/containers` - [software containers](tech_docs/software_environments?id=singularity-containers) can be stored here.
