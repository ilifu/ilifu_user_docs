# CBIO setup

* User homes are in `/users/`. Not sure if this is being backed up, assume not.
* CBIO users will be using the CephFS parallel file partition. The BeeGFS partitions are for the astronomer users. Our space is in `/ceph/cbio/`. Directories that have been setup
  * `/ceph/cbio/users` - a user's private scratch space
  * `/ceph/cbio/projects` - project spaces will be created in here
  * `/ceph/cbio/dbs` - annotation and reference databases will go in here
  * `/ceph/cbio/datasets` - mostly access controlled datasets will go in here e.g. SAHGP, Baylor, AGVP.
  * `/ceph/cbio/soft` - some software that are needed to run workflows will be installed here, most over our other software will be encapsulated into containers.

Some things to note
* CBIO are allowed to use 400TB on the CephFS partition. There is no user, group or project restrictions in place currently.
* Compute resource restrictions are not in place. There are plans to use the SLURM fair ussage to share resources according to initial funding been provided by astronomy, CBIO and DST respectively.
* Currently there are only 1216 cores available on the standard SLURM cluster. This will probably be increased after the pilot phase.
* CBIO can access an additional 320 cores on the OpenStack environment.
   
