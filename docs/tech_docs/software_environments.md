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
<summary id="astro-r-container">astro-r container</summary>

**Description:** an R container with collection of R astronomy packages, including ProFound, ProFit and ProSpect.

**JupyterLab Kernel:** ASTRO-R

| Name                     | Recipe File            | Github repo     | OSVersion |
|--------------------------|------------------------|-----------------|-----------|
| ASTRO-R.simg             |                        |                 | bionic    |

| Packages and Libraries | R Libraries |               |           |
|------------------------|-------------|---------------|-----------|
| fftw                   | akima       | fftwtools     | nnet      |
| R                      | astro       | FITSio        | party     |
| R-essentials           | astrodatR   | knitr         | ProFit    |
|                        | BiocManager | lambda.r      | ProFound  |
|                        | data.table  | LaplacesDemon | ProSpect  |
|                        | devtools    | magicaxis     | rmarkdown |
|                        | EBImage     | mice          |           |

</details>

<details>
<summary id="casa-kernel-container">casa-kernel container</summary>

**Description:** a working development version of CASA which is controlled through the Jupyter Notebook. Open a new notebook with this kernel to run casa as a python module in a jupyter notebook.

**JupyterLab Kernel:** CASA 5.5

| Name                     | Recipe File            | Github repo                   | OSVersion |
|--------------------------|------------------------|-------------------------------|-----------|
| jupyter-casa-latest.simg | jupyter-casa-build.def | idia-container-casakernel     | xenial    |

| Packages and Libraries | Python Libraries |            |            |
|------------------------|------------------|------------|------------|
| CASA 5.5               | bokeh            | matplotlib | psutil     |
| Python 2.7             | Click            | mpi4py     | scipy      |
|                        | cloudpickle      | nose       | virtualenv |
|                        | cryptography     | numpy      |            |
|                        | dask             | pandas     |            |

</details>

<details>
<summary id="casa-stable-container">casa-stable container</summary>

**Description:** the latest stable release of CASA from [NRAO CASA website](https://casa.nrao.edu).

| Name                               | Def file        | Github repo                | OSVersion |
|------------------------------------|-----------------|----------------------------|-----------|
| casa-stable-&#60;version&#62;.simg | casa-stable.def | idia-container-casa-stable | CentOS    |

| Packages and Libraries |
|------------------------|
| CASA                   |


</details>

<details>
<summary id="casameer-container">casameer container</summary>

**Description:** casameer container used in the IDIA Pipeline software, contains CASA 5.4.1 and is appropriate for use with MPI.

| Name                            | Def file        | Github repo             | OSVersion |
|---------------------------------|-----------------|-------------------------|-----------|
| casameer-&#60;version&#62;.simg |                 |                         | CentOS    |

| Packages and Libraries |
|------------------------|
| CASA                   |
| ghostscript            |
| xvfb-run               |

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
<summary id="SF-PY3-container">SF-PY3 container</summary>

**Description:** A collection of astronomy software (originally named sourcefinding_py3), including sourcefinding, machine learning, visualization, SED- and fusion-related software.

**JupyterLab Kernel:** SF-PY3, ASTRO-PY

| Name               | Def file                     | Github repo                    | OSVersion |
|--------------------|-------------        ---------|--------------------------------|-----------|
| SF-PY3-bionic.simg |                              |                                | bionic    |

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

### Building your own container

In order to build containers a user requires root access on the system where the container is being built. Therefore, users cannot build containers directly on the ilifu system. However, containers can be built in an environment where a user has root access, and then the container can be moved to the ilifu system where it can be utilized.

There are several ways a user can build a container, including: creating a sandbox, building from a Docker image, building from the Singularity hub, building from an existing Singularity container or through a recipe or definition file . Additional information for building containers can be found at the [Singularity website](https://www.sylabs.io/guides/2.6/user-guide/build_a_container.html#).

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

In the example above the operating system that is abstracted or seen from within the container is Ubuntu 16.04 xenial. Environmental variables and paths within the container are set within the `%environment` section. Copying files into the container from the root environment where the container is being built is completed in the `%setup` section (this is now `%file` in later versions of Singularity). Installation of packages and software is undertaken in the `%post` section. In this example no `%runscript` is initiated but could be instantiated to run PINK when a container session is initialled using the `run` command. Additional information about Singularity recipes can be found [here](https://www.sylabs.io/guides/2.6/user-guide/build_a_container.html#building-containers-from-singularity-definition-files).

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

##### How to launch RStudio Server

RStudio has been updated to be launched via a the use of modules (which is described in more detail [below](#loading-and-using-modules))

The procedure is to start an interactive job, add the RStudio module and run the  `rstudio` as below:

```bash
USERNAME@slurm-login:~$ srun --nodes=1 --tasks=1 --mem=8g --time 08:00:00 --job-name="rstudio test" --pty bash
USERNAME@slwrk-101:~$ module add R/RStudio1.2.5042-R4.0.0
USERNAME@slwrk-101:~$ rstudio
The environment variable RSTUDIO_PASSWORD was not set, so your password has been chosen for you. It is: lMoV0akqQu6V2lDGu1DUMyYZGpjmoL
Running rserver on port 43627
To connect to this server run this on your local machine:
    ssh -A USERNAME@slwrk-101 -o "ProxyCommand=ssh USERNAME@slurm.ilifu.ac.za nc slwrk-101 22" -L8081:localhost:43627
then vist http://localhost:8081 in your browser and use the username "USERNAME" to login with the password "lMoV0akqQu6V2lDGu1DUMyYZGpjmoL"
(You may need to choose a different port (other than 8081), so remember to change this in both the ssh and browser
```

Note the instructions on how to access the rstudio server now from your own machine: these need to be run on the machine you're working on (rather than on the login / compute node). *The port and password will change each time you run the `rstudio` command.* When you visit the url on your local browser (http://localhost:8081) you will be presented with a login screen. Use your ilifu username and the password provided:

<img src="/_media/rstudio_login.png" alt="rsudio login page" width=800 />

You will then be presented with an rstudio session:

<img src="/_media/rstudio_session.png" alt="rstudio session" width=800 />

If you don't want the automated/random password to be created then you can set your own password using the environmental variable `RSTUDIO_PASSWORD`, i.e.
```bash
USERNAME@slwrk-101:~$ export RSTUDIO_PASSWORD="this is a long password, HoopLA"
USERNAME@slwrk-101:~$ rstudio
Running rserver on port 60407
To connect to this server run this on your local machine:
    ssh -A USERNAME@slwrk-101 -o "ProxyCommand=ssh USERNAME@slurm.ilifu.ac.za nc slwrk-101 22" -L8081:localhost:60407
then vist http://localhost:8081 in your browser and use the username "USERNAME" to login with the password "this is a long password, HoopLA"
(You may need to choose a different port (other than 8081), so remember to change this in both the ssh and browser)
```

##### Old way of launching RStudio Server (You may need this if you're using one of the older CBIO RStudio images)

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
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-58-generic x86_64)
...
```

on your local machine. Specifically what this does is forward traffic on your local machine's port `8082` to the worker node's port `37543` (and it knows how to connect to `slwrk-103` by using the `.ssh/config` settings above). One may use any free local port – ssh will complain if you choose something that is not free with an error message approximating:

```bash
bind [127.0.0.1]:8000: Address already in use
channel_setup_fwd_listener_tcpip: cannot listen to port: 8000
```

Finally in your browser you can connect to http://localhost:8082 and you can login with your `USERNAME` and the `RSTUDIO_PASSWORD` which you set.

*Note on installing packages:*

The exported environmental variable `R_INSTALL_STAGED=false` in the above scripts is only necessary should you wish to install your own packages — [this is due to the home directories using the BeeGFS filesystem](http://r.789695.n4.nabble.com/Staged-installation-fail-on-some-file-systems-td4756897.html)). Should you wish to install packages from within an RStudio session you should run `export R_INSTALL_STAGED=false` before starting the server.

## Environment Modules

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

### Loading and Using modules

Use the `module add` command, e.g.

```bash
USERNAME@slwrk-101:~$ R --version  # this won't work until the module is added

Command 'R' not found, but can be installed with:

apt install r-base-core
Please ask your administrator.

USERNAME@slwrk-101:~$ module add R/4.0.0
USERNAME@slwrk-101:~$ R --version
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

User the `module list` command, e.g.

```bash
USERNAME@slwrk-101:/cbio/soft/lmod$ module list
No modules loaded
USERNAME@slwrk-101:/cbio/soft/lmod$ module add bio/svtoolkit/2.00.1918
USERNAME@slwrk-101:/cbio/soft/lmod$ module list

Currently Loaded Modules:
  1) jdk/11.0.2   2) slurm-drmaa/1.1.0   3) bio/htslib/1.9   4) R/3.6.1   5) bio/svtoolkit/2.00.1918
```

### Anaconda

`anaconda3` is available as a module, which can be accessed with

```bash
module load anaconda3
```

This changes `python` and `python3` to use

```bash
/software/common/anaconda3/2020.07/bin/python
```

This should generally only be used on compute nodes and not the login node. However, it is accessible from the login node with

```bash
module load anaconda3/login
```
