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

Use the sidebar to browse the full documentation.
