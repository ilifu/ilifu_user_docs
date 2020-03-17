# Logging into the ilifu services

There are two main ilifu service platforms, including the SLURM batch scheduler and JupyterLab.

## SLURM batch scheduler

SLURM is a job scheduling system. It consists of a single login node and many worker nodes. The login node is likened to a controller and manages the cluster resources and job submissions. 

The SLURM system can be accessed via `ssh` at `slurm.ilifu.ac.za`. 

```
$ ssh <username>@slurm.ilifu.ac.za
```

This will place the user on the login node. Note that this node should only be used to submit and manage jobs and not for running code or software directly. The worker nodes are where jobs are run, either through submitting a batch script that describes the job to be executed, or interactively running applications on a worker node. See [Submitting a job on SLURM](getting_started/submit_job_slurm.md) for more information on how to do this.


## JupyterLab

The JupyterLab service can be accessed via a web browser at `https://jupyter.ilifu.ac.za`. This system allows the user to spawn a virtual machine (VM) on the ilifu cloud running JupyterLab. Since the VM is launched for each user it allows for excellent management of resources, and provides a reliable environment for developing and running analyses.

After logging into the JupyterLab service, one must select the type of node on which to run Jupyter.  The user is presented with a drop-down list with various options, and should choose the smallest node that will provide sufficient resources for the task at hand:
![dropdown](http://docs.ilifu.ac.za/_media/profile_dropdown_options.png)

Each node will be terminated after a preset interval of time (currently 3 days), however the users' Jupyter environment is saved in their home directory, so when a new Jupyter VM is spawned the workspace is recreated. Some data is also persisted in the notebook file. A user can terminate the VM in order to free up resources on the cloud, or to choose a different VM size.  This is done by choosing the `Hub > Control Panel` option from the top menu bar of JupyterLab:

<img src="http://docs.ilifu.ac.za/_media/hub_selection.png" alt="menu bar options" width=500 />

This will bring you to the page with the `Stop My Server` option, where you can stop your current session, freeing up the resources that have been allocated to your Jupyter session. You are also able to use this process to change the size of the resources allocated to you. Once you have stopped your session you are able to choose a smaller or larger node size.

<img src="http://docs.ilifu.ac.za/_media/stop_server_button.png" alt="stop server button" width=600 />
