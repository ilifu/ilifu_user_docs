# Astronomy Software

## IDIA Pipeline

The IDIA `processMeerKAT` Pipeline has been developed as a tool for calibration and imaging of radio data using the ilifu system. It is currently a fully automated 1GC (cross-calibration) and 2GC (self-calibration) pipeline that runs on ilifu using CASA and SLURM. Please visit the IDIA Pipeline [website](https://idia-pipelines.github.io/) for additional information, including documentation and tutorials. We strongly encourage you to engage with the developers by reporting any bugs or enhancements to the [GitHub issues page](https://github.com/idia-astro/pipelines/issues).

## CARTA

CARTA is the Cube Analysis and Rendering Tool for Astronomy, a new image visualization and analysis tool designed for MeerKAT, ALMA, the VLA, and the SKA pathfinders. Please see the CARTA [website](https://cartavis.github.io/) and [documentation](https://carta.readthedocs.io/en/latest/) for additional information.

A CARTA server is currently hosted on ilifu at https://carta.idia.ac.za. Your login details are the same as those for Jupyter, which were emailed to you when your ilifu account was set up. A server hosting the beta (development) version of CARTA, which will be routinely updated between major releases, is available from https://carta-beta.idia.ac.za.

All astronomy users (i.e. those in `carta-users`) should have access to the CARTA server. Please contact [support@ilifu.ac.za](mailto:support@ilifu.ac.za) if you do not have access. For CARTA-specific issues, please contact the [CARTA helpdesk](mailto:carta_helpdesk@asiaa.sinica.edu.tw) or file an issue on [Github](https://github.com/CARTAvis/carta/issues). 

By default, CARTA will start browsing files in the `/carta_share/users/<your_username>` directory, but you can access any files or folders in the `/carta_share`, `/scratch3`, `/idia` and `/ilifu` directories that your ilifu user can access. Unlike previous versions of CARTA, v1.2 onward relies on unix permissions. If you want other project members to have access to specific files, you can move the files or folders to the relevant project directory, within `/carta_share/groups/`, `/scratch3/projects/`, or `/idia/projects/`. If the relevant project directory doesn't exist, please request for it to be created by contacting [ilifu support](mailto:support@ilifu.ac.za).

The `/idia` and `/ilifu` mounts are read-only, so users cannot export region files, FITS cutouts or moment maps here, but it is possible to do so using `/carta_share` or `/scratch3`. With these file systems mounted, the many copies of images that exist in `/carta_share` (HDF5, FITS, CASA or miriad) are no longer necessary, unless for performance reasons. For large cubes/images, we recommend [converting to HDF5](/astronomy/astronomy_software?id=hdf5-converter) and writing to `/carta_share/current` (SSDs), giving superior performance during visualisation. However, for all other images, this is not necessary, and visualising directly from `/idia`, `/ilifu` or `/scratch3` in any format will still give good performance.

### Restarting your backend

If you experience any issues starting CARTA, or if your CARTA session crashes, you may need to restart your backend. To do this, go to  File -> Server -> Restart Service. Alternatively, go to [carta.idia.ac.za/dashboard](https://carta.idia.ac.za/dashboard) (also accessible via File -> Server -> Dashboard) and press the button to "Restart CARTA service". After this, refresh your CARTA page and log in again.

### Hard-reload white screen

If you visit one of the IDIA CARTA servers and are met with only a white screen, force reload (e.g. command-shift-R) the page to clear the cache.

### HDF5 converter

While CARTA supports `FITS`, `CASA`, and `Miriad` images as well, we strongly suggest converting larges cubes/images to `HDF5` (IDIA schema) files for improved performance. The HDF5 converter can be used in the following way:

```bash
srun fits2idia -o {OUTPUT HDF5 file} {INPUT FITS file}
```
We suggest you perform this conversion with the output file copying straight into a carta_share subdirectory, to avoid additional copies, for example:
```
srun fits2idia -o /carta_share/users/${USER}/image.hdf5 image.fits

```

For large images or cubes, a speed-up can be achieved by increasing the number of CPUs, and it may be necessary to increase the memory allocation, up to 232 GB for a node in the Main partition, and 480 GB for a node in the HighMem partition. For example:

```bash
srun --mem=50GB --time=5 --cpus-per-task=10 fits2idia -p -o /carta_share/users/${USER}/image.hdf5 image.fits
```

where `-p` shows a simple progress bar. Some large FITS cubes will exceed these memory values and will not be able to convert to HDF5 in the default mode. Option `-m` can be used to report the predicted memory usage and exit, in the following way:

```bash
fits2idia -m image.fits
```

For cases where this exceeds 480 GB (or 232 GB if no HighMem nodes are available), option `-s` must be used, which uses a slower but less memory-intensive method, using a single CPU and iterating through a single channel at a time. Usage is as follows:

```bash
srun --mem=10GB --time=01:00:00 --cpus-per-task=1 fits2idia -s -p -o /carta_share/users/${USER}/image.hdf5 image.fits
```

The predicted memory usage for slow-mode conversion is reported when using both options `-s` and `-m`.

## CARACal

The CARACal Pipeline is a pipeline in active development for radio interferometry data reduction and is managed by the developers on ilifu. Please find the CARACal documentation [here](https://caracal.readthedocs.io/en/latest/), and find the repository [here](https://github.com/caracal-pipeline/caracal).

### Installing CARACal on ilifu

CARACal can be installed in a Python virtual environment on ilifu. We suggest creating the Python virtual environment, using the available modules (rather than system Python), in your shared project directory or user workspace. Please do not install CARACal in your `$HOME` (`/users/`) directory (see directory structure documentation [here](/data/directory_structure)). The Singularity containers associated with CARACal software are available and maintained at `/software/astro/caracal/`. 

### Running CARACal on ilifu

Please don't run CARACal on the ilifu login node, but on a compute node, using `sbatch` or `srun`, as documented [here](/getting_started/submit_job_slurm). If you encounter issues with running CARACal, please consider logging a [GitHub issue](https://github.com/caracal-pipeline/caracal/issues/), rather than contacting ilifu support, unless the issue is clearly an ilifu issue.

## Oxkat

Oxkat is a MeerKAT processing pipeline that is written for and commonly used on ilifu, as well as CHPC. It is a highly automated pipeline for MeerKAT data processing all the way through to 3GC (third-generation direction-dependent calibration), including software such as WSClean, DDFacet, killMS and CubiCal. For more information about installation, usage, design and software packages, please see the [GitHub documentation](https://github.com/IanHeywood/oxkat) and [ASCL entry](https://ui.adsabs.harvard.edu/abs/2020ascl.soft09003H/abstract).

## CASA

The NRAO [CASA](https://casa.nrao.edu/index.shtml) software is available on Ilifu within dedicated containers. Two CASA implementations exist: a monolithic version installed using the downloadable tar-file distribution, and a modular version installed through pip-wheels.

CASA containers are available at `/idia/software/containers/`. Monolithic CASA containers are prefixed with `casa-stable-<version>`, while modular CASA is available for CASA 6, and the containers are prefixed with `casa-6.<version>`. A CASA 6 modular container is also available as a Jupyter kernel, named `CASA 6`.

CASA modules are also available, which include helpful short-hand commands that can be used to run functions using the CASA containers. Run `module help casa` for more information.

There is a known issue with the CASA containers from CASA 6.2 upwards when making a general import of all `casatools` (e.g. to use a script written for CASA 5 without changing it) in the following way:

```python
from casatools import *
```

for which the following error is output:

```python
AttributeError: module 'casatools' has no attribute 'version_stringatmosphere'
```

The solution to overcoming this issue is by making specific imports, such as

```python
from casatools import msmetadata,table,image,measures,quanta
```

### CASA plotms

Within CASA 6, plotms is wrapped in AppImage and requires FUSE mounting inside the container. This is currently not possible on the Ilifu due to permission issues, and the use of plotms with FUSE will result in an error. As of the CASA 6.5.0 modular container onwards, the plotms app has been extracted inside the container and is available to run with and without the GUI.

To run CASA plotms with the GUI, you can run the following from the slurm-login node:

```bash
srun --x11 -p Devel singularity exec /idia/software/containers/casa-6.5.0-modular.sif casaplotms
```

To run CASA plotms non-interactively, you can make use of a virtual X server by wrapping your script within xvfb, using the following syntax (e.g. within a sbatch script):

```bash
srun singularity exec /idia/software/containers/casa-6.5.0-modular.sif xvfb-run -a python my-plotms-script.py
```

To use CASA plotms in a Jupyter notebook and display the output image within the notebook, you can use the following Python code example:

```python
import os
from casaplotms import plotms
from IPython.display import Image
import pyvirtualdisplay
_display = pyvirtualdisplay.Display(visible=False, size=(1400, 900))
_ = _display.start()

plotms(vis='</path/to/input>',plotfile='<imagename>.png',showgui=False,overwrite=True)
Image('<imagename>.png', height=500)
```
*Credit to SKA-SA for the above method detailed* [here](https://github.com/ska-sa/ARIWS-Cookbook/blob/main/2-Flagging_and_calibration/L_band_RFI_frequency_flagging.ipynb).

## Simba

### About Simba and Simba-C

**Simba** is a state-of-the-art suite of galaxy formation simulations for exploring the co-evolution of galaxies, black holes, and circum- and inter-galactic gas within a cosmological context. Simba snapshots and galaxy catalogs span up to 151 redshift outputs from z = 20 to z = 0. Further details can be found on the [Simba website](http://simba.roe.ac.uk/).

**Simba-C** is an updated version of the Simba suite which incorporates new chemical enrichment and feedback models, and finds better agreement with observations on e.g. the mass-metallicity relation, galaxy stellar mass function, and galaxy abundance ratios. Please see the [paper](https://ui.adsabs.harvard.edu/abs/2023MNRAS.525.1061H/abstract) for further information on Simba-C.


Please contact [Romeel Davé](mailto:rad@roe.ac.uk) if you have project ideas involving SIMBA data.

### Simba products on ilifu

#### Snapshots and file structure

##### Simba

The following snapshots and corresponding galaxy catalogs are available (read-only access) within the **/idia/data/laduma/SIMBA/** directory. Within this directory files are structured by name (e.g. m100n1024), wind model (e.g. s50), and snapshot number (e.g. 151; see mapping between snapshot number and redshift [here](http://simba.roe.ac.uk/outputs.txt)). For example:

- The snapshot file for the ‘Flagship’ run at redshift z = 0 is at */idia/data/laduma/SIMBA/m100n1024/s50/snap_m100n1024_151.hdf5*
- Its corresponding CAESAR galaxy catalog is in the Groups subfolder: */idia/data/laduma/SIMBA/m100n1024/s50/Groups/m100n1024_151.hdf5*

These are accessible to all IDIA users on ilifu. If you cannot access them, please make a request with [ilifu support](mailto:support@ilifu.ac.za). Further Simba files can be requested to be transferred; please contact [Romeel Davé](mailto:rad@roe.ac.uk) or [Marcin Glowacki](mailto:marcin@idia.ac.za).

Snapshot runs currently available:

- **m25n512** - High-Resolution Run. 25 Mpc/h box, 2x512<sup>3</sup> particles. Currently contains the 051, 056, 062, 071,074, 078, 090, 105, 125, 145, and 151 snapshots. Full Simba physics (s50).
- **m50n512** - 50 Mpc/h box, 2x512<sup>3</sup> particles. Contains feedback variants: s50 (full Simba physics), s50nox (no X-ray AGN feedback), s50nojet (no X-ray, jet feedback) and s50noagn (no AGN feedback). All snapshots available bar for the s50noagn model (smaller selection currently available).
    - In a separate subdirectory of SIMBA/ is **m50n512_NR**/ (non-radiative model), featuring snapshots and caesar files.
- **m100n1024** - 100 Mpc/h box, 2x1024<sup>3</sup> particles. Flagship Run. 31 snapshots available. Full Simba physics only (s50).

Some other files also exist for the above snapshots, such as a ‘blackhole details file’ for m100n1024 (*/idia/data/laduma/SIMBA/m100n1024/s50/blackhole_details/bhALL.hdf5*).

##### Simba-C
Similar to Simba snapshots, files can be found within **/idia/data/laduma/SIMBAC/** directory. Only the full Simba physics is available, so snapshots are available through e.g.*/idia/data/laduma/SIMBAC/m100n1024/*.

Snapshot runs currently available:

- **m100n1024** - 100 Mpc/h box, 2x1024<sup>3</sup> particles. Currently only some snapshots are available: all snapshots at redshifts z < 0.1 (snapshot_{145-151}.hdf5), every second snapshot until redshift z = 10 (i.e. snapshot_145.hdf5, snapshot_143.hdf5, …, snapshot_019.hdf5), and the first snapshot (snapshot_000.hdf5). This is the Flagship full Simba-C physics run.

The above is accompanied by additional files, such as **all** CAESAR snapshot files (within */idia/data/laduma/SIMBAC/m100n1024/Groups*), and files describing black holes in the Simba-C snapshots (within */idia/data/laduma/SIMBAC/m100n1024/blackhole_details*).

- **m50n512** - 50 Mpc/h box, 2x512<sup>3</sup> particles, at the full Simba-C physics run. Currently only contains 10 snapshot boxes (snapshot_{036,051,062,073,078,079,105,124,125,151}.hdf5) but will be faster to load than the 100 Mpc/h boxes for any preliminary checks.

The above is accompanied by the respective CAESAR snapshot files (within */idia/data/laduma/SIMBAC/m50n512/Groups*), and additional files in the *hfof_files* and *other_files* subdirectories. 

- **m25n512** - 25 Mpc/h box, 2x512<sup>3</sup> particles (High-Resolution Run). Currently only some snapshots are available: all snapshots at redshifts z < 0.1 (snapshot_{145-151}.hdf5); every second snapshot until redshift z = 10 (i.e. snapshot_145.hdf5, snapshot_143.hdf5, …, snapshot_019.hdf5), additionally snapshots at z =  2 (snapshot_078.hdf5), 3 (snapshot_062.hdf5), and 6 (snapshot_036.hdf5); and the first snapshot (snapshot_000.hdf5). This is the Flagship full Simba-C physics run.

The above is accompanied by additional files, such as all CAESAR snapshot files as caesar_xxx.hdf5 (within /idia/data/laduma/SIMBAC/m25n512/Groups).

These are also accessible to all IDIA users on ilifu. If you cannot access them, please make a request with ilifu support. If further Simba-C files are of interest to your project, please contact [Romeel Davé](mailto:rad@roe.ac.uk) or [Marcin Glowacki](mailto:marcin@idia.ac.za).

**Coming soon**: m25n512 high-resolution run! We expect these to be available by early 2025.

#### HI Cubes

HI spectral line cubes (in .fits format), and corresponding quick moment maps for individual galaxies in Simba can be created and made available on ilifu, within a ‘Cube’ subfolder. This is done via the [MARTINI](https://github.com/kyleaoman/martini) package (webpage includes tutorial). More can be generated and made available to all ilifu users; please contact [Marcin Glowacki](mailto:marcin@idia.ac.za). (It is also possible to create your own cubes on ilifu, as Martini is installed via the Simba container; see below.)

Currently, example cubes are available for several galaxies within the high resolution (m25n512) snapshots, for the z = 0, 0.5 and 1 files (snapshots 151, 125 and 105 respectively). The cubes have a spectral resolution that corresponds to the MeerKAT 32k mode.

### Simba container

A Simba singularity container (see instructions [here](getting_started/container_environments)) can be accessed on ilifu at */idia/software/containers/SIMBA.simg*. It is also a selectable kernel on [https://jupyter.ilifu.ac.za/](https://jupyter.ilifu.ac.za/) to be used with Jupyter notebooks.

It includes the following packages:

- [CAESAR](https://caesar.readthedocs.io/en/latest/) (used to access the galaxy catalogs)
- [pyGadgetReader](https://github.com/jveitchmichaelis/pygadgetreader) (used for loading files from the raw snapshot)
- MARTINI
- yt
- APLpy
- Astropy
- pandas
- spectral-cube

Previous Simba containers are maintained within /idia/software/containers/, and are named by date. If you would like an update or addition to be made to this software container, please first contact [Marcin Glowacki](mailto:marcin@idia.ac.za).

### Simba Example Jupyter Notebook

An example notebook for accessing a Simba snapshot file and corresponding CAESAR file, obtaining, can be found at `/idia/data/laduma/SIMBA/Simba_Demo.ipynb`. You can copy it to your home directory and access it via ilifu’s JupyterLab system.

# Transfer data from the SARAO archive

If you are a principal investigator (PI) or member of one of the MeerKAT projects whose proposal has been accepted by SARAO, such as a Large Survey Project (LSP) or an Open Time Project (OTP), you may want to transfer your observational data from the SARAO archive to the ilifu facility.

Before pushing your data, it is important to have an existing project on the ilifu facility, so we can make the data available to the project members. If you do not have an existing ilifu project, please contact [ilifu support](mailto:support@ilifu.ac.za) to request one, and notify us of your intention to transfer data, with reference to your proposal ID (PID). Eligible MeerKAT projects are those with a PI or lead technical contact based at a South African institution. ​If a student is the PI, they will need written approval from their supervisor.

In order to access your proposal data on the SARAO archive, you must have an archive account with access to your project. Please visit [https://archive.sarao.ac.za](https://archive.sarao.ac.za) to register an account, and have a PI, or a representative that a PI has nominated, add you do the proposal following the [group management guide](https://archive.sarao.ac.za/statics/Group_Management_Guide.pdf). The user guide for the archive is available [here](https://archive.sarao.ac.za/statics/Archive_Interface_User_Guide.pdf), and further requests can be made via the [SARAO service desk](https://skaafrica.atlassian.net/servicedesk/customer/portal/1/group/-1).

In order to push your data from SARAO to ilifu, your project must be enabled for pushing to IDIA, after which, a "push to IDIA" icon will be shown on the archive, next to the data under the proposal. To request this, please contact [ilifu support](mailto:support@ilifu.ac.za) and provide the relevant MeerKAT proposal ID (PID), and the ilifu project name under which you want to associate this. If you have not yet requested support for this PID, please summarise your expected observing time, data volumes and general resource requirements.

SARAO archive transfers will be written to `/idia/raw` by default, with symbolic links to this path from your project directory in `/idia/projects`. The MS will be read-only, from where it can read and written to your working directory. We request that you please make use of this "push to IDIA" feature rather than creating a directory download link, for the following reasons:

1. The data will make use of a direct Globus transfer, and complete much more quickly compared to directly downloading and decompressing the data with `wget` and `tar`
2. The data will remain as read-only and will therefore ensure project members don't inadvertently edit the raw data
3. The file/directory structure will be easier for both parties (your project group and ilifu support) to understand and monitor

For more information about a general workflow and its relation to raw data, please read our MeerKAT [data management documentation](/data/data_management#general-workflow).

## MVF to MS configuration

In February 2020, new SARAO archive functionality was introduced to configure the conversion to MeasurementSet (MS), including the selection of channel ranges, polarisation products, flags, and options to average in time and frequency channel. This can be done by pressing the "push to IDIA" button and configuring your transfer within the pop-up window. Configuration options are shown [here](https://github.com/ska-sa/MeerKAT-Cookbook/blob/master/archive/Convert%20MVF%20dataset(s)%20to%20MeasurementSet.ipynb), and the flag categories are shown [here](https://archive.sarao.ac.za/statics/sdp_flags.pdf).

A good configuration includes setting `-a true` (to remove auto-correlations) and `--flags=cam,data_lost` (to apply instrumental flags that can't be identified during processing, and to avoid flagging real data, including HI lines). If you have no interest in polarisation data, we also suggest you use `-f false` and `-p HH,VV`, which will halve your data volume. Similarly, for spectral-line projects, if frequencies above 1420 MHz aren't needed, we suggest a channel selection of `-C 0,21591`, reducing your volume by a further ~34%. If you observed in 32k mode but only need 4k data, use `--chanbin=8`, which will reduce your volumes by eight. Using `--quack=1` (to discard the first dump) may also be desirable. For more information, please see our [MeerKAT processing documentation](/astronomy/meerkat_processing).

It is important to note that currently (August 2022):

1. Only a single transfer is allowed per MS<sup>1</sup>
2. Newer transfers (manually done following instructions below) will not overwrite older data, since timestamps are written to the transfer directory<sup>1</sup>
3. Transfers are MS by default<sup>2</sup>

<sup>1</sup> After a dataset has been transferred, the SARAO archive sets a flag that prevents that same dataset from being downloaded to the same destination. If you need to re-transfer your data (e.g. with a different selection), and the archive disallows another transfer (orange arrow labelled 'IDIA'), contact [ilifu support](mailto:support@ilifu.ac.za) to complete the push for you. A feature enabling multiple pushes of the same CBID with different selection is being implemented and will soon be deployed to the SARAO archive.

<sup>2</sup>Transfers of data in the native MeerKAT MVF format can also be arranged by contacting [ilifu support](mailto:support@ilifu.ac.za).

## Changes to flagging

On 26 November 2019, the default [flags](https://archive.sarao.ac.za/statics/sdp_flags.pdf) were updated to `cam,data_lost,ingest_rfi`, whereas previously, particularly for the 2019 MeerKAT Open Time Projects (OTPs), they included the full set of flags, with ~30% of the raw target data typically being flagged, or sometimes up to ~90%. Users affected by this can re-transfer the data following the instructions in the [section above](#mvf-to-ms-configuration). Data older than the OTPs may be affected in different ways, as the archive and its functionality were still being built. Newer transfers can configure these flags using the SARAO archive functionality described in the [section above](#mvf-to-ms-configuration).
