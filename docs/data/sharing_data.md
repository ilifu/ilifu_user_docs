# Sharing Data

## Sharing files or data with existing users or groups

### Sharing data in the project directory

The best way to share data with other project members is to place the data in the shared project folder, located at `/idia/projects/`, `/cbio/projects/`, `/ilifu/<astro|bio>/projects/`, or, if during processing, `/scratch3/projects/`. Placing data in the project folder means that it will be accessible to all project members. This method is particulary good to use if the data is associated with the core science objectives of the project, so that the data is correctly accounted for against the project's storage quota. Any project member can create a folder in the project directory or write data to this location, but it may be a good idea to confirm with the project PI before doing so.

### Sharing data using standard UNIX permissions

You can provide access to files and folders using standard UNIX permissions. The permissions are managed using `chmod`, which manages the read (`r`), write (`w`) and execute (`x`) permissions on files and directories for Owner (`u`), Group (`g`), and Other (`o`). You can only provide access to groups of users or all users using this method, so it is greatly limited (i.e. you shouldn't open up access permissions unnecessarily!)!

You can allow access on a directory to a group of users using the `chmod` command, for example:
```bash
$ chmod g+rx /idia/users/$USER
```
This will enable (`+`) read (`r`) and execute (`x`) permissions on the specified directory (your user workspace in this example) to all members of the group (`g`) of the currently configured group owner. Note that, by default, your workspace will have group ownership of the general group (`idia-group`, `cbio-group`, `ilifu-group`), meaning that any user in that group will now have access to your directory and data. If you want to restrict access to your project group, first adjust the group ownership to the project group with which you want to share the data, for example, to change the group owner of your workspace to the MIGHTEE project group:

```bash
$ chgrp idia-mightee /idia/users/$USER
```
And then run the `chmod` command. 

To remove the group read and execute permission use a `-` in place of the `+`:
```bash
$ chmod g-rx /idia/users/$USER
```

These commands can be run rescursively, using `-R`, to adjust the permissions on all subdirectories and files. To navigate into a directory, execute (`x`) permission is required. If you enable access on a file or directory in a subdirectory, and the user trying to access these paths doesn't have access permissions enabled on the parent directory, they will not be able to access the files. You can provide execute permissions (`x`) on parent directories, without providing read access (`r`), to allow the user to navigate to the intended file or subdirectory. 

When opening access to files or directories, always be aware of the group ownership and access permissions set on your other files and directories. You can list these using `ls -ld`, for example:
```bash
$ ls -ld /idia/users/$USER
drwx------ 12 janedoe idia-group 21 Oct  7 13:02 /idia/users/janedoe
```

By default, any directory or file created will have access permissions `drwxr-xr-x` and `-rw-r--r--`, respectively, meaning that once a group has been given access to the parent folder, they will have read or execute access on most other files and subdirectories. 

**Becareful! If you modify 'u' (Owner) permissions on a file or directory, you can remove your own access!**

**It is easy to forget that you've opened up permissions on your direcories, and then place sensitive data at these locations, unintentionally providing access. Always limit access as much as possible, and remember to remove access as soon as it is no longer needed.**

### Sharing data using ACLs

An **Access Control List** (ACL) is a feature that provides fine grain control for managing permissions on the file system, more so than standard UNIX permissions. With ACLs you are able to share data with individual users, and provide groups access without having to adjust group ownership.

ACLs are set using the `setfacl` command. For example, to share data with another user, the following will enable read (`r`) and execute (`x`) permissions on your workspace folder, in this case for the user `janedoe`:
```bash
$ setfacl -m u:janedoe:r-x /idia/users/$USER
```
You can view the ACLs that are configured on a file or folder using the `getfacl` command, for example:
```bash
$ getfacl /idia/users/$USER
getfacl: Removing leading '/' from absolute path names
# file: idia/users/johndoe
# owner: johndoe
# group: idia-group
user::rwx
user:janedoe:r-x
group::---
mask::r-x
other::---
```
To share data with a project group, the following will enable read (`r`) and execute (`x`) permissions on your scratch folder, in this case for the group, `idia-mightee`:
```bash
$ setfacl -m g:idia-mightee:r-x /scratch3/users/$USER
```
You can remove ACLs using the `-x` parameter, for example:
```bash
$ setfacl -x u:janedoe: /idia/users/$USER
$ setfacl -x g:idia-mightee: /scratch3/users/$USER
```
Or the following will remove all configured ACLs on the specified directory:
```bash
$ setfacl -b /idia/users/$USER
```
The above `setfacl` commands can be set recursively on all files and subdirectories in the specified directory using the `-R` parameter.

If you enable access on a file or directory in a subdirectory, and the user trying to access these paths doesn't have access permissions enabled on the parent directory, they will not be able to access the files. To navigate into a directory, execute (`x`) permission is required. You can provide execute permissions (`x`) on parent directories, without providing read access (`r`), to allow the user to navigate to the intended file or subdirectory without providing access to other files or directories. For example, say you want to provide user `janedoe` access to the directory at `/idia/users/$USER/thesis/COSMOS_output`, without providing them access to other files or directories located at `/idia/users/$USER` or `/idia/users/$USER/thesis`, you can do the following:

Enable execute (`x`) permissions on the two parent directories for the user `janedoe`:
```bash
$ setfacl -m u:janedoe:--x /idia/users/$USER
$ setfacl -m u:janedoe:--x /idia/users/$USER/thesis
```
And then provide execute (`x`) and read (`r`) permissions on the `COSMOS_output` directory and all contained files and subdirectories:
```bash
$ setfacl -R -m u:janedoe:r-x /idia/users/$USER/thesis/COSMOS_output
```
The user `janedoe` will now be able to navigate to and view all files located at `/idia/users/$USER/thesis/COSMOS_output` without having access to other files and directories located in the parent directories.

## Sharing files or data with non-ilifu users

Data releases associated with IDIA projects can be made publically available on the [IDIA Public Data Archive](https://gateway.idia.ac.za/public_data), available from the IDIA Science Gateway.

Other than the IDIA Public Data Archive, currently, no service is provided to allow sharing of files with persons who do not have an ilifu account. An ilifu account is required to access the file system.

To share files or data with non-ilifu users, you would need to transfer the data to an alternative site where the intended person has access. A possible solution is to use `rclone`, available as a module on ilifu, to upload files to a Google Drive folder, and share the files on Google Drive.
