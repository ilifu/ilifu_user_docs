# CBIO setup

* User homes are in `/users/`. Not sure if this is being backed up, assume not.
* CBIO users will be using the CephFS parallel file partition. The BeeGFS partitions are for the astronomer users. Our space is in `/data/projects/cbio/`. Directories that have been setup
  * `/data/projects/cbio/users` - a user's private scratch space. Limited to 5TB. Working in a project space would allow for more storage space. Please see form below in regard to data management plan for projects. 
  * `/data/projects/cbio/projects` - project spaces will be created in here
  * `/data/projects/cbio/dbs` - annotation and reference databases will go in here
  * `/data/projects/cbio/datasets` - mostly access controlled datasets will go in here e.g. SAHGP, Baylor, AGVP.
  * `/data/projects/soft` - some software that are needed to run workflows will be installed here, most of our other software will be encapsulated into singularity images.
  * `/data/projects/cbio/images` - singularity images that need to be shared would be stored here.

Some things to note:
* CBIO is allowed to use 400TB on the CephFS partition. There are no user, group or project restrictions in place currently.
* Compute resource restrictions are currently in place and users are only allowed to run 20 jobs and have 20 jobs in the queue. If you find that these settings are not sufficient for your work please contact the [helpdesk](https://ilifu.freshdesk.com/support/home) and see if any other arrangements can be made. There are plans to use [SLURM's fair-share factor](https://slurm.schedmd.com/priority_multifactor.html#fairshare)  to share resources according to initial funding been provided by astronomy, CBIO and DST respectively.
* Currently there are only 1184 cores available on the standard SLURM cluster. This will probably be increased after the pilot phase.
* CBIO can access an additional 320 cores on the OpenStack environment.

## Data transfer node
* The current node to use for data transfers is `dtn02.ilifu.ac.za`. For now use `scp` or `rsync` to move data.

## Data management plan for projects
* All projects would require to fill in a data management plan [here](https://forms.gle/RMJuj5xJdfFRR6CZ8).

## Examples
* [Running a Nextflow pipeline on the Ilifu standard SLURM setup](https://github.com/grbot/run-fastqc/tree/ilifu).

## Future work and data requirements
* [CBIO/Ilifu compute, storage and transfer setup requirements](http://web.cbio.uct.ac.za/~gerrit/slides/CBIO-Ilifu-compute-storage-and-transfer-setup.pdf).
