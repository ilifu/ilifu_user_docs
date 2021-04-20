# Data transfer to and from the ilifu Facility

Transferring of data to and from the ilifu research cloud can be completed using `Globus`, `scp` or `rsync`. For large files the `Globus Online` software is recommended, which uses efficient GridFTP transfer protocols. **Please do not transfer data to and from the ilifu facility using the SLURM login node, as this will significantly diminish the performance of the login node for other users**.

Transferring astronomy observation data from the SARAO archive is also detailed [below](#transfer-data-from-the-sarao-archive).

## Transfer using scp and rsync

A dedicated transfer node is available at `transfer.ilifu.ac.za` for transferring files using `scp` and `rsync` to and from the ilifu facility. All users may ssh onto this transfer node.

The `scp` and `rsync` tools are useful for transferring data up to 200 GB, or if you're not expecting to transfer data frequently. For files over 200 GB or for frequent transfers, it is recommended to use the Globus Online software below. **Please note that large files should not be copied into your `/users/` directory.**

The following is an example of how to scp from your personal computer to the ilifu facility. From the terminal on your personal computer:

```
$ scp /path/to/file/<filename> <username>@transfer.ilifu.ac.za:~
```

The above command will copy the file to your home directory on ilifu. You can also specify an alternative path in the destination, for example:

```
$ scp /path/to/file/<filename> <username>@transfer.ilifu.ac.za:/idia/users/<username>/scripts/
```

For more information about the `scp` and `rysnc` tools please read the manual pages using `man scp` or `man rysnc` from the command line.

## Transfer using Globus Online

The `Globus Online` software is available at [https://app.globus.org](https://app.globus.org).

There are a number of different options for signing in. It may be possible to login using your institution's credentials by searching for your institution's name. Other login options are also available. If you don’t want to link your Globus account to another account, then select `Use Globus ID to sign in` and you’ll be able to create an account specific to Globus.

<div style="text-align:center"><img src="/_media/data_globus_01.png" alt="globus online login" width=500 /></div>

After logging in you will be redirected to the [Globus file manager](https://app.globus.org/file-manager).

In the centre of the screen you should see a box labelled `Collection`:

<div style="text-align:center"><img src="/_media/data_globus_02.png" alt="globus online collection" width=500 /></div>

Type in `ilifu` there and the resulting search should point you the the ilifu data transfer node (DTN):

<div style="text-align:center"><img src="/_media/data_globus_03.png" alt="globus online collection ilifu" width=400 /></div>>

You will then be redirected to a login screen, where you can enter your ilifu credentials:

<div style="text-align:center"><img src="/_media/data_globus_04.png" alt="globus online ilifu login" width=500 /></div>>

You will be asked to give consent for Globus to access your directories. You’ll then be redirected to a window where you’ll be able to browse through your home directory on the ilifu system. The ilifu system is only one endpoint of the transfer process. You will need to then set up the source or destination for the transfer. In order to do this, click on the button in the upper right corner of the file list, and you’ll see a menu displayed:

<div style="text-align:center"><img src="/_media/data_globus_05.png" alt="globus online options menu" width=200 /></div>

Select `Transfer or Sync to...` to select the other endpoint in your file transfer. This will open up another panel for selecting the other endpoint, which you'll need to configure. You can set up an endpoint for you desktop, as documented [below](#setting-up-an-endpoint-for-your-desktop). If you are a user of the Centre For High Performance Computing (CHPC), you can also search for the Lengau cluster at the CHPC by typing "CHPC South Africa - Lengau" into the search bar, and using your CHPC credentials to authenticate yourself in the same way as for ilifu.

<div style="text-align:center"><img src="/_media/data_globus_06.png" alt="globus online set endpoint" width=600 /></div>>

#### Configuring a transfer

Globus does not transfer symbolic links, so data transferred that includes symlinks, such as Multi-MeasurementSets (MMS) for astronomy, will be incomplete. Therefore, it is advised that the user select "Transfer & Sync Options" --> "preserve source file modification times" from the file manager. This enables the symlinks to be later repaired with a quick and simple rsync command, such as:

```bash
rsync -avhn --size-only --progress --stats <username>@transfer.ilifu.ac.za:/scratch/users/${USER}/my_data/ /${USER}/my_desktop/my_data
```

This will perform a 'dry run', which will "perform a trial run with no changes made". After verifying the correct files (i.e. symlinks only) will be transferred, re-running the expression above with option `-n` removed will perform the transfer.

#### Setting Up An Endpoint for your Desktop

You can also use Globus to transfer files between ilifu and your desktop using the `Globus Connect Personal`. For installing on your personal computer, click [here](https://docs.globus.org/how-to/globus-connect-personal-linux/) for Linux, [here](https://docs.globus.org/how-to/globus-connect-personal-mac) for Mac OS X, or [here](https://docs.globus.org/how-to/globus-connect-personal-windows) for Windows.

Note that by default you may be unable to access paths outside your home directory using Globus Connect Personal for Linux.  Instructions on how to change the accessible paths can be found [here](https://docs.globus.org/faq/globus-connect-endpoints/#_how_do_i_configure_accessible_directories_on_globus_connect_personal_for_linux).

Once `Globus Connect Personal` is installed, head back to the `File Browser`, and select the box allowing you to specify the other collection to install.  On the resulting page you should then be able to select the `Your Collections` tab where you should find your `Globus Connect Personal` endpoint.  Select it by clicking on its name, in this case `Test Endpoint`.

<div style="text-align:center"><img src="/_media/data_globus_07.png" alt="globus online your collections" width=350 /></div>

You should then see a file browser where you can see your ilifu files on the left, and the files from your other endpoint on the right.

You’ll then be able to start making transfers. The interface here resembles a traditional file browser. Select one or more ilifu files to transfer by browsing in the left hand side window and selecting them.

Then shift focus to your other endpoint, by clicking on the greyed out file list. You can then browse around to select your destination, creating a `New Folder` if desired. In the example below we’ve selected the file named `foo` on ilifu to transfer to the `transfer test` folder in my home directory:

<div style="text-align:center"><img src="/_media/data_globus_08.png" alt="globus online transfer example" width=650 /></div>>

Then click the **left** `Start` button at the bottom of the page to initiate a transfer to your system from ilifu (the **right** `Start` button will transfer to ilifu instead).

<div style="text-align:center"><img src="/_media/data_globus_09.png" alt="globus online start" width=300 />
</div>>

You should then see a similar message appear on the page as the following:

<div style="text-align:center"><img src="/_media/data_globus_10.png" alt="globus online activity notification" width=600 /></div>

Globus will then inform your by email of the status of your transfer once it’s either failed or completed or you can click `Activity` in the sidebar to monitor its progress.

**Note that by default Globus will only be able to act on your behalf for 24 hours from since you last submitted your ilifu username and password in the Globus interface to login to the DTN.  At times you may need to extend the lifetime of your credentials.**  To do so, click `Endpoints` in the sidebar, select `ilifu DTN`, and you should then see a button labelled `Extend Activation` on the right hand side of the screen.  You’ll then see a login screen for the `ilifu DTN` similar to before where you can login to extend the credentials available to Globus for a further time period.  (A lifetime other than 24 hours can be specified by clicking `Advanced` and entering a different lifetime in hours, though individual transfers may still be limited to 24 hours each).

#### Using Globus for internal ilifu transfers

Globus can be used to transfer files internal to ilifu (e.g. from one filesystem to another), by setting the two endpoints as the ilifu DTN. However, the performance (< 100 MB/s) is comparable to running `cp`, `mv`, `rsync` or `scp` on transfer.ilifu.ac.za. In the event that a user makes a transfer with Globus (e.g. under poor network conditions, or for long transfers), it is advised that the user [configure a transfer](#configuring-a-transfer) following the instructions above.

#### Setting Up An Endpoint for Another Data Transfer Node

`Globus Connect Personal` can also be installed on computing clusters. However, for best support and reliability, if the destination to which you wish to transfer files operates an endpoint already registered with Globus, it is highly recommended to use this endpoint instead. Just search for the endpoint in the collections box on the right as before and complete the login process similar to how you logged into the ilifu DTN.

If your institution does not already have a Globus endpoint, you can setup Globus Connect Personal on Linux. Click [here](https://docs.globus.org/how-to/globus-connect-personal-linux/#globus-connect-personal-cli) for installing on a computing cluster.

Once a transfer is initiated, as long as the Globus platform can reach both ilifu and the location you’re transferring files to, no connectivity is required to other machines (i.e. assuming you’ve installed the Globus Connect Personal software on a compute server, rather than on your personal computer, you should not have to worry if your laptop loses network connectivity or is shut down, as long as the `Globus Connect Personal` software continues to run on the server.

## Transfer data from the SARAO archive

If you are a principal investigator (PI) or member of one of the MeerKAT projects whose proposal has been accepted by SARAO, such as a Large Survey Project (LSP) or an Open Time Project, you may want to transfer your observational data from the SARAO archive to the ilifu facility.

Before pushing your data, it is important to have an existing project on the ilifu facility in order for us to make the data available to the project members. If you do not have an existing ilifu project, please make contact with the ilifu support team at support@ilifu.ac.za to request one, and notify us of your intention to transfer data. Eligible MeerKAT projects are those with a PI or lead technical contact based at a South African institution. ​If a student is the PI, they will need written approval from their supervisor.

In order to push your data from SARAO to ilifu, a PI, or a representative that a PI has nominated, must go to [https://archive.sarao.ac.za](https://archive.sarao.ac.za) and register an account. Once they have registered, the PI must send an email to archive@ska.ac.za requesting for this person to access the proposal.

The user guide for the archive is available [here](https://archive.sarao.ac.za/statics/Archive_Interface_User_Guide.pdf).

### MVF to MS configuration

In February 2020, new SARAO archive functionality was introduced to configure the conversion to MeasurementSet (MS), including the selection of channel ranges, polarisation products, flags, and options to average in time and frequency channel. It is important to note that currently (March 2020):

1. Only a single transfer is allowed per MS<sup>1</sup>
2. Newer transfers (manually done following instructions below) overwrite older data<sup>1</sup>
3. Transfers are MS by default<sup>2</sup>

Discussions to optimise this process are ongoing. For now, we suggest that users transfer only a single MS per dataset, and set `-a true` (to remove auto-correlations) and `--flags=cam,data_lost` (to apply instrumental flags that can't be identified during processing, and to avoid flagging real data, including HI lines). If you have no interest in polarisation data, we also suggest you use `-f false` and `-p HH,VV`, which will halve your data volume. Using `--quack=1` (to discard the first dump) may also be desirable. Conversion options are shown [here](https://github.com/ska-sa/MeerKAT-Cookbook/blob/master/archive/Convert%20MVF%20dataset(s)%20to%20MeasurementSet.ipynb), and flagging options [here](https://archive.sarao.ac.za/statics/sdp_flags.pdf).

<sup>1</sup> After a dataset has been transferred, the SARAO archive sets a flag that prevents that same dataset from being downloaded to the same destination. If you must re-transfer your data, and the archive disallows another transfer (orange arrow labelled 'IDIA'), firstly contact [ilifu support](mailto:support@ilifu.ac.za) to rename (or remove) your data, and then contact the [SARAO archive](mailto:archive@ska.ac.za) to reset the flag.

<sup>2</sup>Transfers of data in the native MeerKAT format (MFV / MKV4) can also be arranged by contacting the [SARAO archive](mailto:archive@ska.ac.za).

### Changes to flagging

On 26 November 2019, the default [flags](https://archive.sarao.ac.za/statics/sdp_flags.pdf) were updated to `cam,data_lost,ingest_rfi`, whereas previously, particularly for MeerKAT Open Time Projects (OTPs), they included the full set of flags, with ~30% of the raw target data typically being flagged, or sometimes up to ~90%. Users affected by this can re-transfer the data following the instructions in the [section above](#mvf-to-ms-configuration). Data older than the OTPs may be affected in different ways, as the archive and its functionality were still being built. Newer transfers can configure these flags using the SARAO archive functionality described in the [section above](#mvf-to-ms-configuration).
