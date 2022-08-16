# Data Management

Storage on the ilifu Research Facility is shared amongst all members of our user community. In order to support our users and the diverse range of projects that we host, it is important to make efficient use of storage by having a good data management strategy. The following describes some of these strategies, best practises and workflows in reference to data management. A good data management strategy includes ... (mention temporary vs. long-term, type of processing, etc)

## Typical Workflow

As outlined in our [directory structure](/data/directory_structure) documentation, the scratch mounts are for the purpose of data processing, and are expected to contain temporary data products that can be quickly removed. As also outlined here, the `/{idia,cbio,ilifu}/projects` (referred to collectively as `/n/data`) directories are project specific directories expected to contain final data products for longer-term storage. A good workflow utilising this directory structure is shown below.

<div style="text-align:center"><img src="/_media/DM-workflow.png" alt="Data management workflow" width=800 /></div>

Within this workflow, scripts and configuration files stored in `/users` are used to run a processing workflow or pipeline, reading (e.g. raw) data from a read-only mount such as `/n/raw` or `/n/data`, and writing temporary/intermediate data products to a scratch mount such as `/scratch3`. At the end of this process, specific data products (e.g. final results - see suggested products below) are selected and written into a project directory. After this, all remaining data is removed from the workspace on the scratch mount. There are two approaches for doing this:

1. Identify products to selectively write for longer-term storage, and remove the rest
2. Remove what isn't needed, and writing the remainder to longer-term storage

For a typical workflow, there are many temporary products, meaning the first approach is significantly easier. Following the directory structure, we expect you to remove old files on scratch mounts, but as a start, it's helpful to identify and remove large files that are no longer needed.

## Copying or Moving Data

Data can be moved or copied between directories on the same or different mounts / filesystems. When moving from one directory to another within the same mount, we recommend making use of the `mv` command, which will instantly move your data. Below is an example of moving data between different directories on the same mount:

```bash
mv /idia/users/$USER/run1 /idia/projects/myproject/processed
```

When moving data between mounts, the `mv` command can also be used, which (under the hood) will first copy and then remove your data. However, this is very slow, and we recommend rather making use of the `cp` command in archive mode (option `-a` -- this will preserve the timestamps, ownership and other metadata) and then removing your data after verifying its integrity, incase your transfer is interrupted mid-transfer. Below is an example of copying data between different mounts:

```bash
cp -ra /scratch3/projects/myproject/final-run /cbio/projects/myproject/processed
```

The recurrsive `-r` option is needed when copying a directory rather than a single file.

When copy data on ilifu, please do not make use of the SLURM login node. Copying is best done via an sbatch script, which will be run on a compute node and is therefore much less volatile. Alternatively, transfers can be run via the [transfer node](/data/data_transfer#transfer-using-scp-and-rsync), or on a SLURM node interactively via a persistent terminal (e.g. screen/tmux/mosh).

### Large Transfers with Globus

For large transfers, we recommend making use of [Globus](/data/data_transfer#transfer-using-globus-online). When undertaking internal ilifu transfers with Globus, the performance will [not be optimal](/data/data_transfer?id=using-globus-for-internal-ilifu-transfers) compared to transfers between two well-configured end-points. However, a number of the features contained within Globus (accessible via the `Transfer & Timer Options`) make Globus useful for internal transfers. These include the "sync" option to only transfer new or changed files, the option verifying file integrity, and the functionality to schedule regular transfers within paticular directories. In general, we recommend enabling the sync option, and the option to "preserve source file modification times" (e.g. when having to [repair symbolic links with rsync](/data/data_transfer#configuring-a-transfer)).

### Fast Transfers with Parallel Copy Script

If you wish to run an efficient internal copy on ilifu, we recommend making use of the GNU `parallel` task to simultaneously transfer a number of large files. Before writing and launching a script to do so, it's important to identify directories in which there are a number of large files or subdirectories, as this approach performs poorly when run over a small number of files. In this example, the `/scratch3/users/$USER/my-data` directory contains 16 large files/subdirectories.

Therefore we write the following script, which runs 16 parallel calls of `cp -ra` over these 16 files/subdirectories.

```bash
shopt -s dotglob #Include hidden files with '*'
cd /scratch3/users/$USER/my-data
mkdir /ilifu/astro/projects/my-project/my-data
printf '%s\n' * | parallel -j 16 cp -ra {} /ilifu/astro/projects/my-project/my-data
```

Next, we make it executible and create a directory for the logs:

```bash
chmod +x parallel_copy.sh
```

Then we write an sbatch file to run our copy on a SLURM compute node, ensuring we use 16 CPUs and allow enough wall-time to complete the transfer:

```bash
#!/bin/bash
#SBATCH --cpus-per-task=16
#SBATCH --mem=16GB
#SBATCH --job-name=parallel_copy
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err
#SBATCH --partition=Main
#SBATCH --time=02:00:00

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

./parallel_copy.sh
```

Lastly, we run the script and monitor it via the SLURM queue.

```bash
sbatch parallel_copy.sbatch
```

## Checking File Integrity

When copying data, it may be important to check the integrity of your data before removing is from its original location. For individual files, this can achieved using a program such as `md5sum` or `sha256sum`, which will output a checksum. The checksum will be identical for each file if it has been transferred intact. Using the same paths from the previous example, below is an example of checking the file integrity of all files within the directory *from* which (source) and *to* which (destination) you've copied your data.

```bash
cd /scratch3/projects/myproject/final-run
find -type f -exec md5sum '{}' \; > md5sum.txt
cd /cbio/projects/myproject/processed
find -type f -exec md5sum '{}' \; > md5sum.txt
diff /scratch3/projects/myproject/final-run/md5sum.txt /cbio/projects/myproject/processed/md5sum.txt
```

If nothing is output when running `diff`, your data has been copied intact, as all checksums between source and destination are identical. If any files have been missed or skipped, or have partially transferred and are incomplete, they will be output when running `diff`. In such a case, either wait until your copy has completed and run your checksum again, or remove the data from destination and re-run the copy of that file. When multiple files are missing, the difference between can be checked by running rsync in a similar way to what is documented [here](/data/data_transfer#configuring-a-transfer). Paticular attention must be paid to including the trailing slash (`/`) for the source path, and exluding it for the destination path. A final `rsync` can also be used to ensure source and path and desination are identical, before removing the data from source.

As mentioned above, file integrity is checked automatically during Globus transfers, although this option can be switched off if necessary.

## Maturity of Workflow

During processing, it's important to identify the maturity of your workflow, in terms of the its stage or type, as this affects what processing and data management strategy is followed. In general, you will be:

1. Developing or prototyping your workflow
2. Running a production workflow

### Prototyping

Prototyping or developing your workflow involves experimentation, in order to create or optimise a workflow via the identification of optimal parameters, data products, etc. Such prototyping may include disconnected custom scripts that are manually run one-by-one, or manual processing, and may involve a significant amount of interactivity. Prototyping may also include running a fully automated pipeline, but experimenting with different parameters to optimise results. During development, the intermediate/temporary data products may be retained, for comparison, or as input to experimentation.

Best practises when prototyping or developing your workflow include the following:

* Experiment with small volumes of temporary products
* Avoid prototyping / development over large volumes, unless necessary
* Verify outputs and identify optimal parameters

### Production

Production workflows are workflows in which little to no development, experimentation or interactivity is expected to occur, and there is no interest in retaining intermediate / temporary data products. Such workflows are generally run as a pipeline, meaning they are contained within a series of end-to-end steps (i.e. the output of one step is used as input to the next step) that are managed by a single wrapper software package. Often such a pipeline will be automated and can be configured before launching, and scheduled to run in advance (e.g. via Slurm and/or Nextflow).

Importantly, a pipeline may be run for prototyping or development purposes, in such cases where the workflow itself or parameters are not optimised.

Best practises when running a production workflow include the following:

* Capture software / pipelines versions and input parameters, so your results can be reproduced
* Automate / pipeline the removal of temporary data products
* Automate / pipeline the selective writing of final data products to longer-term storage

Importantly, during production, temporary data products can be regenerated at any point via running the same workflow with the same inputs. Therefore, it's safe and ideal to remove such products automatically during your production workflow.

## General Best Practises

* Prototyping should develop into production workflows
* Backup your scripts, workflow or pipeline, ideally by uploading to a version-controlled repository such as via GitHub<sup>1</sup>
* Keep a record of your the software versions of your workflow/pipeline, and its input parameters

<sup>1</sup> We recommend users familiarise themselves with the resources available from the [Software Carpentry website](https://software-carpentry.org).

## Products to Retain

For a typical workflow, final data products will be retained for longer-term storage, as produced by your workflow. For the purpose of reproducibility and posterity, it is important to retain your workflow's parameters / inputs / versions, and its logs (e.g. sbatch standard out / error).

### Radio Astronomy

For radio astronomy processing with a MeasurementSet (MS), it's import to retain your final calibrated data (often a few to 10s TB in size for MeerKAT data). Ideally, this is in the form of a single column (e.g. corrected data) MS. Additionally, it's import to retain the following data products, which are typically much smaller in size than the calibrated data:

1. Calibration tables (typically MB in size)
2. Flag versions (typically GB in size)
3. Final images or cubes (typically MB for images and GB for cubes)

It is possible to store only the calibration tables and flag versions, and remove your calibrated data, which can be regenerated at any point by applying the calibration and flags to the raw MS (e.g. using CASA's `applycal` and `flagmanager` tasks).

## Products to Remove

## Domain-Specific Data Management

### Astronomy

<div style="text-align:center"><img src="/_media/MS-inflation.png" alt="MS inflation" width=800 /></div>

Other stuff [here](/astronomy/meerkat_processing)

### Bioinformatics

DANE
