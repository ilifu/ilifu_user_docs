## Astronomy Software

### IDIA Pipelines

The IDIA Pipelines software has been developed as a tool for calibration and imaging of radio data using the ilifu system. Please visit the IDIA Pipeline [website](https://idia-pipelines.github.io/) for additional information, including documentation and tutorials.

### CARTA

CARTA is the Cube Analysis and Rendering Tool for Astronomy, a new image visualization and analysis tool designed for the ALMA, the VLA, and the SKA pathfinders. Please see the CARTA [website](https://cartavis.github.io/) and [documentation](https://carta.readthedocs.io/en/latest/) for additional information.

A CARTA server is currently hosted on ilifu at https://carta.idia.ac.za.

Please contact support@ilifu.ac.za for access to the CARTA server.

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
/carta_share/hdf_convert/run_hdf_converter {INPUT FITS file} {OUTPUT HDF5 file}
```
We suggest you perform this conversion with the output file copying straight into a
carta_share subdirectory, to avoid additional copies, for example:
```
/carta_share/hdf_convert/run_hdf_converter image.fits /carta_share/users/<username>/image.hdf5

```