Ilifu User Documentation
========================

Welcome to the ilifu user documentation repository.

This user documentation site guides users on technical and procedural aspects relating to the use of the ilifu cloud computing facility.

The ilifu project website may be found at http://www.ilifu.ac.za

Please familiarise yourself with the list of recommendations below.

#### DOs:
* try to run jobs using [sbatch](getting_started/submit_job_slurm#submitting-a-job-using-a-batch-script) rather than interactive jobs
* cleanup unused files when not needed
* set --time, --mem, --account parameters when [submitting jobs](getting_started/submit_job_slurm#specifying-resources-when-running-jobs-on-slurm), as accurate job parameters improves the performance of the SLURM scheduler

#### DON'Ts:
* run software on the login-node
* transfer large data on the login-node, use [transfer.ilifu.ac.za](data/data_transfer) (accessed via ssh) to do this
* copy large files to /users directory
* leave data in /scratch as this space is limited, after processing remove data that is not required and move files to your project directory

For more information, please see a list of [best practices](getting_started/best_practices.md). For any queries or if you need help please contact the support team at [support@ilifu.ac.za](mailto:support@ilifu.ac.za)

#### Table of Contents
- **News**
  - [Updates](news/updates.md)
- **Getting Started**
  - [Request access](getting_started/request_access.md)
  - [SSH keys](getting_started/ssh.md)
  - [Accessing the ilifu services](getting_started/access_ilifu.md)
  - [Change your password](getting_started/change_password.md)
  - [Directory structure](data/directory_structure.md)
  - [Software containers](getting_started/container_environments.md)
  - [Submit a job on SLURM](getting_started/submit_job_slurm.md)
  - [Using JupyterLab](getting_started/using_jupyterlab.md)
  - [Getting help](getting_started/getting_help.md)
  - [Best Practices](getting_started/best_practices.md)
  - [Next Steps](getting_started/next_steps.md)
- **Technical Documentation**
  - [Astronomy](astronomy/astronomy_software.md)
  - [Bioinformatics](bioinformatics/cbio.md)
  - [Running jobs on the cluster](tech_docs/running_jobs.md)
  - [Fairshare](tech_docs/fairshare.md)
  - [Supported software environments](tech_docs/software_environments.md)
  - [Data Transfer](data/data_transfer.md)
  - [Openstack flavours](openstack/flavours.md)
  - [System Specifications](tech_docs/specifications.md)
- **Help and Info**
  - [FAQ](help/faq.md)
  - [Contact and Communication](help/contact.md)
  - [Requesting Help](help/requesting_help.md)
- **About**
  - [What is ilifu?](about/what_is.md)