# Supported Software Environments

For Astronomy, IDIA provides a number of supported software environments on ilifu. These are provided principally through [singularity containers](#singularity-containers). Bioinformatics software is also supported via containers, but also through the use of [environment modules](#environment-modules).

## Singularity Containers

Containers are unit software packages that contain all the software, files, libraries, dependencies and environmental variables necessary to run a particular task or workflow. Containers are encapsulated software environments and abstract the software and applications from the underlying operating system. This allows users to run workflows in customized environments, switch between environments, and to share these environments with colleagues and research teams.

### Using a container

The container images that are maintained by the support team can be found at `/idia/software/containers/`. There are a number of ways one can use a Singularity container, including both interactive and non-interactive sessions, as detailed below.

#### 1. Interactive shell command

A user is able to open a Singularity container as an interactive shell and issue command line tasks within the environment that the container provides. To do this a user calls the Singularity container using the `shell` command.

```shell
$ singularity shell /idia/software/containers/casa-stable.img
Singularity: Invoking an interactive shell within container...

Singularity casa-stable-5.1.1.img:~>
```

This command will spawn a new shell inside the container, in this case the `casa-stable` container, allowing the user to interact with the container environment. The user can then run software or develop workflows interactively.

#### 2. Exec command

A user is able to execute a script within the container environment using the singularity `exec` command.

```shell
$ singularity exec /idia/software/containers/sourcefinding_py3.simg python myscript.py
hello world!
$
```

This command will execute the script, `myscript.py`, using Python within the `sourcefinding_py3` container. The script will have access to all the Python libraries that have been included in the container.

Similary,

```shell
$ singularity exec /idia/software/containers/casa-stable.img casa --log2term --nologger -c "print 'hello world'"

=========================================
The start-up time of CASA may vary
depending on whether the shared libraries
are cached or not.
=========================================

IPython 5.1.0 -- An enhanced Interactive Python.

CASA 5.1.1-5   -- Common Astronomy Software Applications

2019-04-01 13:49:49     INFO    ::casa  CASA Version 5.1.1-5
--> CrashReporter initialized.
hello world
$
```

will execute `print 'hello world'` using the CASA software package that is contained in the `casa-stable` container.

The `exec` command can also be used to initiate an interative session. For example:

```shell
$ singularity exec /idia/software/containers/casa-stable.img casa --log2term --nologger

=========================================
The start-up time of CASA may vary
depending on whether the shared libraries
are cached or not.
=========================================

IPython 5.1.0 -- An enhanced Interactive Python.

CASA 5.1.1-5   -- Common Astronomy Software Applications

2019-04-01 13:51:39     INFO    ::casa  CASA Version 5.1.1-5
--> CrashReporter initialized.
Enter doc('start') for help getting started with CASA...
Using matplotlib backend: TkAgg

CASA <1>:

```

The above command will run the CASA software within the `casa-stable` container environment and will allow the user to use the environment interactively. However, the primary use of the `exec` command is to execute scripts without interaction, for example on the SLURM cluster.

#### 3. Run command

When containers are built a runscript can be designated in the recipe file. This allows programs to be automatically initiated using a `run` command. For example:

```shell
$ singularity run /idia/software/containers/SF-PY3-bionic.simg
Python 3.6.5 |Anaconda, Inc.| (default, Apr 29 2018, 16:14:56)
[GCC 7.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

The runscript for this container is:

```text
%runscript
    /anaconda3/bin/python "$@"
```

Running this container using the `run` command will initialize a container session and open the Python package (from Anaconda3 in this case) contained within the container, allowing the user to run python commands interactively. However, as soon as the Python command line is exited the container session is closed.

A number of the containers that are supported by ilifu do not include runscripts and therefore cannot be used using the `run` command.

### Available containers

Several containers have been developed and are currently maintained. These containers include the following (**See the dropdown information for specific container details by clicking on the relevant arrow below**):

<details>
<summary id="jupyter-casa-container">jupter-casa container</summary>

| Name                     | Recipe File            | URL                                                   | OSVersion |
|--------------------------|------------------------|-------------------------------------------------------|-----------|
| jupyter-casa-latest.simg | jupyter-casa-build.def | idia-container-casakernel/jupyter-casa-build.def      | xenial    |

| Packages & Libraries           |                    |                            | Python Libraries  |
|--------------------------------|--------------------|----------------------------|-------------------|
| ant                            | libcfitsio3-dev    | libsqlite3-0               | foolscap          |
| antlr                          | libdbus-1-dev      | libsqlite3-dev             | matplotlib        |
| apt-utils                      | libdbus-c++-1-0v5  | libwcs5                    | nose              |
| ASAP                           | libdbus-c++-dev    | libxerces-c-dev            | numpy             |
| bison                          | libdbus-cpp-dev    | libxerces-c3.1             | scipy             |
| CasaCORE                       | libdbus-glib-1-2   | libxml2-dev                |                   |
| cmake                          | libdbusmenu-glib4  | libxslt1-dev               |                   |
| dbus-x11                       | libeigen3-dev      | libxslt1.1                 |                   |
| doxygen                        | libfftw3-dev       | pgplot5                    |                   |
| flex                           | libfftw3-dev       | python-dbus                |                   |
| g++-6                          | libfftw3-doc       | python-dev                 |                   |
| gcc-6                          | libfftw3-double3   | python-foolscap            |                   |
| GCWrap                         | libfftw3-single3   | python-matplotlib          |                   |
| gfortran                       | libgsl-dev         | python-nose                |                   |
| ipython                        | libgsl2            | python-numpy               |                   |
| juptyer                        | libhdf5-serial-dev | python-numpy-dev           |                   |
| libantlr-dev                   | libjdom1-java      | python-pip                 |                   |
| libantlr-java                  | libjfreechart-java | python-scipy               |                   |
| libblas-dev                    | liblapack-dev      | python2.7                  |                   |
| libboost-all-dev               | liblapack3         | qt4-dev-tools              |                   |
| libboost-dev                   | liblapacke         | refits                     |                   |
| libboost-filesystem-dev        | liblapacke-dev     | scons                      |                   |
| libboost-filesystem1.58.0      | liblog4cxx-dev     | software-properties-common |                   |
| libboost-program-options-dev   | libncurses5-dev    | sqlite3                    |                   |
| libboost-program-options1.58.0 | libpgsbox-dev      | sqlite3-doc                |                   |
| libboost-python-dev            | libpgsbox-dev      | subversion                 |                   |
| libboost-python1.58.0          | libpgsbox5         | swig                       |                   |
| libboost-regex-dev             | libqt4-dbus        | tix                        |                   |
| libboost-regex1.58.0           | libqt4-dev         | tix-dev                    |                   |
| libboost-serialization-dev     | libqwt-dev         | unzip                      |                   |
| libboost-system-dev            | libqwt5-qt4-dev    | vim                        |                   |
| libboost-system1.58.0          | libqwt6abi1        | wcslib-dev                 |                   |
| libboost-thread-dev            | libreadline-dev    | wget                       |                   |
| libcfitsio2                    | libsakura          | xvfb                       |                   |

</details>

<details>
<summary id="casa-stable-container">casa-stable container</summary>

| Name        | Def file        | URL                                        | OSVersion |
|-------------|-----------------|--------------------------------------------|-----------|
| casa-stable | casa-stable.def | idia-container-casa-stable/casa-stable.def | CentOS    |

| Packages and Libraries |                    |                  |                 |
|------------------------|--------------------|------------------|-----------------|
| casa                   | libfontconfig      | libXcursor-dev*  | libXrender-dev* |
| cmake                  | libfontconfig-dev* | libXext-dev*     | python          |
| fontconfig-dev         | libGL-dev*         | libXft*          | svn             |
| fontconfig-dev*        | libGL*             | libXi-dev*       | vim             |
| gcc                    | libSM-dev*         | libXinerama-dev* | wget            |
| git                    | libX11-dev*        | libXrandr-dev*   |                 |

</details>

<details>
<summary id="casameer-container">casameer container</summary>

Casameer container used in the IDIA Pipeline software, contains CASA 5.4.1 and is appropriate for use with MPI.

| Name        | Def file        | URL                                        | OSVersion |
|-------------|-----------------|--------------------------------------------|-----------|
| casameer    |                 |                                            | CentOS    |

| Packages and Libraries |
|------------------------|
| casa-5.4.1             |
| ghostscript            |
| xvfb-run               |

</details>

<details>
<summary id="kern-2-container">kern-2 container</summary>

| Name   | Def file   | URL                            | OSVersion |
|--------|------------|--------------------------------|-----------|
| kern-2 | kern-2.def | idia-container-kern/kern-2.def | xenial    |

| Packages & Libraries  |                            |                           | Python Libraries |
|-----------------------|----------------------------|---------------------------|------------------|
| 21cmfast              | libcasasynthesis1          | python-attrdict           | atpy             |
| aips                  | libcommon                  | python-casacore           | psutils          |
| aoflagger             | libdocker                  | python-galsim             | attrdict         |
| aoflagger-dev         | libdppp                    | python-katdal             | casacore         |
| casacore-data         | libdppp-aoflag             | python-katpoint           | galsim           |
| casacore-dev          | libelementresponse         | python-katversion         | katdal           |
| casacore-doc          | liblmwcommon               | python-kittens            | katpoint         |
| casacore-tools        | liblofar-pyparameterset    | python-lofar              | katversion       |
| casalite              | liblofar-pyparmdb          | python-meqtrees-cattery   | kittens          |
| casarest              | liblofar-pystationresponse | python-meqtrees-timba     | lofar            |
| cassbeam              | liblofar-pytools           | python-montblanc          | meqtrees-cattery |
| chgcentre             | liblofarft                 | python-owlcat             | meqtrees-timba   |
| cub-dev               | liblofarstman              | python-presto             | montblanc        |
| dialog                | libmeqtrees-timba0         | python-purr               | owlcat           |
| drive-casa            | libmessagebus              | python-pymoresane         | presto           |
| dspsr                 | libms                      | python-pyxis              | purr             |
| dysco                 | libmslofar                 | python-qwt5-doc           | pymoresane       |
| galsim                | libparmdb                  | python-qwt5-qt4           | pyxis            |
| galsim-dev            | libplc                     | python-rfimasker          | qwt5-doc         |
| galsim0               | libpurify-dev              | python-scatterbrane       | qwt5-qt4         |
| karma                 | libpurify2.0               | python-sourcery           | rfimasker        |
| libaoflagger0         | libpythondppp              | python-tigger             | scatterbrane     |
| libapplcommon         | libsopt-dev                | python-tkp                | sourcery         |
| libawimager2lib       | libsopt2.0                 | python-pip                | tigger           |
| libbbscontrol         | libspdlog-dev              | python-transitions        | tkp              |
| libbbskernel          | libspwcombine              | python3-casacore          | transitions      |
| libblob               | libstationresponse         | python3-transitions       |                  |
| libcasa-casa2         | libtransport               | rpfits                    |                  |
| libcasa-coordinates2  | libwsclean0                | sagecal                   |                  |
| libcasa-derivedmscal2 | lofar-dev                  | sigproc                   |                  |
| libcasa-fits2         | lofar-doc                  | sigpyproc                 |                  |
| libcasa-images2       | meqtrees                   | simfast21                 |                  |
| libcasa-lattices2     | Meqtrees-timba             | simms                     |                  |
| libcasa-meas2         | Montage                    | singularity-container     |                  |
| libcasa-measures2     | msutils                    | stimela                   |                  |
| libcasa-mirlib2       | mt-imager                  | tempo                     |                  |
| libcasa-ms2           | multinest                  | tempo2                    |                  |
| libcasa-msfits2       | obit                       | texlive-fonts-recommended |                  |
| libcasa-python2       | oskar                      | tirific                   |                  |
| libcasa-python3-2     | parseltongue               | tmv-dev                   |                  |
| libcasa-scimath-f2    | presto                     | tmv0                      |                  |
| libcasa-scimath2      | psrcat                     | wsclean                   |                  |
| libcasa-tables2       | psrchive                   | wsclean-dev               |                  |
| libcasasynthesis-dev  | purify                     |                           |                  |

</details>

<details>
<summary id="kern-4-container">kern-4 container</summary>

| Name  | Def file  | URL                             | OSVersion |
|-------|-----------|---------------------------------|-----------|
| kern4 | kern4.def | idia-container-kern-4/kern4.def | bionic    |

| Packages & Libraries |                |                       | Python Libraries |
|----------------------|----------------|-----------------------|------------------|
| 21cmfast             | katdal         | purr                  | numpy            |
| aips                 | karma          | pyfftw                | atpy             |
| astro-tigger         | kittens        | pymonetdb             | scipy            |
| astro-tigger-lsm     | lofar          | pymoresane            | psutil           |
| attrdict             | losoto         | python-typing         | pyfits           |
| bl-sigproc           | meqtrees-timba | pyxis                 | typing           |
| blimpy               | Montage        | PyBDSF                | pywcs            |
| blitz                | msutils        | rfimasker             |                  |
| casalite             | multinest      | rmextract             |                  |
| casarest             | obit           | rpfits                |                  |
| chgcentre            | owlcat         | sagecal               |                  |
| ctypesgen            | parseltongue   | sched                 |                  |
| cub                  | peasoup        | sigpyproc             |                  |
| ddfacet              | polygon2       | simfast21             |                  |
| difmap               | ppgplot        | simms                 |                  |
| drive-casa           | prefactor      | singularity-container |                  |
| dysco galsim         | presto         | tempo                 |                  |
| gbt-seti             | psrcat         | tigger                |                  |
| gsm                  | psrchive       | tirific               |                  |
| heimdall-astero      | psrdada        | turbo-seti            |                  |

</details>

<details>
<summary id="meerlicht-container">meerlicht container</summary>

| Name      | Def file      | URL                                    | OSVersion |
|-----------|---------------|----------------------------------------|-----------|
| meerlicht | meerlicht.def | idia-container-meerlicht/meerlicht.def | xenial    |

| Packages & Libraries |                   |                   | Python Libraries |
|----------------------|-------------------|-------------------|------------------|
| Anaconda             | dgursoy-pyfftw    | psfex             | astropy          |
| anaconda-ephem       | ecpy-watchdog     | rclone            | psycopg2         |
| anaconda-psycopg2    | fitsio            | sextractor        | pyephem          |
| anaconda-pyqt        | gcc               | sip_tpv           | pyqt             |
| apt-utils            | git               | slackclient       |                  |
| astrometry           | libbz2-dev        | sphinx-automodapi |                  |
| astropy-ccdproc      | libcairo2-dev     | swarp             |                  |
| astropy-lmfit        | libjpeg-dev       | swig              |                  |
| astropy-photutils    | libnetpbm10-dev   | vim               |                  |
| atlas                | libplplot-dev     | wcstools          |                  |
| auto-ushlex          | libpng12-dev      | wget              |                  |
| build-essential      | milk              | wwwget            |                  |
| bzip2                | netlib-lapack     | Z0GY              |                  |
| cdsclient            | netpbm            | zip               |                  |
| conda-forge-sphinx   | openastronomy-sep | zlib1g-dev        |                  |

</details>

<details>
<summary id="pink-container">pink container</summary>

| Name | Def file | URL                          | OSVersion |
|------|----------|------------------------------|-----------|
| pink | pink.def | idia-container-pink/pink.def | xenial    |

| Packages & Libraries |         |      | Python Libraries |
|----------------------|---------|------|------------------|
| apt-utils            | doxygen | Pink |                  |
| build-essential      | gcc     | vim  |                  |
| cmake                | make    | wget |                  |

</details>

<details>
<summary id="sourcefinding-py3-container">sourcefinding_py3 container</summary>

| Name              | Def file                     | URL                                                           | OSVersion |
|-------------------|------------------------------|---------------------------------------------------------------|-----------|
| Source Finding P3 | sourcefinding_py3.def        | idia-container-sourcefinding-py3/sourcefinding_py3.def        | xenial    |
| Source Finding P3 | sourcefinding_py3_update.def | idia-container-sourcefinding-py3/sourcefinding_py3_update.def | xenial    |

| Packages & Libraries  |                            |                           | Python Libraries | Python Libraries |
|-----------------------|----------------------------|---------------------------|------------------|------------------|
| 21cmfast              | libcasa-python3-2          | python-casacore           | acor             | pyspark          |
| aips                  | libcasa-scimath-f2         | python-galsim             | aplpy            | pyvo             |
| Anaconda              | libcasa-scimath2           | python-katdal             | astroml          | pyxis            |
| Aegean                | libcasa-tables2            | python-katpoint           | astroML          | qwt5-doc         |
| AGNfitter             | libcasasynthesis-dev       | python-katversion         | astroML_addons   | qwt5-qt4         |
| aoflagger             | libcasasynthesis1          | python-kittens            | astroplan        | regions          |
| aoflagger-dev         | libcommon                  | python-lofar              | astropy          | reproject        |
| Astrometry            | libdocker                  | python-meqtrees-cattery   | astroquery       | rfimasker        |
| casacore-data         | libdppp                    | python-meqtrees-timba     | atpy             | scatterbrane     |
| casacore-dev          | libdppp-aoflag             | python-montblanc          | attrdict         | scikit-image     |
| casacore-doc          | libelementresponse         | python-owlcat             | casacore         | scikit-learn     |
| casacore-tools        | liblmwcommon               | python-presto             | ccdproc          | scikit-plot      |
| casalite              | liblofar-pyparameterset    | python-purr               | configobj        | scipy            |
| casarest              | liblofar-pyparmdb          | python-pymoresane         | corner           | sciserver        |
| cassbeam              | liblofar-pystationresponse | python-pyxis              | docopt           | seaborn          |
| chgcentre             | liblofar-pytools           | python-qwt5-doc           | easydict         | sep              |
| cigale                | liblofarft                 | python-qwt5-qt4           | emcee            | sourcery         |
| cub-dev               | liblofarstman              | python-rfimasker          | galsim           | sourcery         |
| dialog                | libmeqtrees-timba0         | python-scatterbrane       | ginga            | specutils        |
| drive-casa            | libmessagebus              | python-sourcery           | glue             | sqlalchemy       |
| DS9                   | libms                      | python-tigger             | glueviz          | statsmodels      |
| dspsr                 | libmslofar                 | python-tkp                | h5py             | tensorflow       |
| dvipng                | libparmdb                  | python-transitions        | healpy           | theano           |
| dysco                 | libplc                     | python3-casacore          | hips             | tigger           |
| eazy-photoz           | libpurify-dev              | python3-transitions       | Ipykernel        | tkp              |
| emacs                 | libpurify2.0               | python3.6                 | IPython          | tqdm             |
| galfit                | libpythondppp              | qt5-default               | kapteyn          | transitions      |
| galsim                | libsopt-dev                | rpfits                    | katdal           | WCSAxes          |
| galsim-dev            | libsopt2.0                 | sagecal                   | katpoint         |                  |
| galsim0               | libspdlog-dev              | scamp                     | katversion       |                  |
| ginga                 | libspwcombine              | screen                    | keras            |                  |
| GPz                   | libstationresponse         | sed3fit                   | kittens          |                  |
| karma                 | libtransport               | sextractor                | lofar            |                  |
| Java8                 | libwsclean0                | sigproc                   | meqtrees-cattery |                  |
| lftp                  | lofar-dev                  | sigpyproc                 | meqtrees-timba   |                  |
| libaoflagger0         | lofar-doc                  | simfast21                 | montblanc        |                  |
| libapplcommon         | meqtrees                   | simms                     | Mpld3            |                  |
| libawimager2lib       | meqtrees-timba             | singularity-container     | nbconvert        |                  |
| libbbscontrol         | Montage                    | SoFiA                     | nbdime           |                  |
| libbbskernel          | msutils                    | stimela                   | numba            |                  |
| libblob               | mt-imager                  | swarp                     | numpy            |                  |
| libcasa-casa2         | multinest                  | tcsh                      | nway             |                  |
| libcasa-coordinates2  | nano                       | tempo                     | opencv-python    |                  |
| libcasa-derivedmscal2 | obit                       | tempo2                    | owlcat           |                  |
| libcasa-fits2         | oskar                      | texlive-fonts-recommended | pandas           |                  |
| libcasa-images2       | parseltongue               | texlive-latex-extra       | pandas           |                  |
| libcasa-lattices2     | presto                     | tirific                   | photutils        |                  |
| libcasa-meas2         | psrcat                     | tmv-dev                   | presto           |                  |
| libcasa-measures2     | psrchive                   | tmv0                      | purr             |                  |
| libcasa-mirlib2       | PUMA                       | Tractor                   | pydl             |                  |
| libcasa-ms2           | purify                     | wsclean                   | pymoc            |                  |
| libcasa-msfits2       | PyBDSF                     | wsclean-dev               | pymoresane       |                  |
| libcasa-python2       | python-attrdict            |                           | pyregion         |                  |

Packages installed in during the update:

| Packages & Libraries |          |       | Python Libraries | Python Libraries |
|----------------------|----------|-------|------------------|------------------|
| Astromatic           | eog      | PASTA | datalab-client   | pywcsgrid2       |
| Blobcat              | fits2hdf |       | pywcs            | tensorflow       |

</details>

### Building your own container

In order to build containers a user requires root access on the system where the container is being built. Therefore, users cannot build containers directly on the ilifu system. However, containers can be built in an environment where a user has root access, and then the container can be moved to the ilifu system where it can be utilized.

There are several ways a user can build a container, including: creating a sandbox, building from a Docker image, building from the Singularity hub, building from an existing Singularity container or through a recipe or definition file . Additional information for building containers can be found at the [Singularity website](https://www.sylabs.io/guides/3.0/user-guide/build_a_container.html#).

The recommended way to build a container for the ilifu system is through using a recipe. A recipe allows for reproducability of the container environment and allows for containers to be more easily referenced in research publications. Recipes define the way a container is built, which OS system is abstracted from within the container, and what files, libraries, packages and environmental variables and dependencies are included in the container.

Here is an example of the PINK container recipe, the recipe file is called `pink.def`:

```text
Bootstrap: debootstrap
MirrorURL: http://archive.ubuntu.com/ubuntu/
OSVersion: xenial
Include: software-properties-common

%environment
    export PATH=/software/pink/bin:$PATH

%setup
    cp pink-latest.tar $SINGULARITY_ROOTFS

%post
    apt-get update -y
    apt-get install -y doxygen wget vim apt-utils gcc make cmake build-essential
    mkdir /install /software
    mv /pink-latest.tar /install
    cd /install
    tar xfv pink-latest.tar

    # Create /users to bind home directories into the container.
    mkdir -p /users /scratch /data

    # Installation of PINK
    cd pink-latest
    mkdir build
    cd build
    cmake -DCMAKE_INSTALL_PREFIX=/software/pink  ..
    make -j 2
    make install
```

In the example above the operating system that is abstracted or seen from within the container is Ubuntu 16.04 xenial. Environmental variables and paths within the container are set within the `%environment` section. Copying files into the container from the root environment where the container is being built is completed in the `%setup` section (this is now `%file` in later versions of Singularity). Installation of packages and software is undertaken in the `%post` section. In this example no `%runscript` is initiated but could be instantiated to run PINK when a container session is initialled using the `run` command. Additional information about Singularity recipes can be found [here](https://www.sylabs.io/guides/3.0/user-guide/build_a_container.html#building-containers-from-singularity-definition-files).

In order to build the container from the recipe, the following command can be used:

```shell
# singularity build pink.simg pink.def
Using container recipe deffile: pink.def
Sanitizing environment
Adding base Singularity environment to container
I: Retrieving InRelease
I: Checking Release signature
I: Valid Release signature (key id 790BC7277767219C42C86F933B4FE6ACC0B21F32)
I: Retrieving Packages
I: Validating Packages
I: Resolving dependencies of required packages...
I: Resolving dependencies of base packages...
I: Checking component main on http://archive.ubuntu.com/ubuntu...
I: Retrieving adduser 3.113+nmu3ubuntu4
I: Validating adduser 3.113+nmu3ubuntu4
I: Retrieving apt 1.2.10ubuntu1
I: Validating apt 1.2.10ubuntu1
...
```

This command will build a container using the `pink.def` file and will name the container `pink.simg`. The container can then be copied to the ilifu cloud and run using the `shell` or `exec` command.

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
        "IPython.kernel",
        "-f",
        "{connection_file}"
        ]
}
```

where `<kernel_name>` is the name that will appear in the JupyterHub kernel menu, `<path/to/container/container.simg>` is the path to the container you wish to use as a kernel, and the `<path/to/python_executable>` is the path to the python executable inside the container (this must be the version of python you wish to use as a kernel, for example 2.7 or 3.6). Once this is complete you should be able to select your custom kernel from the kernel menu within JupyterHub.

### RStudio

The R/RStudio container comes in two flavours: one for the astronomy community; and one for the bioinformatics community, where
the only difference between them is the default selection of packages that are installed. The astro variant can be found at `/idia/software/containers/bionic-R3.6.1-RStudio1.2.1335-astro.simg` while the bioinformatics variant can be found at `/cbio/images/bionic-R3.6.1-RStudio1.2.1335-bio.simg`. The examples below will be given for the bio container.


#### Running R
It is recommended that the following script be created `~/bin/R` (remember to `chmod u+x ~/bin/R`):
```bash
#!/bin/bash
export R_INSTALL_STAGED=false
singularity run --app R /cbio/images/bionic-R3.6.1-RStudio1.2.1335-bio.simg "$@"
``` 
<sup>* See the note below on installing packages</sup>

This will allow you to run `R` as normal (you may need to log out and in again if you don't already have scripts in `~/bin`).

#### Running Rscript
Similarly you should create the script `~/bin/Rscript`:
```bash
#!/bin/bash
export R_INSTALL_STAGED=false
singularity run --app Rscript /cbio/images/bionic-R3.6.1-RStudio1.2.1335-bio.simg "$@"
```
<sup>* See the note below on installing packages</sup>

#### Running RStudio Server
Should you wish to use RStudio Server the process is slightly more complicated — largely due to the process of ensuring the security of the RStudio session as well as allowing several simultaneous sessions. Firstly one should configure `ssh` in such a way that it is simple to connect to a worker node once a job is running. The easiest way it to add the following to your local `~/.ssh/config` file:
```bash
Host *.ilifu.ac.za
    User USERNAME
    ForwardAgent yes

Host slwrk-*
    Hostname %h
    User USERNAME
    StrictHostKeyChecking no
    ProxyCommand ssh slurm.ilifu.ac.za nc %h 22
```
One should substitute in your ilifu `USERNAME` in the above script.

Next is the process of starting an interactive job and launching RStudio. To begin start an interactive job – below is an example of launching a single node / 4 core job with 32Gb of ram:
```console
USERNAME@slurm-login:~$ srun --nodes=1 --ntasks 4 --mem=32g --pty bash
USERNAME@slwrk-103:~$
```
Once the interactive session has begun on a specific node (in this case `slwrk-103`), RStudio can be launched as follows:
```console
USERNAME@slwrk-103:~$ RSTUDIO_PASSWORD='Make your own secure password here' /cbio/images/bionic-R3.6.1-RStudio1.2.1335-bio.simg
Running rserver on port 37543
```
This will launch an RStudio server listening on a random free port (in this case `37543`). Now one needs to port-forward from your local machine to the host machine. One connects to the appropriate node by running:
```bash
$ ssh slwrk-103 -L8082:localhost:37543
```
on your local machine. Specifically what this does is forward traffic on your local machine's port `8082` to the worker node's port `37543` (and it knows how to connect to `slwrk-103` by using the `.ssh/config` settings above). One may use any free local port – ssh will complain if you choose something that is not free with an error message approximating:
```bash
bind [127.0.0.1]:8000: Address already in use
channel_setup_fwd_listener_tcpip: cannot listen to port: 8000
```
Finally in your browser you can connect to http://localhost:8082 and you can login with your `USERNAME` and the `RSTUDIO_PASSWORD` which you set.

*Note on installing packages
The exported environmental variable `R_INSTALL_STAGED=false` in the above scripts is only necessary should you wish to install your own packages — [this is due to the home directories using the BeeGFS filesystem](http://r.789695.n4.nabble.com/Staged-installation-fail-on-some-file-systems-td4756897.html)). Should you wish to install packages from within an RStudio session you should run `export R_INSTALL_STAGED=false` before starting the server.

## Environment Modules

Coming soon.
