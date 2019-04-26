# CBIO setup

* User homes are in `/users/`. Not sure if this is being backed up, assume not.
* CBIO users will be using the CephFS parallel file partition. The BeeGFS partitions are for the astronomer users. Our space is in `/data/projects/cbio/`. Directories that have been setup
  * `/data/projects/cbio/users` - a user's private scratch space
  * `/data/projects/cbio/projects` - project spaces will be created in here
  * `/data/projects/cbio/dbs` - annotation and reference databases will go in here
  * `/data/projects/cbio/datasets` - mostly access controlled datasets will go in here e.g. SAHGP, Baylor, AGVP.
  * `/ceph/cbio/soft` - some software that are needed to run workflows will be installed here, most of our other software will be encapsulated into singularity images.
  * `/data/projects/cbio/images` - singularity images that need to be shared would be stored here.

Some things to note
* CBIO are allowed to use 400TB on the CephFS partition. There is no user, group or project restrictions in place currently.
* Compute resource restrictions are not in place. There are plans to use the SLURM fair ussage to share resources according to initial funding been provided by astronomy, CBIO and DST respectively.
* Currently there are only 1216 cores available on the standard SLURM cluster. This will probably be increased after the pilot phase.
* CBIO can access an additional 320 cores on the OpenStack environment.

Examples
* [Running a Nextflow pipeline on the Ilifu standard SLURM setup](https://github.com/grbot/run-fastqc/tree/ilifu).

## Future work and data requirements
* [CBIO/Ilifu compute, storage and transfer setup requirements](http://web.cbio.uct.ac.za/~gerrit/slides/CBIO-Ilifu-compute-storage-and-transfer-setup.pdf)
