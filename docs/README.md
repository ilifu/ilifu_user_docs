Ilifu User Documentation
========================

Welcome to the ilifu user documentation repository.

This user documentation site guides users on technical and procedural aspects relating to the use of the ilifu cloud computing facility.

The ilifu project website may be found at http://www.ilifu.ac.za

Ilifu training videos and the accompanying slides from our user training workshops are available on the ilifu website [here](https://www.ilifu.ac.za/latest-training/).

Please familiarise yourself with the list of recommendations below.

#### DOs:
* try to run jobs using [sbatch](getting_started/submit_job_slurm#submitting-a-job-using-a-batch-script) rather than interactive jobs
* store larger files in a project [directory](data/directory_structure.md) or your ~/workspace directory (latter limited to 10 TiB total)
* cleanup unused files when not needed
* set --time, --mem, --account parameters when [submitting jobs](getting_started/submit_job_slurm#specifying-resources-when-running-jobs-on-slurm), as accurate job parameters improves the performance of the SLURM scheduler

#### DON'Ts:
* run software on the login-node
* transfer large data on the login-node, use [transfer.ilifu.ac.za](data/data_transfer) (accessed via ssh) to do this
* copy large files to /users directory
* leave data in /scratch3 as this space is limited, after processing remove data that is not required and move files to your project directory

For more information, please see a list of [best practices](getting_started/best_practices.md). For any queries or if you need help please contact the support team at [support@ilifu.ac.za](mailto:support@ilifu.ac.za)

#### Table of Contents
- **Getting Started**
  - [Request access](getting_started/request_access.md)
  - [SSH keys](getting_started/ssh.md)
  - [Accessing the ilifu services](getting_started/access_ilifu.md)
  - [Change your password](getting_started/change_password.md)
  - [Directory structure](data/directory_structure.md)
  - [Software containers](getting_started/container_environments.md)
  - [Submit a job on Slurm](getting_started/submit_job_slurm.md)
  - [Using JupyterLab](getting_started/using_jupyterlab.md)
  - [Getting help](getting_started/getting_help.md)
  - [Best practices](getting_started/best_practices.md)
  - [Next steps](getting_started/next_steps.md)
- **Astronomy**
  - [Astronomy software](astronomy/astronomy_software.md)
  - [MeerKAT processing](astronomy/meerkat_processing.md)
- **Bioinformatics**
  - [CBIO](bioinformatics/cbio.md)
- **Data Management**
  - [Data transfer](data/data_transfer.md)
  - [Data management](data/data_management.md)
  - [Sharing data](data/sharing_data.md)
- **Technical Documentation**
  - [Specifying resources for Slurm jobs](tech_docs/running_jobs.md)
  - [Software environments](tech_docs/software_environments.md)
  - [Resource allocation guide](tech_docs/resource_allocation.md)
  - [Fairshare](tech_docs/fairshare.md)
  - [Container registry server](tech_docs/container_registry.md)
  - [Openstack](openstack/openstack.md)
  - [System specifications](tech_docs/specifications.md)
- **Help and Info**
  - [Contact and communication](help/contact.md)
  - [Requesting help](help/requesting_help.md)
- **About**
  - [What is ilifu?](about/what_is.md)
  - [Acknowledgement](about/acknowledgement.md)
