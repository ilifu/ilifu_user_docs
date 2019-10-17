## Astronomy Software

### IDIA Pipelines

The IDIA Pipelines software has been developed as a tool for calibration and imaging of radio data using the ilifu system. Please visit the IDIA Pipeline [website](https://idia-pipelines.github.io/) for additional information, including documentation and tutorials.

### CARTA

CARTA is the Cube Analysis and Rendering Tool for Astronomy, a new image visualization and analysis tool designed for the ALMA, the VLA, and the SKA pathfinders. Please see the CARTA [website](https://cartavis.github.io/) and [documentation](https://carta.readthedocs.io/en/latest/) for additional information.

A CARTA server is currently hosted on ilifu at https://carta.idia.ac.za. Your login details are the same as those for Jupyter, which were emailed to you when your ilifu account was set up.

All astronomy users (i.e. those in `idia-group`) should have access to the CARTA server. Please contact support@ilifu.ac.za if you do not have access.

By default, CARTA will start browsing files in the `/carta_share/users/<your_username>`
directory, but you can access any files or folders in the /carta_share directory that your ilifu
user can access. Unlike previous versions of CARTA, v1.2 relies on unix permissions. If you
want other users to have access to specific files, you can change the file permissions of
those files or folders.

While CARTA v1.2 supports `FITS`, `CASA`, and `Miriad` images as well, we strongly suggest
converting your files to `HDF5` (IDIA schema) files for improved performance. The HDF5
converter can be found in `/carta_share/hdf_convert/run_hdf_converter`. Usage is as
follows:

```
srun /carta_share/hdf_convert/run_hdf_converter {INPUT FITS file} {OUTPUT HDF5 file}
```
We suggest you perform this conversion with the output file copying straight into a
carta_share subdirectory, to avoid additional copies, for example:
```
srun /carta_share/hdf_convert/run_hdf_converter image.fits /carta_share/users/<username>/image.hdf5

```

## Transfer data from the SARAO archive

If you are a principal investigator (PI) or member of one of the MeerKAT projects whose proposal has been accepted by SARAO, such as a Large Survey Project (LSP) or an Open Time Project, you may want to transfer your observational data from the SARAO archive to the ilifu cluster.

Before pushing your data, it is important to have an existing project on the ilifu cluster in order for us to make the data available to the project members. If you do not have an existing ilifu project, please make contact with the ilifu support team at support@ilifu.ac.za to request one, and notify us of your intention to transfer data.

In order to push your data from SARAO to ilifu, a PI, or a representative that a PI has nominated, must go to https://archive.sarao.ac.za and register an account. Once they have registered, the PI must send an email to archive@ska.ac.za requesting for this person to access the proposal.

The user guide for the archive is available [here](https://archive.sarao.ac.za/statics/Archive_Interface_User_Guide.pdf).