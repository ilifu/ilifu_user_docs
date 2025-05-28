# Temporary Files

Temporary files are files that are not intended to be kept permanently. They are often used for intermediate data, temporary storage, or caching purposes. In the context of ilifu, temporary files can be created during data processing, job execution, or other operations and should be managed carefully to avoid unnecessary storage usage.

In addition to the scratch storage described in the [Directory structure](data/directory_structure.md#scratch-storage) section, many applications and jobs will, by default, create temporary files in the user's home directory, in the job's working directory and in the `/tmp/` system directory. These files can accumulate over time and consume significant disk space. It is important to regularly clean up these temporary files to maintain a healthy storage environment. `/tmp/` is especially important to clean up as it is shared by all users and can fill up quickly, leading to system issues and should be avoided if at all possible.

## Using `/dev/shm/` for Temporary Files
The `/dev/shm/` directory is a temporary filesystem (tmpfs) that is used for shared memory in Linux. It is often used for storing temporary files that need to be accessed quickly. The advantage of using `/dev/shm/` is that it is stored in RAM, which makes it much faster than disk-based storage. But in order to use it effectively, you need to ensure that the size of `/dev/shm/` is sufficient for your needs — and this will come out of your memory allocation for the job. So if you are running a job that requires a lot of temporary storage, you should ensure that the job is allocated enough memory to accommodate the size of `/dev/shm/` in addiction to the memory required for the job itself.

### Example Usage
Below is an example of how to use `/dev/shm/` for temporary files in a Slurm job script:

```bash
#!/bin/bash
#SBATCH --job-name=my_temp_job
#SBATCH --mem=8G

TMPDIR=`mktemp /dev/shm/${USER}.XXXXX -d`  # this creates a temporary directory in /dev/shm and stores the path in TEMPDIR
TMP=${TMPDIR}
TEMP=${TMPDIR}
export TMPDIR TMP TEMP  # this exports variables for jobs that may use them

# Your job commands go here
# For example, running a command that allows you to specify the temporary directory
my_command --temp-dir ${TMPDIR} some_input_file

# Clean up the temporary directory after the job is done
rm -rf ${TMPDIR}
```

This script creates a temporary directory in `/dev/shm/`, sets the necessary environment variables, runs a command that uses the temporary directory, and then cleans up the temporary directory after the job is done.
