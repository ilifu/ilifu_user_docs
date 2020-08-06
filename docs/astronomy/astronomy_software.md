## Astronomy Software

### IDIA Pipeline

The IDIA `processMeerKAT` Pipeline has been developed as a tool for calibration and imaging of radio data using the ilifu system. It is currently a 1GC (cross-calibration) pipeline that runs on ilifu using CASA and SLURM, which is actively being extended to 2GC (self-calibration), as well as being optimised to run more than an order of magnitude faster, with good success so far. Please visit the IDIA Pipeline [website](https://idia-pipelines.github.io/) for additional information, including documentation and tutorials. We strongly encourage you to engage with the developers by reporting any bugs or enhancements to the [GitHub issues page](https://github.com/idia-astro/pipelines/issues).

### CARTA

CARTA is the Cube Analysis and Rendering Tool for Astronomy, a new image visualization and analysis tool designed for ALMA, the VLA, and the SKA pathfinders. Please see the CARTA [website](https://cartavis.github.io/) and [documentation](https://carta.readthedocs.io/en/latest/) for additional information.

A CARTA server is currently hosted on ilifu at https://carta.idia.ac.za. Your login details are the same as those for Jupyter, which were emailed to you when your ilifu account was set up.

All astronomy users (i.e. those in `idia-group`) should have access to the CARTA server. Please contact [support@ilifu.ac.za](mailto:support@ilifu.ac.za) if you do not have access. For CARTA-specific issues, please contact the [CARTA helpdesk](mailto:carta_helpdesk@asiaa.sinica.edu.tw) or file an issue on [Github](https://github.com/CARTAvis/carta/issues).

By default, CARTA will start browsing files in the `/carta_share/users/<your_username>`
directory, but you can access any files or folders in the /carta_share directory that your ilifu
user can access. Unlike previous versions of CARTA, v1.2 relies on unix permissions. If you
want other users to have access to specific files, you can change the file permissions of
those files or folders.

While CARTA supports `FITS`, `CASA`, and `Miriad` images as well, we strongly suggest
converting your files to `HDF5` (IDIA schema) files for improved performance. The HDF5
converter can be found in `/carta_share/hdf_convert/run_hdf_converter`. Usage is as
follows:

```
srun /carta_share/hdf_convert/run_hdf_converter -o {OUTPUT HDF5 file} {INPUT FITS file}
```
We suggest you perform this conversion with the output file copying straight into a
carta_share subdirectory, to avoid additional copies, for example:
```
srun /carta_share/hdf_convert/run_hdf_converter -o /carta_share/users/<username>/image.hdf5 image.fits

```

### CARACal

The CARACal Pipeline is a pipeline in active development for radio interferometry data reduction, which currently exists outside ilifu's [supported software environments](/tech_docs/software_environments), and is managed by the developers. Please read the documentation [here](https://caracal.readthedocs.io/en/latest/), and find the (private) repository [here](https://github.com/caracal-pipeline/caracal). For access to this repository, please contact [Paolo Serra](mailto:paolo.serra@inaf.it).

#### Installing CARACal on ilifu

Installing a stable version of CARACal on ilifu is a work in progress, as captured in [this](https://github.com/caracal-pipeline/caracal/issues/625) GitHub issue. Please consult this issue for the latest progress, and comment here if you make some of your own progress. Please do not install CARACal in your `/users/` directory (see directory structure documentation [here](/data/directory_structure)), particularly the singularity containers, which are available and maintained at `/software/astro/caracal/`.

#### Running CARACal on ilifu

Please don't run CARACal on the ilifu login node, but on a compute node, using `sbatch` or `srun`, as documented [here](/getting_started/submit_job_slurm). If you encounter issues with running CARACal, please consider commenting on the [GitHub issue](https://github.com/caracal-pipeline/caracal/issues/625), or logging a new one, rather than contacting ilifu support, unless the issue is clearly an ilifu issue.

## Transfer data from the SARAO archive

If you are a principal investigator (PI) or member of one of the MeerKAT projects whose proposal has been accepted by SARAO, such as a Large Survey Project (LSP) or an Open Time Project, you may want to transfer your observational data from the SARAO archive to the ilifu cluster.

Before pushing your data, it is important to have an existing project on the ilifu cluster in order for us to make the data available to the project members. If you do not have an existing ilifu project, please make contact with the ilifu support team at support@ilifu.ac.za to request one, and notify us of your intention to transfer data.

In order to push your data from SARAO to ilifu, a PI, or a representative that a PI has nominated, must go to [https://archive.sarao.ac.za](https://archive.sarao.ac.za) and register an account. Once they have registered, the PI must send an email to archive@ska.ac.za requesting for this person to access the proposal.

The user guide for the archive is available [here](https://archive.sarao.ac.za/statics/Archive_Interface_User_Guide.pdf).

### MVF to MS configuration

In February 2020, new SARAO archive functionality was introduced to configure the conversion to MeasurementSet (MS), including the selection of channel ranges, polarisation products, flags, and options to average in time and frequency channel. It is important to note that currently (March 2020):

1. Only a single transfer is allowed per MS<sup>1</sup>
2. Newer transfers (manually done following instructions below) overwrite older data<sup>1</sup>
3. Transfers are MS by default<sup>2</sup>

Discussions to optimise this process are ongoing. For now, we suggest that users transfer only a single MS per dataset, and set `-a true` (to remove auto-correlations) and `--flags=cam,data_lost` (to apply instrumental flags that can't be identified during processing, and to avoid flagging real data, including HI lines). If you have no interest in polarisation data, we also suggest you use `-f false` and `-p HH,VV`, which will halve your data volume. Using `--quack=1` (to discard the first dump) may also be desirable. Conversion options are shown [here](https://github.com/ska-sa/MeerKAT-Cookbook/blob/master/archive/Convert%20MVF%20dataset(s)%20to%20MeasurementSet.ipynb), and flagging options [here](https://archive.sarao.ac.za/statics/sdp_flags.pdf).

<sup>1</sup> After a dataset has been transferred, the SARAO archive sets a flag that prevents that same dataset from being downloaded to the same destination. If you must re-transfer your data, and the archive disallows another transfer (orange arrow labelled 'IDIA'), firstly contact [ilifu support](mailto:support@ilifu.ac.za) to rename (or remove) your data, and then contact the [SARAO archive](mailto:archive@ska.ac.za) to reset the flag.

<sup>2</sup>Transfers of data in the native MeerKAT format (MFV / MKV4) can also be arranged by contacting the [SARAO archive](mailto:archive@ska.ac.za).

### Changes to flagging

On 26 November 2019, the default [flags](https://archive.sarao.ac.za/statics/sdp_flags.pdf) were updated to `cam,data_lost,ingest_rfi`, whereas previously, particularly for MeerKAT Open Time Projects (OTPs), they included the full set of flags, with ~30% of the raw target data typically being flagged, or sometimes up to ~90%. Users affected by this can re-transfer the data following the instructions in the [section above](#mvf-to-ms-configuration). Data older than the OTPs may be affected in different ways, as the archive and its functionality were still being built. Newer transfers can configure these flags using the SARAO archive functionality described in the [section above](#mvf-to-ms-configuration).