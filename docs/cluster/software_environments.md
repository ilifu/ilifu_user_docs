# Supported Software Environments

For Astronomy, IDIA provides a number of supported software environments on Ilifu. These are provided principally through Singularity containers. More details of the bioinformatics suite of supported software will be added here later.

## Singularity Containers

Containers are unit software packages that contain all the software, files, libraries, dependencies and environmental variables necessary to run a particular task or workflow. Containers are encapsulated software environments and abstract the software and applications from the underlying operating system. This allows users to run workflows in customized environments, switch between environments, and to share these environments with colleagues and research teams.

### Using a container

There are several ways one can use a Singularity container.

#### 1. Interactive shell command

A user is able to open a Singularity container as an interactive shell and issue command line tasks within the environment that the container provides. To do this a user calls the Singularity container using the `shell` command. 

    user:~$ singularity shell /data/exp_soft/containers/casa-stable.img

This command will spawn a new shell inside the container, in this case the `casa-stable` container, allowing the user to interact with the container environment. The user can then run software or develop workflows interactively.

#### 2. Exec command

A user is able to execute a script within the container environment using the singularity `exec` command.

    user:~$ singularity exec /data/exp_soft/containers/sourcefinding_py3.simg python myscript.py

This command will execute the script, `myscript.py`, using Python within the `sourcefinding_py3` container. The script will have access to all the Python libraries that have been included in the container.

Similary,

    user:~$ singularity exec /data/exp_soft/containers/casa-stable.img casa --log2term --nologger -c "print 'hello world'"

will execute `print 'hello world'` using the CASA software package that is contained in the `casa-stable` container.

The `exec` command can also be used to initiate an interative session. For example:

    user:~$ singularity exec /data/exp_soft/containers/casa-stable.img casa --log2term --nologger
    
The above command will run the CASA software within the `casa-stable` container environment and will allow the user to use the environment interactively. However, the primary use of the `exec` command is to execute scripts without interaction, for example on the SLURM cluster.

#### 3. Run command

When containers are built a runscript can be designated in the recipe file. This allows programs to be automatically initiated using a `run` command. For example:

    user:~$ singularity run /data/exp_soft/containers/sourcefinding_py3.simg
    
The runscript for this container is:

    %runscript

        /anaconda3/bin/python "$@"

Running this container using the `run` command will initialize a container session and open the Python package (from Anaconda3 in this case) contained within the container, allowing the user to run python commands interactively. However, as soon as the Python command line is exited the container session is closed.

A number of the containers that are supported by Ilifu do not include runscripts and therefore cannot be used using the `run` command.

### Available containers

Several containers have been developed and are currently maintained. These containers include the following (**See the dropdown information for container details**):

<details>
<summary>Jupter-Casa container</summary>

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
<summary>kern-2 container</summary>

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
<summary>kern-4 container</summary>

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
<summary>meerlicht container</summary>
  
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
<summary>pink container</summary>
  
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
<summary>sourcefinding_py3 container</summary>

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

In order to build containers a user requires root access on the system where the container is being built. Therefore, users cannot build containers directly on the Ilifu system. However, containers can be built in an environment where a user has root access, and then the container can be moved to the Ilifu system where it can be utilized.

There are several ways a user can build a container, including: creating a sandbox, building from a Docker image, building from the Singularity hub, building from an existing Singularity container or through a recipe or definition file . Additional information for building containers can be found at the [Singularity website](https://www.sylabs.io/guides/3.0/user-guide/build_a_container.html#).

The recommended way to build a container for the Ilifu system is through using a recipe. A recipe allows for reproducability of the container environment and allows for containers to be more easily referenced in research publications. Recipes define the way a container is built, which OS system is abstracted from within the container, and what files, libraries, packages and environmental variables and dependencies are included in the container.

Here is an example of the PINK container recipe, the recipe file is called `pink.def`:

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

In the example above the operating system that is abstracted or seen from within the container is Ubuntu 16.04 xenial. Environmental variables and paths within the container are set within the `%environment` section. Copying files into the container from the root environment where the container is being built is completed in the `%setup` section (this is now `%file` in later versions of Singularity). Installation of packages and software is undertaken in the `%post` section. In this example no `%runscript` is initiated but could be instantiated to run PINK when a container session is initialled using the `run` command. Additional information about Singularity recipes can be found [here](https://www.sylabs.io/guides/3.0/user-guide/build_a_container.html#building-containers-from-singularity-definition-files).

In order to build the container from the recipe, the following command can be used:

    root:~$ singularity build pink.simg pink.def
    
This command will build a container using the `pink.def` file and will name the container `pink.simg`. The container can then be copied to the Ilifu cloud and run using the `shell` or `exec` command.

### Using a custom container as a Jupyter kernel

You can use a custom container as a python Jupyter kernel. The kernel will then appear with the system defined kernels that already exist in JupyterHub. If you launch a notebook using the custom kernel you will have access to all the python packages included in the container and would be able to access the container environment from inside the notebook, for example, issuing terminal commands using `!`.

In order to achieve this, the `ipykernel` python package must be installed in the container for the version of python that you wish to use as the Jupyter kernel. Outside the container, in your /users/ directory, create a folder in `$HOME/.local/share/jupyter/kernels/` and create a `kernel.json` inside this new folder. The path for the `kernel.json` file should look something like `$HOME/.local/share/jupyter/kernels/example_kernel/kernel.json`. Inside the 'kernel.json' include the following:

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

where '<kernel_name>' is the name that will appear in the JupyterHub kernel menu, <path/to/container/container.simg> is the path to the container you wish to use as a kernel, and the <path/to/python_executable> is the path to the python executable inside the container (this must be the version of python you wish to use as a kernel, for example 2.7 or 3.6). Once this is complete you should be able to select your custom kernel from the kernel menu within JupyterHub.

