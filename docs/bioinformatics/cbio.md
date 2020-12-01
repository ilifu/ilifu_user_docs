# CBIO setup

## Directory Structure

Please read [CBIO Directory Structure](/data/directory_structure#CBIO-directory-structure) to see how your data should be organised.

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
