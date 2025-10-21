# Data management

Storage on the ilifu Research Facility is shared amongst all members of our user community. In order to support our users and the diverse range of projects that we host, it is important to make efficient use of storage by having a good data management strategy. The following describes some of these strategies, best practises and workflows in reference to data management. A good data management strategy includes the following, all of which is outlined within this documentation:

1. Prototype your workflow (via a version-controlled repository) over small volumes
2. Develop your workflow into a fully-automated production workflow
3. Automatically write selected data products (including logs, software versions and input parameters) to longer-term storage
4. Automatically remove temporary/intermediate data products (i.e. the remainder)

## Typical workflow

As outlined in our [directory structure](/data/directory_structure) documentation, the scratch mounts are for the purpose of data processing, and are expected to contain temporary data products that can be quickly removed. As also outlined there, the `/{idia,cbio,ilifu}/projects` directories are project-specific directories expected to contain final data products for longer-term storage. A good workflow utilising this directory structure is shown below.

<div style="text-align:center"><img src="/_media/DM-workflow.png" alt="Data management workflow" width=800 /></div>

Within this workflow, scripts and configuration files stored in `/users` are used to run a processing workflow or pipeline, reading (e.g. raw) data from a read-only directory such as `/n/raw`, `/n/projects` or `/n/data`, and writing temporary/intermediate data products to a scratch mount such as `/scratch3`. At the end of this process, specific data products (e.g. final results - see suggested products below) are selected and written into a project directory. After this, all remaining data is removed from the workspace on the scratch mount. There are two approaches for doing this:

1. Identify products to selectively write to longer-term storage, and remove the rest
2. Remove what isn't needed, and write the remainder to longer-term storage

For a typical workflow, there are many more temporary products than final products, meaning the first approach is significantly easier. Following our directory structure, we expect you to remove old files on scratch mounts, but as a start, it's helpful to identify and remove large files that are no longer needed.

## Copying or moving data

Data can be moved or copied between directories on the same or different mounts / filesystems. When moving from one directory to another within the same mount, we recommend making use of the `mv` command, which will instantly move your data. Below is an example of moving data between different directories on the same mount:

```bash
mv /idia/users/$USER/run1 /idia/projects/my-project/processed
```

[Python virtual environments](/tech_docs/software_environments?id=python-virtual-environments) should not be moved, as the path associated with these environments is hard-coded, and the environment cannot be activated after changing its location. Instead, the virtual environment can be rebuilt, making use of the `pip freeze` command where necessary, to identify the virtual environment's packages. In general, we recommend building virtual environments in one of your personal workspaces, such as `/idia/users/$USER/software`.

<!-- https://stackoverflow.com/questions/32407365/can-i-move-a-virtualenv -->

When moving data between mounts, the `mv` command can also be used, which (under the hood) will first copy and then remove your data. However, this is very slow, and may result in data loss if your transfer is interrupted mid-transfer. Therefore, we recommend rather making use of the `cp` command, and then removing your data after verifying its integrity. Below is an example of copying data between different mounts:

```bash
cp -a /scratch3/projects/my-project/final-run /cbio/projects/my-project/processed
```

The archive mode (option `-a`) will preserve the timestamps, ownership and other metadata, and includes the recursive `-r` option, which is needed when copying a directory rather than a single file.

When copying data on ilifu, please do not make use of the Slurm login node. Copying is best done via an sbatch script, which will be run on a compute node and therefore be much less volatile. Alternatively, transfers can be run via the [transfer node](/data/data_transfer#transfer-using-scp-and-rsync), or on a Slurm compute node interactively via a persistent terminal (e.g. screen/tmux/mosh).

### Large transfers with Globus

For large transfers, we recommend making use of [Globus](/data/data_transfer#transfer-using-globus-online). When undertaking internal ilifu transfers with Globus, the performance will [not be optimal](/data/data_transfer?id=using-globus-for-internal-ilifu-transfers) compared to transfers between two well-configured end-points. However, a number of the features contained within Globus (accessible via the "Transfer & Timer Options") make Globus useful for internal transfers. These include the "sync" option to only transfer new or changed files, the verifying of file integrity, and the functionality to schedule regular transfers within paticular directories. In general, we recommend enabling the sync option, and the option to "preserve source file modification times" (e.g. when having to [repair symbolic links with rsync](/data/data_transfer#configuring-a-transfer)).

### Fast transfers with parallel copy script

If you wish to run an efficient internal copy on ilifu, we recommend making use of the GNU `parallel` task to simultaneously transfer a number of large files. Before writing and launching a script to do so, it's important to identify directories in which there are a number of large files or subdirectories, as this approach performs poorly when run over a small number of files. In this example, the `/scratch3/users/$USER/my-data` directory contains 16 large files/subdirectories.

Therefore we include the following lines of code in a script called `parallel_copy.sh`, which will run 16 parallel calls of `cp -a` over these 16 files/subdirectories.

```bash
#!/bin/bash
shopt -s dotglob #Include hidden files with '*'
mkdir /ilifu/astro/projects/my-project/my-data
cd /scratch3/users/$USER/my-data
printf '%s\n' * | parallel -j 16 cp -a {} /ilifu/astro/projects/my-project/my-data
```

Next, we make it executible and create a directory for the logs:

```bash
chmod +x parallel_copy.sh
mkdir logs
```

Then we write an sbatch file, `parallel_copy.sbatch` to run our copy on a Slurm compute node, ensuring we use 16 CPUs and allow enough wall-time to complete the transfer:

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

Lastly, we run the script and monitor it via the Slurm queue.

```bash
sbatch parallel_copy.sbatch
```

## Checking file integrity

When copying data, it may be important to check the integrity of your data before removing it from its original location. For individual files, this can be achieved using a program such as `md5sum` or `sha256sum`, which will output a checksum. The checksum will be identical for each file if it has been transferred intact. Using the paths from a previous example, below is an example of checking the integrity of all files within the directory **from** which (source) and **to** which (destination) you've copied your data.

```bash
cd /scratch3/projects/my-project/final-run
find -type f -exec md5sum '{}' \; > md5sum.txt
cd /cbio/projects/my-project/processed
find -type f -exec md5sum '{}' \; > md5sum.txt
```

Lastly, produce a checksum for the entire set of output checksums, and compare the two to ensure they're the same:

```bash
cat /scratch3/projects/my-project/final-run/md5sum.txt | sort -k 2 | md5sum
cat /cbio/projects/my-project/processed/md5sum.txt | sort -k 2 | md5sum
```

<!-- https://unix.stackexchange.com/questions/35832/how-do-i-get-the-md5-sum-of-a-directorys-contents-as-one-sum -->

If the output is identical, your data has been copied intact, as all checksums between source and destination are identical. If they're not identical, the difference can be investigated using `diff`. If any files have been missed or skipped, or have partially transferred and are incomplete, they will be output when running `diff`:

```
diff /scratch3/projects/my-project/final-run/md5sum.txt /cbio/projects/my-project/processed/md5sum.txt
```

In such a case, either wait until your copy has completed and run your checksum again, or remove the data from destination and re-run the copy of that file. When multiple files are missing, the difference between them can be checked by running `rsync` in a similar way to what is documented [here](/data/data_transfer#configuring-a-transfer). Paticular attention must be paid to including the trailing slash (`/`) for the source path, and excluding it for the destination path. A final `rsync` can also be used to ensure source and desination are identical, before removing the data from source. Files that are only present in the destination directory but not the source directory will also be displayed with this `diff` command, and can be ignored when you wish to verify the integrity of only the files copied from source.

As mentioned above, file integrity is checked automatically during Globus transfers, although this option can be switched off if necessary.

## Maturity of workflow

During processing, it's important to identify the maturity of your workflow, in terms of the its stage or type, as this affects what processing and data management strategy is followed. In general, you will be:

1. Prototyping or developing your workflow
2. Running a production workflow

### Prototyping

Prototyping or developing your workflow involves experimentation, in order to create or optimise a workflow via the identification of optimal parameters, data products, etc. Such prototyping may include manual processing, or disconnected custom scripts that are manually run one-by-one, and may involve a significant amount of interactivity. Prototyping may also include running a fully automated pipeline, but experimenting with different parameters to optimise results. During prototyping, the intermediate/temporary data products may be retained, for comparison, or as input to experimentation.

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

### General best practises

* Prototyping should develop into production workflows
* Backup your scripts, workflow or pipeline, ideally by uploading to a version-controlled repository such as GitHub<sup>1</sup>
* For each processing run, keep a record of your the software versions of your workflow/pipeline, and its input parameters

<sup>1</sup> We recommend users familiarise themselves with the resources available from the [Software Carpentry website](https://software-carpentry.org).

## Products to retain

For a typical workflow, final data products will be retained for longer-term storage, as produced by your workflow. For the purpose of reproducibility and posterity, it is important to retain your workflow's parameters / inputs / versions, and its logs (e.g. sbatch standard out / error). Further domain-specific data products to retain are [listed below](#domain-specific-data-management).

## Products to remove

Following the [typical workflow](#typical-workflow) above, we recommend first selectively writing data products you wish to retain for longer-term storage, and removing everything else from your processing run, which will include your temporary / inflated data products. In some cases, it may be better/easier to identify which products to remove, and write the remainder to longer-term storage. A helpful start is identifying the large data products that don't need to be retained, and removing those. For very large files, it may be more suitable to run `rm` within an interative Slurm session, or on the transfer node. Some additional domain-specific data products to remove are [listed below](#domain-specific-data-management).

## Domain-specific data management

### Radio astronomy

For radio astronomy processing with a MeasurementSet (MS) or Multi-MeasurementSet (MMS), it's often important to retain your final calibrated data (often a few to 10s TB in size for MeerKAT data). Ideally, this is in the form of an MS with a single data column (e.g. corrected data). Additionally, it's important to retain the following data products, which are typically much smaller in size than the calibrated data:

1. Calibration tables (typically MB in size)
2. Flag versions (typically GB in size)
3. Final images (typically MB in size) or cubes (typically GB in size)

It is possible to store only the calibration tables and flag versions, and remove your calibrated data, which can be regenerated at any point by applying the calibration and flags to the raw MS (e.g. using CASA's `applycal` and `flagmanager` tasks).

#### Find and remove MeasurementSets

As mentioned above, we expect you to remove old files on scratch mounts, but as a start, it's helpful to identify and remove large files that are no longer needed. If you no longer need the (M)MSs from a completed processing run, remove them to free up the bulk of the storage from your processing run.

For data produced via the [IDIA pipeline](https://idia-pipelines.github.io/docs/processMeerKAT), the `cleanup.sh` script can be run to remove the temporary MMSs, and `allSPW_cleanup.sh` can be run to also remove the final calibrated MMSs. For a general workflow (including the IDIA pipeline), below is an example of using the `find` command to find and remove (M)MSs:

```bash
#!/bin/bash

find $1 \( -name "*.ms" -o -name "*.mms" \) -exec ls -d {} \; > vis_and_flags_tmp.txt
du -hsc $(cat vis_and_flags_tmp.txt)
read -p "Press return to remove data... "
rm -r $(cat vis_and_flags_tmp.txt)
rm vis_and_flags_tmp.txt
```

This script finds and then displays the volume (and total sum) of the (M)MSs on disk, and the `read -p` step forces you to press return to remove the data, or otherwise press control+C to cancel the script (e.g. if an (M)MS is displayed that you do not wish to remove). If you also don't need to retain the flag versions, add the following to the `find` call (at the end of the brackets):

```bash
 -o -name "*flagversions"
 ```

#### General workflow

Below is a diagram showing the cumulative inflation of data for a general MeerKAT processing workflow, following the [typical workflow](#typical-workflow) shown above.

<div style="text-align:center"><img src="/_media/MS-inflation.png" alt="MS inflation" width=800 /></div>

The data volumes shown here are for a typical MeerKAT 32k MS, for an 8 hour observation including all antennas and polarisations. As suggested [here](/data/data_transfer#mvf-to-ms-configuration), it is recommended that you average or select data wherever possible during SARAO archive transfers. This will reduce the disk volumes and significantly improve the data processing time. If you have pushed raw data with high spectral resolution and wish to replace it with averaged data, please contact [support@ilifu.ac.za](mailto:support@ilifu.ac.za) to request this.

The raw data contains a single `DATA` column by default, and is stored as a read-only MS in `/idia/raw` (symlinked from `/idia/projects`), from where it can be read during the initial processing steps (e.g. via CASA tasks `mstransform`, `split` or `partition`), ideally on a scratch mount. For pipelines that require the MS within the working directory, or for cases where you wish to give the raw MS a different name, we recommended creating a symbolic link (symlink) to the raw MS, via the following:

```bash
cd /scratch3/projects/my-project/processing/
ln -s /idia/raw/my-project/SCI-YYYYMMDD-PI-01/0123456789/0123456789_sdp_l0.ms my-raw-data.ms
```

After this, `/scratch3/projects/my-project/processing/my-raw-data.ms` will point to your raw read-only MS.

During processing, the (M)MSs from within your working directory will inflate by ~2.5 times, as they will add a `MODEL_DATA` column (e.g. during CASA task `setjy`) and a `CORRECTED_DATA` column (e.g. during `applycal`), in addition to the `DATA` column. Often an initial cross-calibration process will produce these temporary (M)MSs, split out the corrected data for your target(s), and then self-calibrate the target(s), further inflating this separate (M)MS with three data columns. The final calibrated data should contain a single corrected data column, roughly equal in size to the raw data (or smaller with averaging), to be selectively written back to your project directory for longer-term storage. All other temporary inflated data products should be removed.

Once you have selectively written your final data products for longer-term storage, we recommend removing your raw MS. As this is read-only, please contact [support@ilifu.ac.za](mailto:support@ilifu.ac.za) to request this, specifying which MSs can be removed. In some cases, you may require retaining your raw MS for a longer verification period, and we request that you please contact [support@ilifu.ac.za](mailto:support@ilifu.ac.za) to motivate for this. However, it should be noted that your raw data can be transferred again from the SARAO archive (and if older than 200 days, first restaged from tape). Furthermore, it may be possible to recover your raw data from (M)MSs derived from it, such as where the original `DATA` column exists, running `flagmanager` to undo flags where needed.

For further information about MeerKAT processing and data management strategies, please read our [MeerKAT processing documentation](/astronomy/meerkat_processing).
