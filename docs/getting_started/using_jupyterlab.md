# Using JupyterLab

Once you have logged into JupyterLab and selected a node size you will be placed on the main launch page of your Jupyter session. On the left sidebar you will find a directory navigation panel. On the right of the screen you will find the launch panel which provides a list of kernels to choose from. The different kernels provide the software environment within which your Jupyter notebook is run.

## Navigating to other directories

The directory navigation panel will default to your `$HOME` directory when you first log in. In order to navigate to your personal workspace or scratch directory, you can create a symlink using the terminal, from your `$HOME` directory to the relevant target directory. For example you can use the following command to create a symlink from your `$HOME` directory to your personal scratch folder:

```bash
	$ ln -s /scratch/users/<username> $HOME/scratch
```

The first parameter is the target directory of the symlink, and the second parameter is the location and name of the symlink. Remember to replace the `<username>` placeholder with your username. Once the symlink is created, you'll be able to then navigate to your scratch folder in the directory navigation window in JupyterLab.

## Jupyter kernels

There are kernels for both Python and R languages. The different kernels include different software stacks, such as the `CASA-#` kernels that contain Python wrapped CASA tasks which can be executed within the notebook, or the `ASTRO-PY3` kernel which contains an assortment of astronomy related software and Python packages. Once you have selected a kernel a notebook will be created. You can change the kernel from within the notebook by going `Kernel > Change Kernel...` from the top menu bar, or by clicking the kernel name on the top right side of the notebook panel, next to the kernel indicator circle.

The kernels themselves are in fact Singularity software containers. All the additional software packages installed in the container, beyond the Python packages, are also available to use from within the Jupyter notebook. You can make calls to these other software packages or to the underlying operating system by prefixing the relevant command with `!` in the Jupyter notebook, for example:

```
[ ]: !pwd
```
will provide you with the path of your current work directory.

The following table lists the available kernels and their related Singularity containers:

| Kernel name                 | Container                                 |
|-----------------------------|-------------------------------------------|
| ASTRO-R                     | ASTRO-R.simg                              |
| CASA-5                      | jupyter-casa-latest.simg                  |
| CASA-6                      | casa-6.simg                               |
| katcal (public)             | katcal.sif                                |
| KERN-2                      | kern-2.img                                |
| KERN-5                      | kern5.simg                                |
| PY2                         | python-2.7.img                            |
| PY3                         | python-3.6.img                            |
| Python 3                    | System Python (not a container)           |
| SF-PY2                      | source-finding.img                        |
| SF-PY3                      | ASTRO-PY3.simg                            |
| Simba                       | SIMBA.simg                                |

Details of the python libraries, software and other libraries available within the different kernels can be found in the [Available containers](tech_docs/software_environments?id=available-containers) section. An alternative way to view the available Python packages included in the kernel is to run the command `!pip freeze` in your Jupyter notebook. This command will list all the python packages available in the currently active kernel. To create a custom kernel for use in your Jupyter session, see [Using a custom container as a Jupyter kernel](tech_docs/software_environments?id=using-a-custom-container-as-a-jupyter-kernel).