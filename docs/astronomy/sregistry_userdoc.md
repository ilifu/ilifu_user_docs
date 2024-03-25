# IDIA Singularity Registry Server 

The IDIA Singularity Registry Server (IDIA sregistry) is available for managing, organising, and sharing Singularity container images. Ilifu users are able to upload containers and maintain their own teams and collections. Public containers are available to be downloaded to any remote site using Singularity CE software.

## Requirements

An ilifu user account is required to upload containers to the IDIA Singularity Registry repository.
For containers to be uploaded to the IDIA Singularity Registry repository, the containers must have been built using Singularity `version 3.3.0+`

## Support
Contacts ilifu support at support@ilifu.ac.za to get help with uploading or downloading containers from IDIA sregistry

## Definitions
`Collection` describes a class of containers, or a project group for which containers are created. A collection can be public or private, and, if private, only the creator, or assigned group, will have access to the collection.<br />
`Container_name`, is the name of the container (this is usually the name of the primary software, the project group for which the container is created, or a custom name if the container includes multiple software packages without a clear primary packages).<br />
`Tag` is the version of the primary software package included in the container (example v6.5.0), a date to indicate different builds (2023-01-23), or another custom versioning method.<br />
`Team` is a group of users that can be assigned as collaborators to a collection.

## Available Collections
To view available containers visit our web UI at https://sregistry.idia.ac.za/collections. All container-collections listed are publicly available.

## Access/Download Available Containers:
All containers listed in the collection page are available for use by the public. Containers can be pulled to the local machine using the Singularity CE pull only. 

Example:
Run this `cmd`to pull/download a `container` in `collection` with `tag`.
```bash
singularity pull --library https://sregistry.idia.ac.za/ collection/container:tag
```
To pull a container called `wsclean` with a tag `v3.3` in a collection called `busybox`, We use the cmd:
```bash
singularity pull --library https://sregistry.idia.ac.za/ busybox/wsclean:v3.3
```

If you have already added the **remote endpoint**, you can pull the same container using the cmd below (See https://docs.sylabs.io/guides/3.7/user-guide/endpoint.html for details about adding an end-point, also see below about adding IDIA sregistry end-point):
```bash
singularity pull library://busybox/wsclean:v3.3
```
**Note**: most public containers available in the IDIA sregistry are also available on ilifu at `/idia/software/containers`. Please confirm whether the container already exists on the filesystem before pulling the container to ilifu storage. 

Containers from the repository can be used within a job step, without creating the container image file, using the following examples: 

Run the container:
```bash
singularity run --library https://sregistry.idia.ac.za/ collection/container:tag
```
Similarly if the registry end-point already exist then:
```bash
singularity run library://collection/container:tag
```
Shell into the container:
```bash
singularity shell --library https://sregistry.idia.ac.za/ collection/container:tag
```
Similarly if the registry end-point already exist then:
```bash
singularity shell library://collection/container:tag
```
**Note**: containers used this way are stored in a local cache (usually `$HOME/.singularity/cache` if an alternative is not set using `SINGULARITY_CACHEDIR`). The storage used for this can grow considerably over time and we recommend using `singularity cache clean -a` to remove images after use.
 

## Pushing Containers to the Registry
Any user with the IDIA/ilifu user account is able to login and push images to their collections.

### Adding remote end-point (also see this [guide](https://docs.sylabs.io/guides/3.7/user-guide/endpoint.html)).

To Add the registry end-point, run:
```bash
singularity remote add idia-registry https://sregistry.idia.ac.za/
```
It will ask for an access token. This token can be accessed by going to the [webUI](https://sregistry.idia.ac.za). Click login and once you have logged-in there will be a dropdown menu from your username at the top right. Click this drop down button and select Token. Copy the token (it will look something like: `742a2ca17065a2d0137f24ec30455a4a3cd3fe2e`) to the clipboard and paste it on the terminal. You should receive confirmation that the token is verified, as follows:.
```
Generate an access token at https://sregistry.idia.ac.za/auth/tokens, and paste it here.
Token entered will be hidden for security.
Access Token: 
INFO:    Access Token Verified!
INFO:    Token stored in /users/walter/.singularity/remote.yaml
```

If you get an issue like:
```
INFO:    Remote "idia-registry" added.
Generate an access token at https://sregistry.idia.ac.za/auth/tokens, and paste it here.
Token entered will be hidden for security.
Access Token: 
FATAL:   while verifying token: error response from server: Invalid Credentials
```
Try updating the token and login to the endpoint. Since it is already created, there is no need to add it again:
```bash
singularity remote login idia-registry.
```

### Create a collection
To create a collection login via the [webUI](https://sregistry.idia.ac.za). Go to [View Collection](https://sregistry.idia.ac.za/collections) or select containers from the top menu. You Should see the “New Collection” button. Use this to create a collection. A collection name should all be in small letters and must not have the “/” or ”.” characters.

### Push the container to your collection:
**NB**. You can only push containers to the collections you created, or one to which your group has been assigned.

Make sure the end point is added successfully. 
You can check the remote status via; `singularity remote use idia-registry`, then `singularity remote status` and output would look like.
```
INFO:    Checking status of default remote.
SERVICE    STATUS  VERSION  URI
Keyserver  OK      v1.0.0   https://sregistry.idia.ac.za
Library    OK      v1.0.0   https://sregistry.idia.ac.za
Token      OK      v1.0.0   https://sregistry.idia.ac.za
INFO:    Access Token Verified!

Valid authentication token set (logged in).
```
This means you are ready to push images.<br />
To push a container named `astror` to a collection `calibration` (as shown in the screenshot above), run:
```bash
singularity push -U ASTRO-R.simg library://walter/calibration/astror:latest
```
In this command: `ASTRO-R`is the local name of the container that I want to push, `walter` - is my username, `calibration` is the name of the collection I am pushing the container to, `astror` is the name a container will have in the IDIA sregistry, `latest` is the tag of the container. 
See the screenshot below to demonstrate the container has been uploaded.. 

## Team/Group Container Management
A team (group of users) can be created to manage a collection specific to a project and multiple users must manage it. A team is created by an authenticated user. Creating a team means that the creator becomes the Owner of the team that can add and remove users. A user in a group then has the ability to push containers to the collection and also has permissions to view private containers.

Create a Teams:
- Go to webUI:https://sregistry.idia.ac.za/
- Click on the “Teams” tab in the navigation bar
- Choose a name, team name, and image.
- Decide if your team is “open” or “invite” only
- **invite** only means that an owner must send an invitation link.
- **open** means that anyone can join the team that is authenticated in the registry