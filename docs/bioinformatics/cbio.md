# CBIO setup

## Directory Structure

Please read [CBIO Directory Structure](/data/directory_structure#CBIO-directory-structure) to see how your data should be organised.

## Restrictions

Some things to note:

* CBIO is allowed to use 400TB on the CephFS partition. There are currently no user, group or project restrictions in place.
* Compute resource restrictions are currently in place and users are only allowed to have 20 jobs queued/running. If you find that these settings are not sufficient for your work please contact the [helpdesk](https://ilifu.freshdesk.com/support/home) and see if any other arrangements can be made. There are plans to use [SLURM's fair-share factor](https://slurm.schedmd.com/priority_multifactor.html#fairshare) to share resources according to the funding initially provided by IDIA (astronomy), CBIO and DST respectively.
* Currently there are only 1184 cores available on the standard SLURM cluster. This will probably be increased after the pilot phase.
* CBIO can access an additional 320 cores on the OpenStack environment.


## Data transfer nodes
* For `scp`, `cp` or `rsync` use `transfer.ilifu.ac.za`.
* For Globus Online (gridftp) transfers use `dtn01.ilifu.ac.za`.

## Data management plan for projects

* All projects would require to fill in a data management plan [here](https://forms.gle/RMJuj5xJdfFRR6CZ8).

## Examples

* [Running a Nextflow pipeline on the ilifu standard SLURM setup](https://github.com/grbot/run-fastqc/tree/ilifu).
* [Launching RStudio in a SLURM job](/tech_docs/software_environments#rstudio)

### GenomeStrip

Genome strip requires the use of [environment modules](tech_docs/software_environments#environment-modules) to configure your software environment. The genome strip module is: `bio/svtoolkit/2.00.1918`, i.e. you should run:

```bash
$ module add bio/svtoolkit/2.00.1918
$ module list

Currently Loaded Modules:
  1) jdk/11.0.2   2) slurm-drmaa/1.1.0   3) bio/htslib/1.9   4) R/3.6.1   5) bio/svtoolkit/2.00.1918

```

So now the `SV_DIR` environment variable is set, and the dependencies (such as `java`, `R`, `samtools` and `tabix`) are loaded too. Finally please follow the instructions on [using DRMAA with GenomeStrip](https://gatkforums.broadinstitute.org/gatk/discussion/12327/genomestrip-and-slurm). Particularly one should add the arguments below to the `SVPreprocess`, `SVDiscovery` and `SVGenotyper` scripts.

```bash
  -jobRunner Drmaa
  -gatkJobRunner Drmaa
  -jobNative "--mem-per-cpu=XXXX --time=XXXX ..."
  -jobQueue Main
```

*Note: please update the `mem-per-cpu` and `time` parameters*

## Future work and data requirements

* [CBIO/ilifu compute, storage and transfer setup requirements](http://web.cbio.uct.ac.za/~gerrit/slides/CBIO-Ilifu-compute-storage-and-transfer-setup.pdf).
