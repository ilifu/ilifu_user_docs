## CBIO setup

## Directory Structure

Please read [CBIO Directory Structure](/data/data_management#CBIO-directory-structure) to see how your data should be organised.

## Restrictions

Some things to note:
* CBIO is allowed to use 400TB on the CephFS partition. There are currently no user, group or project restrictions in place.
* Compute resource restrictions are currently in place and users are only allowed to run 20 jobs and have 20 jobs in the queue. If you find that these settings are not sufficient for your work please contact the [helpdesk](https://ilifu.freshdesk.com/support/home) and see if any other arrangements can be made. There are plans to use [SLURM's fair-share factor](https://slurm.schedmd.com/priority_multifactor.html#fairshare) to share resources according to the funding initially provided by IDIA (astronomy), CBIO and DST respectively.
* Currently there are only 1184 cores available on the standard SLURM cluster. This will probably be increased after the pilot phase.
* CBIO can access an additional 320 cores on the OpenStack environment.

### Data transfer node
* The current node to use for data transfers is `dtn02.ilifu.ac.za`. For now use `scp` or `rsync` to move data.

### Data management plan for projects
* All projects would require to fill in a data management plan [here](https://forms.gle/RMJuj5xJdfFRR6CZ8).

### Examples
* [Running a Nextflow pipeline on the Ilifu standard SLURM setup](https://github.com/grbot/run-fastqc/tree/ilifu).

### Future work and data requirements
* [CBIO/Ilifu compute, storage and transfer setup requirements](http://web.cbio.uct.ac.za/~gerrit/slides/CBIO-Ilifu-compute-storage-and-transfer-setup.pdf).