# Supported software environments

The software environments on ilifu are provided principally through [Singularity](https://docs.sylabs.io/guides/latest/user-guide/) containers and [environment modules](#environment-modules). Additional software environments include virtual environments, either [Python virtual environments](#python-virtual-environments), or [Conda](#anaconda) -- these are generally created and managed by the user or project group. 

## Singularity containers

Containers are unit software packages that contain all the software, files, libraries, dependencies and environmental variables necessary to run a particular task or workflow. Containers are encapsulated software environments and abstract the software and applications from the underlying operating system. This allows users to run workflows in customized environments, switch between environments, and to share these environments with colleagues and research teams.

The container images that are maintained by the support team can be found at different paths, depending on the group that you belong to: `/idia/software/containers/`, `/cbio/images` and `/ilifu/software/containers`, as well as common areas `/software/<astro|bio|common>/containers`. There are a number of ways one can use a Singularity container, including executing the software inside a container or interactively using a shell session in the container environment, as detailed below.

### Using a container

The container images that are maintained by the support team can be found at different paths, depending on the group that you belong to: `/idia/software/containers/`, `/cbio/images` and `/ilifu/software/containers`, as well as common areas `/software/<astro|bio|common>/containers`. There are a number of ways one can use a Singularity container, including executing the software inside a container or interactively using a shell session in the container environment, as detailed below.

**Note:** singularity is not installed on the Slurm login node and therefore containers can only be accessed from worker nodes, either through job submissions using `sbatch` or using the `sinteractive`/`srun` command for interactively running a job on a worker node.

#### Execute software in a container

A user is able to execute a script using the software from the container environment using the singularity `exec` command. From the Slurm login node, if you want to try the commands, you'll first need to allocate some resources on a compute node to yourself using the following:
```bash
$ sinteractive
```
This will place you on a development node, `compute-001`. Singularity is then available from the compute node. You could execute a Python script using the `python` software in a container, for example:
```bash
$ singularity exec /idia/software/containers/ASTRO-PY3.10.sif python myscript.py
hello world!
$
```
This command will execute the script, `myscript.py`, using the Python software that is contained within the `ASTRO-PY3.10.sif` container. The script will have access to all the Python libraries that have been included in the container.

Similary, the following will execute `print("hello world!")` using the CASA software package that is contained in the `casa-stable-v6.sif` container. Note that once the script has been run successfully the container session is closed automatically. **The `singularity exec` command is widely used to submit jobs on Slurm**.

```bash
$ singularity exec /idia/software/containers/casa-stable-v6.sif casa --log2term --nologger -c 'print("hello world!")'

optional configuration file not found, continuing CASA startup without it

No event loop hook running.
Using matplotlib backend: agg
CASA 6.7.0.31 -- Common Astronomy Software Applications [6.7.0.31]
...
hello world!
```

#### Interactive shell command

A user is able to open a Singularity container as an interactive shell and issue command line tasks within the environment that the container provides. To do this a user calls the Singularity container using the `shell` command. You can open a shell session within an available container using the following:
```bash
$ singularity shell /idia/software/containers/SoFiA2v2.5.1.sif 
SoFiA2v2.5.1.sif:~$ sofia
____________________________________________________________________________

 Pipeline started
____________________________________________________________________________

  Using:    Source Finding Application (SoFiA)
  Version:  2.5.1 (24-Jun-2022)
  CPU:      1 thread available
  Time:     Tue Oct 21 11:36:38 2025
```

This command will spawn a new shell inside the container, in this case the `SoFiA2v2.5.1.sif` container, allowing the user to interact with the container environment. The user can then run software that is housed in the container and develop workflows interactively.

#### Run command

When containers are built a runscript can be designated in the recipe file. This allows programs to be automatically initiated using a `run` command. For example:

```shell
$ singularity run /idia/software/containers/ASTRO-PY3.10.sif -c 'print("hello world!")'
hello world!
```

The runscript for this container is:

```text
%runscript
    /usr/bin/python "$@"
```

Running this container using the `run` command will initialize a container session and run any arguments (`"$@"`) using the Python package contained within the container, allowing the user to run python commands interactively. However, as soon as the Python command line is exited the container session is closed.

A number of the containers that are supported by ilifu do not include runscripts and therefore cannot be used using the `run` command.

### Available containers

Several containers have been developed for use on the ilifu cluster and in other clusters, and are currently maintained by the support team. These containers include the following (**See the dropdown information for specific container details by clicking on the relevant arrow below**). For use in other clusters the containers can be downloaded from the [IDIA Singularity Registry Server](https://sregistry.idia.ac.za/):

<details>
<summary id="casa-modular-v6-container">casa-modular-v6 container</summary>

**Description:** the latest stable release of CASA from [NRAO CASA website](https://casa.nrao.edu).

**JupyterLab Kernel:** CASA-6

| Name        | Def file           | Github repo           | OSVersion |
|-------------|--------------------|-----------------------|-----------|
| casa-6.simg | casa-6-modular.def | idia-container-casa-6 | jammy     |

| Packages & Libraries | Python Libraries |                  |              |
|----------------------|------------------|------------------|--------------|
| Python 3.10          | PyQt5            | casashell        | holoviews    |
| casacore-data        | astropy          | casatablebrowser | katbeam      |
| casacore-dev         | astroquery       | casatasks        | katdal       |
| xvfb                 | bokeh            | casatestutils    | matplotlib   |
|                      | casaconfig       | casatools        | numpy        |
|                      | casadata         | casaviewer       | pandas       |
|                      | casafeather      | cloudpickle      | protobuf     |
|                      | casalogger       | dask-ms[xarray]  | pybdsf       |
|                      | casampi          | datashader       | pygdsm       |
|                      | casaplotms       | h5py             | scikit-image |
|                      | casaplotserver   | healpy           | scipy        |

</details>

<details>
<summary id="casa-stable-v6-container">casa-stable-v6 container</summary>

**Description:** the latest stable release of CASA from [NRAO CASA website](https://casa.nrao.edu).

| Name               | Def file        | Github repo                    | OSVersion |
|--------------------|-----------------|--------------------------------|-----------|
| casa-stable-v6.sif | casa-stable.def | idia-container-casa-stable-py3 | jammy     |

| Packages and Libraries |
|------------------------|
| CASA (Python 3.10)     |
| xvfb                   |

</details>

<details>
<summary id="casa-stable-container">casa-stable container</summary>

**Description:** the latest stable release of CASA from [NRAO CASA website](https://casa.nrao.edu).

| Name                           | Def file        | Github repo                | OSVersion       |
|--------------------------------|-----------------|----------------------------|-----------------|
| casa-stable-[4.7.2-5.8.0].simg | casa-stable.def | idia-container-casa-stable | CentOS / Ubuntu |

| Packages and Libraries |
|------------------------|
| CASA (Python 2.7)      |

</details>

<details>
<summary id="ASTRO-PY3.X-container">ASTRO-PY3.X containers</summary>

**Description:** A collection of astronomy software, including sourcefinding, machine learning, visualization, SED- and fusion-related software.

**JupyterLab Kernel:** ASTRO-PY3 (Python 3.112), ASTRO-PY3 (Python 3.10), ASTRO-PY3 (Python 3.8)

| Name             | Def file | Github repo | OSVersion |
|------------------|----------|-------------|-----------|
| ASTRO-PY3.12.sif |          |             | noble     |
| ASTRO-PY3.10.sif |          |             | jammy     |
| ASTRO-PY3.8.simg |          |             | bionic    |

| Packages & Libraries | Python Libraries |                       |                         |
|----------------------|------------------|-----------------------|-------------------------|
| Aladin               | Aegean           | fastprogress          | pymc                    |
| GPz                  | H-E-L-P/XID_plus | fits2hdf              | pymoc                   |
| LFTools              | Jinja2           | fitsio                | pymultinest             |
| MultiNest            | MCVCM            | fruitbat              | pyregion                |
| SoFiA (python 2.7)   | MontagePy        | future                | pyro-ppl                |
| SoFiA-2              | MrMoose          | galsim                | pyspark                 |
| astromatic/eye       | PASTA            | geopandas             | pystan                  |
| astromatic/skymaker  | PUMA             | ginga                 | pyswarms                |
| astrometry.net       | Pillow           | glob2                 | pysynch                 |
| blackbox             | PyQt5yt          | glueviz               | python-casacore         |
| blobcat              | PyVirtualDisplay | graphviz              | pyvo                    |
| casacore-data        | RM-Tools         | gwcs                  | qtpy                    |
| casacore-dev         | RMextract        | h5py                  | regions                 |
| cds.cdsclient        | Tractor          | hips                  | reproject               |
| ds9                  | TreeCorr         | httplib2              | rich                    |
| eog                  | WCSAxes          | imbalanced-learn      | schwimmbad              |
| galfit               | altair           | imgcat                | scikit-image            |
| galfitm              | aplpy            | ipykernel             | scikit-learn            |
| graphviz             | astro-datalab    | ipywidgets            | scikit-optimize         |
| libblas-dev          | astro-pink       | jdaviz                | scikit-plot             |
| libcfitsio-dev       | astroML          | jmetalpy[distributed] | scikit-survival         |
| libfftw3-dev         | astroNN          | kapteyn               | scikits.bootstrap       |
| libgsl-dev           | astroimtools     | lark-parser           | scipy                   |
| libplplot            | astroplan        | lifelines             | sciserver               |
| missfits             | astropy          | matplotlib            | seaborn                 |
| montage              | astropy-healpix  | mlflow                | sep                     |
| openjdk-11-jre       | astroquery       | mlpack                | sfdmap                  |
| postgresql           | atpy             | mocpy                 | skypy                   |
| psfex                | autokeras        | mpi4py                | somoclu                 |
| python-tk            | bdsf[ishell]     | mpld3                 | sourcery                |
| python2.7            | cachey           | mpsort                | spectral-cube           |
| python3-pip          | ccdproc          | mxnet                 | specutils               |
| scamp                | cdshealpix       | nbconvert             | sqlalchemy              |
| sextractor           | ceres-solver     | nbdime                | squarify                |
| stiff                | cesium           | ne2001                | statsmodels             |
| stilts               | cfgrib           | netCDF4               | tensorflow_probability  |
| swarp                | cigale           | networkx              | tensorpack              |
| texlive-latex-extra  | click            | numba                 | theano                  |
| topcat               | cma              | numpy                 | tkp                     |
| wcslib-dev           | configobj        | numpyro               | tqdm                    |
| weightwatcher        | corner           | opencv-python         | vaex                    |
| wsctools             | cython           | pandas                | virtualenv              |
| xvfb                 | dask             | patsy                 | xarray                  |
|                      | dask-ml          | photutils             | xgboost                 |
|                      | dask-ms[xarray]  | plotly                | zoobot                  |
|                      | deeplenstronomy  | plotly-express        | astropy (python 2.7)    |
|                      | docopt           | pscikit-learn         | eazy-pype (python 2.7)  |
|                      | easydict         | psycopg2-binary       | matplotlib (python 2.7) |
|                      | eazy             | pydl                  | numpy (python 2.7)      |
|                      | eazy-py          | pydot                 | scipy (python 2.7)      |
|                      | emcee            | pyds9                 |                         |
|                      | extinction       | pyesasky              |                         |

</details>

<details>
<summary id="ASTRO-PY3-container">ASTRO-PY3 container</summary>

**Description:** A collection of astronomy software (originally named sourcefinding_py3), including sourcefinding, machine learning, visualization, SED- and fusion-related software. This is a **legacy** container, see ASTRO-PY3.10 & ASTRO-PY3.12 containers.

**JupyterLab Kernel:** ASTRO-PY3, SF-PY3

| Name           | Def file | Github repo | OSVersion |
|----------------|----------|-------------|-----------|
| ASTRO-PY3.simg |          |             | bionic    |

| Packages & Libraries |                      | Python Libraries      |                  |
|----------------------|----------------------|-----------------------|------------------|
| AEGEAN               | PINK                 | altair                | opencv           |
| AGNFitter            | PSEx                 | aplpy                 | pandas           |
| Aladin               | PUMA                 | astroML               | photutils        |
| ANNZ                 | PyBDSF               | astroplan             | psycopg2         |
| Astromatic           | SCAMP                | astropy               | pydl             |
| Astrometry           | SED3FIT              | astroquery            | pymc             |
| BlobCat              | Sextractor           | autokeras             | pymoc            |
| CIGALE               | SkyMaker             | bohek                 | PyMultiNest      |
| datalab              | SoFiA                | ccdproc               | pyregion         |
| DS9                  | sofia2               | corner                | pyregion         |
| EASZY                | Sourcery             | dask                  | pyspark          |
| EAZY-PIPE            | STIFF                | datalab               | pystan           |
| EyE                  | stilts               | datashader            | pytorch          |
| GALFIT               | Stuff                | easydict              | pyvo             |
| GalFitM              | Swarp                | emcee                 | regions          |
| GalSim               | Topcat               | fits2hdf              | reproject        |
| GPz                  | Tractor              | ginga                 | scikit-bootstrap |
| LFTools              | VAEX                 | glueviz               | scikit-image     |
| MissFITS             | VisiOmatic           | gwcs                  | scikit-learn     |
| Montage              | VIZIC                | h5py                  | scikit-plot      |
| PASTA                | WeightWatcher        | healpy                | scipy            |
|                      |                      | herschelhelp_internal | sciserver        |
|                      |                      | herschelhelp_python   | seaborn          |
|                      |                      | hfpy                  | somoclu          |
|                      |                      | hips                  | specutils        |
|                      |                      | holoviews             | squarify         |
|                      |                      | keras                 | statsmodels      |
|                      |                      | lifelines             | tensorflow       |
|                      |                      | matplotlib            | tensorpack       |
|                      |                      | nbconvert             | theano           |
|                      |                      | nbdime                | tqdm             |
|                      |                      | numba                 | XID_plus         |
|                      |                      | numpy                 | yt               |

</details>

<details>
<summary id="ASTRO-GPU-container">ASTRO-GPU containers</summary>

**Description:** These containers includes Tensorflow or PyTorch and software for accelerating ETL (DALI, RAPIDS), Training (cuDNN, NCCL), and Inference (TensorRT) workloads. Common astronomy Python pacakges have also been included. 

**JupyterLab Kernel:** ASTRO-GPU (TensorFlow), ASTRO-GPU (PyTorch)

| Name                   | Repo                      | Github repo | OSVersion |
|------------------------|---------------------------|-------------|-----------|
| ASTRO-GPU.simg (TF)    | nvcr.io/nvidia/tensorflow |             | noble     |
| ASTRO-GPU-PyTorch.simg | nvcr.io/nvidia/pytorch    |             | focal     |

| Packages & Libraries              | Python Libraries (TF) | Python Libraries (PyTorch) |
|-----------------------------------|-----------------------|----------------------------|
| CUDA                              | astropy               | astropy                    |
| cuBLAS                            | glop                  | glop                       |
| NVIDIA cuDNN                      | ipykernel             | ipykernel                  |
| NVIDIA NCCL                       | ipython               | ipython                    |
| RAPIDS                            | ipywidgets            | matplotlib                 |
| NVIDIA Data Loading Library (DALI)| jupyterlab-optuna     | numpy                      |
| TensorRT                          | matplotlib            | scipy                      |
| TensorFlow with TensorRT (TF-TRT) | numpy                 | zoobot[pytorch]            |
| OR Torch-TensorRT                 | optuna                |                            |
|                                   | plotly                |                            |
|                                   | scipy                 |                            |
</details>

<details>
<summary id="kern-2-container">kern-2 container</summary>

**Description:** KERN is a bi-annually released set of radio astronomical software packages. It should contain most of the standard tools that a radio astronomer needs to work with radio telescope data. Package list available at from the [KERN-suite website](https://kernsuite.info/).

**JupyterLab Kernel:** KERN-2

| Name       | Def file   | Github repo                    | OSVersion |
|------------|------------|--------------------------------|-----------|
| kern-2.img | kern-2.def | idia-container-kern            | xenial    |

| Packages & Libraries |              | Python Libraries |                   |
|----------------------|--------------|------------------|-------------------|
| 21cmfast             | multinest    | atpy             | owlcat            |
| aips                 | obit         | psutils          | presto            |
| aoflagger            | oskar        | attrdict         | purr              |
| aoflagger-dev        | parseltongue | casacore         | pymoresane        |
| casacore             | presto       | galsim           | pyxis             |
| casalite             | psrcat       | katdal           | qwt5-doc          |
| casarest             | psrchive     | katpoint         | qwt5-qt4          |
| cassbeam             | purify       | katversion       | rfimasker         |
| chgcentre            | rpfits       | kittens          | scatterbrane      |
| cub-dev              | sagecal      | lofar            | sourcery          |
| dialog               | sigproc      | meqtrees-cattery | tigger            |
| drive-casa           | sigpyproc    | meqtrees-timba   | tkp               |
| dspsr                | simfast21    | montblanc        | transitions       |
| dysco                | simms        |                  |                   |
| galsim               | stimela      |                  |                   |
| karma                | tempo        |                  |                   |
| lofar                | tempo2       |                  |                   |
| meqtrees             | tirific      |                  |                   |
| Montage              | tmv          |                  |                   |
| msutils              | wsclean      |                  |                   |

</details>

<details>
<summary id="kern-5-container">kern-5 container</summary>

**Description:** KERN is a bi-annually released set of radio astronomical software packages. It should contain most of the standard tools that a radio astronomer needs to work with radio telescope data. Package list available at from the [KERN-suite website](https://kernsuite.info/).

**JupyterLab Kernel:** KERN-5

| Name       | Def file  | Github repo           | OSVersion |
|------------|-----------|-----------------------|-----------|
| kern5.simg | kern5.def | idia-container-kern-5 | bionic    |

| Packages & Libraries |                |                       | Python Libraries |
|----------------------|----------------|-----------------------|------------------|
| 21cmfast             | katdal         | purr                  | numpy            |
| aips                 | karma          | pyfftw                | atpy             |
| astro-tigger         | kittens        | pymonetdb             | scipy            |
| astro-tigger-lsm     | lofar          | pymoresane            | psutil           |
| attrdict             | losoto         | python-typing         | pyfits           |
| bl-sigproc           | meqtrees-timba | pyxis                 | typing           |
| blimpy               | Montage        | PyBDSF                | pywcs            |
| blitz                | msutils        | rfimasker             | virtualenv       |
| casalite             | multinest      | rmextract             |                  |
| casarest             | obit           | rpfits                |                  |
| chgcentre            | owlcat         | sagecal               |                  |
| ctypesgen            | parseltongue   | sched                 |                  |
| cubical              | peasoup        | sigpyproc             |                  |
| cub                  | polygon2       | simfast21             |                  |
| ddfacet              | ppgplot        | simms                 |                  |
| difmap               | prefactor      | singularity-container |                  |
| drive-casa           | presto         | tempo                 |                  |
| dysco galsim         | psrcat         | tigger                |                  |
| gbt-seti             | psrchive       | tirific               |                  |
| gsm                  | psrdada        | turbo-seti            |                  |
| heimdall-astero      |                |                       |                  |

</details>

<details>
<summary id="astro-r-container">astro-r container</summary>

**Description:** an R container with collection of R astronomy packages, including ProFound, ProFit and ProSpect.

**JupyterLab Kernel:** ASTRO-R

| Name                     | Recipe File            | Github repo     | OSVersion |
|--------------------------|------------------------|-----------------|-----------|
| ASTRO-R.simg             |                        |                 | jammy     |

| Packages and Libraries | R Libraries   |            |           |
|------------------------|---------------|------------|-----------|
| R                      | BiocManager   | Rfits      | lambda.r  |
| fftw                   | Cairo         | Rwcs       | magicaxis |
|                        | DBI           | akima      | mgcv      |
|                        | EBImage       | astro      | mice      |
|                        | FITSio        | castrodatR | nlme      |
|                        | Highlander    | caret      | nnet      |
|                        | IRkernel      | cmaeshpc   | pacman    |
|                        | LaplacesDemon | data.table | party     |
|                        | ProFit        | devtools   | remotes   |
|                        | ProFound      | dplyr      | rmarkdown |
|                        | ProPane       | fftwtools  | shiny     |
|                        | ProSpect      | ggplot2    | tidyr     |
|                        | ProSpectData  | imager     | tidyverse |
|                        | Rcpp          | knitr      | xtable    |

</details>

#### How to know what software a container includes

The maintained containers are generally named after the primary software they are created for, for example `SoFiA2v2.5.1.sif`, and include the version or date they were built. Some containers, however, contain a suite of software, such as the `ASTRO-PY3` containers, and therefore it isn't feasible to include all the software in the container name. There are a number of useful techniques to determine what sofware is included in a container:

##### Check the container %help information

Sometimes a container will include information in its help function, which can be access using the following command:
```bash
    $ srun singularity run-help /path/to/container
```
##### Check the included python packages

A simple way to determine what Python packages a container includes is to run the command `pip freeze` within the container environment to list all the Python packages installed using `pip`. This can be achieved using the following command:
```bash
	$ srun singularity exec /path/to/container pip freeze
```

##### Check the container build script (definition file)

You can generally see the build script that was used to build the container using the `inspect -d` parameter, for example:

```bash
    $ srun singularity inspect -d /path/to/container
```

The build script will include all the commands used to create the container, `apt-get`, `pip install`, etc, so you can use this information to find out what software was installed in the container. This unfortunately is not possible if the Singularity container was created by pulling a Docker container (although it will indicate which Docker library and image was used), or if the container was built from another base image/container only the last build script will be visible. If the latter is the case, the build scripts of each previous layer are included in the container at `/.singularity.d/bootstrap_history/` and may provide additional information about the included software.

### Building your own container

In order to build containers a user requires root access on the system where the container is being built. Therefore, users cannot build containers directly on the ilifu cluster. However, containers can be built in an environment where a user has root access, and then the container can be moved to the ilifu system where it can be utilised. To move a container to ilifu, a user can follow this [user guide](tech_docs/container_registry) to push the container to the [IDIA Singularity Registry Server](https://sregistry.idia.ac.za/) and then pull a container to ilifu or follow the [transfers guide](data/data_transfer) to move container to ilifu.

There are several ways a user can build a container, including: creating a sandbox, building from a Docker image, building from the Singularity hub, building from an existing Singularity container or through a recipe or definition file . Additional information for building containers can be found at the [Singularity website](https://docs.sylabs.io/guides/latest/user-guide/build_a_container.html).

The recommended way to build a container for the ilifu system is through using a recipe. A recipe allows for reproducability of the container environment and allows for containers to be more easily referenced in research publications. Recipes define the way a container is built, which OS system is abstracted from within the container, and what files, libraries, packages and environmental variables and dependencies are included in the container.

Here is an example of the SoFiA2 container recipe, the recipe file is called `sofia2.def`:

```text
Bootstrap: debootstrap
MirrorURL: http://archive.ubuntu.com/ubuntu/
OSVersion: focal

%help
	This container includes SoFiA2 master branch

%environment
	export LC_ALL=C
	export SOFIA2_PATH="/opt/SoFiA-2"
	export PATH="$PATH:/opt/SoFiA-2"

%post
	# Installation of initial packages
	export DEBIAN_FRONTEND=noninteractive
	apt-get update -y
	apt-get install -y software-properties-common
	add-apt-repository -y universe
	apt-get install -y wget vim apt-utils git build-essential make bzip2 curl pkg-config python3-pip python-is-python3 libpng-dev

	# Install SoFiA2
	apt-get install -y gcc wcslib-dev libopenmpi-dev openmpi-bin openmpi-common
	cd /opt
	git clone https://github.com/SoFiA-Admin/SoFiA-2.git
	cd SoFiA-2
	./compile.sh -fopenmp

	# Cleanup the container
	apt-get clean
	apt-get autoclean
```

In the example above the operating system that is abstracted or seen from within the container is Ubuntu 20.04 focal. Environmental variables and paths within the container are set within the `%environment` section. Installation of packages and software is undertaken in the `%post` section. In this example no `%runscript` is initiated but could be instantiated to run `sofia` when a container session is initialled using the `run` command. Additional information about Singularity recipes can be found [here](https://docs.sylabs.io/guides/latest/user-guide/definition_files.html).

In order to build the container from the recipe, the following command can be used:

```shell
$ sudo singularity build sofia2.sif sofia2.def 
INFO:    Starting build...
I: Retrieving InRelease 
I: Checking Release signature
I: Valid Release signature (key id F6ECB3762474EDA9D21B7022871920D1991BC93C)
I: Retrieving Packages 
I: Validating Packages 
I: Resolving dependencies of required packages...
I: Resolving dependencies of base packages...
I: Checking component main on http://archive.ubuntu.com/ubuntu...
I: Retrieving adduser 3.118ubuntu2
I: Validating adduser 3.118ubuntu2
I: Retrieving apt 2.0.2
I: Validating apt 2.0.2
...
```

This command will build a container using the `sofia2.def` file and will name the container `sofia2.sif`. The container can then be copied to the ilifu cloud and run using the `shell` or `exec` command.

### Using a custom container as a Jupyter kernel

You can use a custom container as a python Jupyter kernel. The kernel will then appear with the system defined kernels that already exist in JupyterHub. If you launch a notebook using the custom kernel you will have access to all the python packages included in the container and would be able to access the container environment from inside the notebook, for example, issuing terminal commands using `!`.

In order to achieve this, the `ipykernel` python package must be installed in the container for the version of python that you wish to use as the Jupyter kernel. Outside the container, in your /users/ directory, create a folder in `$HOME/.local/share/jupyter/kernels/` and create a `kernel.json` file inside this new folder. The path for the `kernel.json` file should look something like `$HOME/.local/share/jupyter/kernels/example_kernel/kernel.json`. Inside the 'kernel.json' include the following:

```json
{
    "display_name": "<kernel_name>",
    "language": "python",
    "argv": [
        "singularity", "exec", "<path/to/container/container.simg>", "<path/to/python_executable>",
        "-m",
        "ipykernel_launcher",
        "-f",
        "{connection_file}"
        ]
}
```

where `<kernel_name>` is the name that will appear in the JupyterHub kernel menu, `<path/to/container/container.simg>` is the path to the container you wish to use as a kernel, and the `<path/to/python_executable>` is the path to the python executable inside the container (this must be the version of python you wish to use as a kernel, for example 2.7 or 3.6). Once this is complete you should be able to select your custom kernel from the kernel menu within JupyterHub.

## Environment modules

The [Lmod environment module system](https://lmod.readthedocs.io/en/latest/) is available on the cluster. The [online user documentation](https://lmod.readthedocs.io/en/latest/010_user.html) serves as a comprehensive guide to using lmod in general.

### Checking available modules

Use the `module avail` command, e.g.

```bash
$ module avail

------------------------------ /software/modules/common -------------------------------
   LAPACK/3.9.0                    java/openjdk-14.0.1 (D)    python/2.7.18
   R/RStudio1.2.5042-R4.0.0        maven/3.6.3                python/3.7.7
   R/3.6.3                         mono/6.8.0.123             python/3.8.2
   R/4.0.0                  (D)    openBLAS/0.3.9             python/3.8.3  (D)
   drmaa/1.1.1                     openmpi/3.1.6
   java/jre-1.8.0_261              openmpi/4.0.3       (D)

-------------------------------- /software/modules/bio --------------------------------
   bcbio/1.2.3           genomestrip/2.00.1958    popgen/0.1
   bcftools/1.10.2       htslib/1.10.2            prsice-2/2.3.1d
   canvas/1.40.0.1613    plink/2.00a2.3           samtools/1.10

-------------------------- /usr/share/lmod/lmod/modulefiles ---------------------------
   Core/lmod/6.6    Core/settarg/6.6

  Where:
   D:  Default Module

Use "module spider" to find all possible modules.
Use "module keyword key1 key2 ..." to search for all possible modules matching any of
the "keys".
```

*Note: CBIO users will notice they have an additional section for modules found in `/cbio/soft/lmod`.*

### Loading and using modules

Use the `module add` command, e.g.

```bash
USERNAME@compute-101:~$ R --version  # this won't work until the module is added

Command 'R' not found, but can be installed with:

apt install r-base-core
Please ask your administrator.

USERNAME@compute-101:~$ module add R/4.0.0
USERNAME@compute-101:~$ R --version
R version 4.0.0 (2020-04-24) -- "Arbor Day"
Copyright (C) 2020 The R Foundation for Statistical Computing
Platform: x86_64-pc-linux-gnu (64-bit)

R is free software and comes with ABSOLUTELY NO WARRANTY.
You are welcome to redistribute it under the terms of the
GNU General Public License versions 2 or 3.
For more information about these matters see
https://www.gnu.org/licenses/.
```

### Checking which modules are loaded

Use the `module list` command, e.g.

```bash
USERNAME@compute-101:/cbio/soft/lmod$ module list
No modules loaded
USERNAME@compute-101:/cbio/soft/lmod$ module add bio/svtoolkit/2.00.1918
USERNAME@compute-101:/cbio/soft/lmod$ module list

Currently Loaded Modules:
  1) jdk/11.0.2   2) slurm-drmaa/1.1.0   3) bio/htslib/1.9   4) R/3.6.1   5) bio/svtoolkit/2.00.1918
```

## RStudio

The R/RStudio container comes in two flavours: one for the astronomy community; and one for the bioinformatics community, where
the only difference between them is the default selection of packages that are installed. The astro variant can be found at `/idia/software/containers/bionic-R3.6.1-RStudio1.2.1335-astro.simg` while the bioinformatics variant can be found at `/cbio/images/bionic-R3.6.3-RStudio1.2.5042-bio.simg`. The examples below will be given for the bio container.

### Running R

It is recommended that the following script be created `~/bin/R` (remember to `chmod u+x ~/bin/R`):

```bash
#!/bin/bash
export R_INSTALL_STAGED=false
singularity run --app R /cbio/images/bionic-R3.6.3-RStudio1.2.5042-bio.simg "$@"
```

<sup>* See the [note](#note-on-installing-packages) below on installing packages</sup>

This will allow you to run `R` as normal (you may need to log out and in again if you don't already have scripts in `~/bin`).

### Running Rscript

Similarly you should create the script `~/bin/Rscript`:

```bash
#!/bin/bash
export R_INSTALL_STAGED=false
singularity run --app Rscript /cbio/images/bionic-R3.6.3-RStudio1.2.5042-bio.simg "$@"
```

<sup>* See the [note](#note-on-installing-packages) below on installing packages</sup>

### Running RStudio Server

#### How to launch RStudio Server

RStudio has been updated to be launched via a the use of modules (which is described in more detail [below](#loading-and-using-modules))

The procedure is to start an interactive job, add the RStudio module and run the `rstudio` as below:

```bash
USERNAME@slurm-login:~$ srun --nodes=1 --tasks=1 --mem=8g --time 08:00:00 --job-name="rstudio test" --pty bash
USERNAME@compute-101:~$ module load R/RStudio2025.05.1-513-R4.5.1
USERNAME@compute-101:~$ rstudio
The environment variable RSTUDIO_PASSWORD was not set, so your password has been chosen for you. It's: BcOaaYLmpjfufcQDozchq79rpZAdjo
Running rserver on port 53997
To connect to this server run this on your local machine:
    ssh -A USERNAME@compute-101 -o "ProxyCommand=ssh USERNAME@slurm.ilifu.ac.za nc compute-101 22" -L8081:localhost:53997
then visit http://localhost:8081 in your browser and use the username "USERNAME" to login with the password "BcOaaYLmpjfufcQDozchq79rpZAdjo"
(You may need to choose a different port (other than 8081), so remember to change this in both the ssh and browser)
```

Note the instructions on how to access the rstudio server now from your own machine: these need to be run on the machine you're working on (rather than on the login / compute node). *The port and password will change each time you run the `rstudio` command.* When you visit the url on your local browser (http://localhost:8081) you will be presented with a login screen. Use your ilifu username and the password provided:

<img src="/_media/rstudio_login.png" alt="rsudio login page" width=800 />

You will then be presented with an rstudio session:

<img src="/_media/rstudio_session.png" alt="rstudio session" width=800 />

If you don't want the automated/random password to be created then you can set your own password using the environmental variable `RSTUDIO_PASSWORD`, i.e.
```bash
USERNAME@compute-101:~$ export RSTUDIO_PASSWORD="this is a long password, HoopLA"
USERNAME@compute-101:~$ rstudio
Running rserver on port 60759
To connect to this server run this on your local machine:
    ssh -A USERNAME@compute-101 -o "ProxyCommand=ssh USERNAME@slurm.ilifu.ac.za nc compute-101 22" -L8081:localhost:60759
then visit http://localhost:8081 in your browser and use the username "USERNAME" to login with the password "this is a long password, HoopLA"
(You may need to choose a different port (other than 8081), so remember to change this in both the ssh and browser)
```

#### Old way of launching RStudio Server (You may need this if you're using one of the older CBIO RStudio images)

Should you wish to use RStudio Server the process is slightly more complicated — largely due to the process of ensuring the security of the RStudio session as well as allowing several simultaneous sessions. Firstly one should configure `ssh` in such a way that it is simple to connect to a worker node once a job is running. The easiest way it to add the following to your local `~/.ssh/config` file:

```bash
Host *.ilifu.ac.za
    User USERNAME
    ForwardAgent yes

Host compute-*
    Hostname %h
    User USERNAME
    StrictHostKeyChecking no
    ProxyCommand ssh slurm.ilifu.ac.za nc %h 22
```

One should substitute in your ilifu `USERNAME` in the above script.

Next is the process of starting an interactive job and launching RStudio. To begin start an interactive job – below is an example of launching a single node / 4 core job with 32Gb of ram:

```console
USERNAME@slurm-login:~$ srun --nodes=1 --ntasks 4 --mem=32g --pty bash
USERNAME@compute-103:~$
```

Once the interactive session has begun on a specific node (in this case `compute-103`), RStudio can be launched as follows:

```console
USERNAME@compute-103:~$ RSTUDIO_PASSWORD='Make your own secure password here' /cbio/images/bionic-R3.6.3-RStudio1.2.5042-bio.simg
Running rserver on port 37543
```

This will launch an RStudio server listening on a random free port (in this case `37543`). Now one needs to port-forward from your local machine to the host machine. One connects to the appropriate node by running:

```bash
$ ssh compute-103 -L8082:localhost:37543
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-58-generic x86_64)
...
```

on your local machine. Specifically what this does is forward traffic on your local machine's port `8082` to the worker node's port `37543` (and it knows how to connect to `compute-103` by using the `.ssh/config` settings above). One may use any free local port – ssh will complain if you choose something that is not free with an error message approximating:

```bash
bind [127.0.0.1]:8000: Address already in use
channel_setup_fwd_listener_tcpip: cannot listen to port: 8000
```

Finally in your browser you can connect to http://localhost:8082 and you can login with your `USERNAME` and the `RSTUDIO_PASSWORD` which you set.

## Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com/) (or VS code, vscode) is an alternative interactive development environment to Jupyter. A Visual Code Studio server, using [Code Server](https://github.com/coder/code-server), can be launched as an interactive app from the [IDIA Science Gateway](https://gateway.idia.ac.za) application dashboard, and run in your web browser.

After selecting the Visual Studio Code from the application dashboard, select the number of cores and duration for your session, and select `Launch`.

<div style="text-align:center"><img src="/_media/vscode_launcher.png" alt="application dashboard" width=600 /></div>

The Visual Studio Code server will be launched on the [Devel partition](getting_started/access_ilifu?id=devel) in the ilifu Slurm environment, and after a moment, you'll be able to `Connect to Visual Studio Code Server`, opening the VS code web app in a new window in your web browser. Note that Visual Code Studio server is restricted to one session per user.

<div style="text-align:center"><img src="/_media/vscode_session.png" alt="application dashboard" width=600 /></div>

You can reconnect to a running VS code server session by going to `My Interactive Sessions` on the top menu bar in the application dashboard. 

### Old way of running Visual Code Studio

Running VS Code on the Slurm login node will impacted the performance of the Slurm login node, interfering with users' ability to submit and manage their Slurm jobs. The following setup ensures that VS Code server is run on the Devel partion (`compute-001`), and does not run code on the Slurm login node, however, the process has now been superseded by VS code being available through the application dashboard as a web app.

Firstly one should configure `ssh` in such a way that it is able to connect directly to an interactive job once it is running. The easiest way is to add the following to your local `~/.ssh/config` file:

```bash 
Host *.ilifu.ac.za
    User <USERNAME>
    ForwardAgent yes

Host compute-001
    User <USERNAME>
    ForwardAgent yes
    Hostname %h
    ProxyCommand ssh <USERNAME>@slurm.ilifu.ac.za nc %h 22

```

Next, an interactive job should be started and then connected to with VS Code. To start an interactive job, the `sinteractive` command is used. The below example extends the default length of 3 hours to 1 day by using the `--time` flag and allocates 4 CPUS using the `-c` flag. Currently, the maximum length for an interactive session is 5 days.

```bash
USERNAME@slurm-login:~$ sinteractive --time=1-00:00:00 -c 4
```

Note that it also possible to run the sinteractive session in a tmux session. This allows the interactive job to persist when losing connectivity to the Slurm login node.

Lastly use VS Code's remote explorer to connect to compute-001. It will ask for the operating system of the remote server (pick Linux) and will then install the necessary VS Code server software. You should then be able to use VS Code to browse your ilifu home directory and open an interactive terminal.

## Python virtual environments

Virtual envrionments provide isolated environments for python projects, in which you can customize the dependencies to suit your requirements. This kind of environment is ideal for prototyping and development as they are easy to set up and maintain. It is, however, important to note that virtual environments are limited to non-python libraries of the base operating system.

### Creating a virtual environment

`virtualenv` is the package available for creating environments and can be used with

```bash
$ virtualenv /path/to/virtualenv
```

This will create a virtual environment with the name *virtualenv* (any name can be used here) at the specified path. Note that environments created in shared folders will be accessible to anyone with access to the folder, and similarly environments created in private folders will be accessible only to the user.

The `virtualenv` command will create an environment using the version of python available on the current `$PATH` which by default is the system `python 3.8.10`. If you want to use a different version of python, you can load the corresponding module from those available before creating the virtual environment

```bash
$ module load python/2.7.18
$ which python
/software/common/python/2.7.18/bin/python
```

A created virtual environment can then be activated with

```bash
$ source /path/to/virtualenv/bin/activate
(virtualenv)$
```
The name of the virtual environment will show enclosed in brackets before the command prompt cursor to indicate the environment is activated.

Specific python packages or a requirements list can then be installed using

```bash
(virtualenv)$ pip install <python_package>
```
```bash
(virtualenv)$ pip install -r requirements.txt
```

More information on `virtualenv` can be found in its [documentation](https://virtualenv.pypa.io/en/latest/user_guide.html#introduction) and on our [online training site](https://www.ilifu.ac.za/latest-training/#advanced1).

### A virtual environment as a Jupyter kernel

Virtual envrionments can also be used as Jupyter kernels. This is useful if you have a python configuration not already available on the cluster that you wish to develop in or test in a Jupyter session. 

Once a virtual environment is activated, you must install the `ipykernel` package. You can then run the following commmand to install a kernel for the virtual environment.

```bash
(virtualenv)$ ipython kernel install --name "my_python_kernel" --user

Installed kernelspec my_python_kernel in /users/USERNAME/.local/share/jupyter/kernels/my_python_kernel
```

Note the kernel can be named anything, but it is recommended to use something descriptive of the environment's function. The kernel will then be available in the Jupyter Launcher. 

### Installing niche packages

If you require a single, less common package to use in conjunction with an existing kernel, you can install it for your user account with

```bash
$ pip install --user <python_package>
```

This command needs to be run from a worker node that has access to the `pip` command, either by using a Python module or by shelling inside a container. This is most easily done through a command line terminal started from the Jupyter Launcher. Note that packages installed this way in a user space can conflict with the same packages in existing kernels, and as such this method should only be used for very use-case specific packages. Note that to use a package in conjunction with an existing kernel, the pip python version must correspond to the python version of the kernel (3.6, 3.7 etc.).
