# Data Management

Storage on the ilifu Research Facility is shared amongst all members of our user community. In order to support our users and the diverse range of projects that we host, it is important to make efficient use of storage by having a good data mangaement strategy. The following describes some of these strategies, best practises and workflows in reference to data management. A good data management strategy includes ... (mention temporary vs. long-term, type of processing, etc)

## Typical Workflow

As outlined in our [directory structure](/data/directory_structure) documentation, the scratch mounts are for the purpose of data processing, and are expected to contain temporary data products that can be quickly removed. As also outlined here, the `/{idia,cbio,ilifu}/projects` (referred to collectively as `/n/data`) directories are project specific directories expected to contain final data products for longer-term storage. A good workflow utilising this directory structure is shown below.

<div style="text-align:center"><img src="/_media/DM-workflow.png" alt="Data management workflow" width=800 /></div>

Within this workflow, scripts and configuration files stored in `/users` are used to run a processing workflow or pipeline, reading (e.g. raw) data from a read-only mount such as `/n/raw` or `/n/data`, and writing temporary/intermediate data products to a scratch mount such as `/scratch3`. At the end of this process, specific data products (e.g. final results - see suggested products below) are selected and written into a project directory. After this, all remaining data is removed from the workspace on the scratch mount. There are two approaches for doing this:

1. Identify products to selectively write for longer-term storage, and remove the rest
2. Remove what isn't needed, and writing the remainder to longer-term storage

For a typical workflow, there are many temporary products, meaning the first approach is signifcantly easier. Following the directory structure, we expect you to remove old files on scratch mounts, but as a start, it's helpful to identify and remove large files that are no longer needed.

## Maturity of Workflow

During processing, it's important to identify the maturity of your workflow, in terms of the its stage or type, as this affects what processing and data mangaement strategy is followed. In general, you will be:

1. Developing or prototyping your workflow
2. Running a production workflow

### Prototyping

Prototyping or developing your workflow involves experimentation, in order to create or optimise a workflow via the identification of optimal parameters, data products, etc. Such prototyping may include disconnected custom scripts that are manually run one-by-one, or manual processing, and may involve a significant amount of interactivity. Prototyping may also include running a fully automated pipeline, but experimenting with different parameters to optimise results. During developement, the intermediate/temporary data products may be retained, for comparison, or as input to experimentation.

Best practises when prototyping or developing your workflow include the following:

* Experiment with small volumes of temporary products
* Avoid prototyping / development over large volumes, unless necessary
* Verify outputs and identify optimal parameters

### Production

Production workflows are workflows in which little to no development, experimentation or interactivity is expected to occur, and there is no interest in retaining intermediate / temporary data products. Such workflows are genearlly run as a pipeline, meaning they are contained within a series of end-to-end steps (i.e. the output of one step is used as input to the next step) that are managed by a single wrapper software package. Often such a pipeline will be automated and can be configured before launching, and scheduled to run in advance (e.g. via Slurm and/or Nextflow).

Importantly, a pipline may be run for protyping or development purposes, in such cases where the workflow itself or parameters are not optimised.

Best practises when running a production workflow include the following:

* Capture software / pipelines versions and input parameters, so your results can be reproduced
* Automate / pipeline the removal of temporary data products
* Automate / pipeline the selective writing of final data products to longer-term storage

Importantly, during production, temporary data products can be regenerated at any point via running the same workflow with the same inputs. Therefore, it's safe and ideal to remove such products automatically during your production workflow.

## General Best Practises

* Prototyping should develop into production workflows
* Backup your scripts, workflow or pipeline, ideally by uploading to a version-controlled reposity such as via GitHub
* Keep a record of your the software versions of your workflow/pipeline, and its input parameters

## Products to Retain

### Astronomy

## Products to Remove

## Copying or Moving Data



## Domain-Specific Data Management

### Astronomy

<div style="text-align:center"><img src="/_media/MS-inflation.png" alt="MS inflation" width=800 /></div>

### Bioinformatics

DANE
