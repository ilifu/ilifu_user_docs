# Logging in to ilifu services

There are two main ilifu service platforms, including the SLURM batch schedular and JupyterLab.

## SLURM batch schedular

SLURM is a job scheduling system. It consists of a single head node and many worker nodes. The head node is likened to a controller and manages the cluster resources and job submissions. 

The SLURM system can be accessed via `ssh` at `slurm.ilifu.ac.za`. 

```
$ ssh <username>@slurm.ilifu.ac.za
```

This will place the user on the head node. Note that this node should only be used to submit and manage jobs and not for running code or software directly. This node does not have significant resources and will likely crash under heavy usage.


## JupyterLab

The JupyterLab service can be accessed via a web browser at `https://jupyter.ilifu.ac.za`. This system allows the user to spawn a virtual machine (VM) on the ilifu cloud running JupyterLab. Since the VM is launched for each user it allows for excellent management of resources, and provides a reliable environment for developing and running analyses.

After logging in to the JupyterLab service, one must select the type of node on which to run Jupyter.  The user is presented with a drop-down list with various options, and should choose the smallest node that will provide sufficient resources for the task at hand:
![dropdown](http://docs.ilifu.ac.za/_media/profile_dropdown_options.png)

Each node will be terminated after a preset interval of time (currently 3 days), however the users' Jupyter environment is saved in their home directory, so when a new Jupyter VM is spawned the workspace is recreated. Some data is also persisted in the notebook file. A user can terminate the VM in order to free up resources on the cloud, or to choose a different VM size.  This is done by choosing the `Hub` option from the top menu bar of JupyterLab:

<img src="http://docs.ilifu.ac.za/_media/hub_selection.png" alt="menu bar options" width=500 />

Choose the `Control Panel` option to stop your server:

<img src="http://docs.ilifu.ac.za/_media/stop_server_button.png" alt="stop server button" width=600 />
